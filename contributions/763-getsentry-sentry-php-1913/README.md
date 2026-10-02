# getsentry/sentry-php #1913: Add option to exclude certain HTTP statuses from tracing

| 项 | 值 |
|---|---|
| Issue | https://github.com/getsentry/sentry-php/issues/1913 |
| Tier | 自由 |
| Labels | Feature, PHP, Performance (New), Traces, good first issue |
| Status | ✅ ready：patch 和 PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01 查过：issue 仍 open，无 assignee、无评论，Development 区没有关联 PR。用 `pulls?q=1913`、`trace_ignore_status_codes`、`404`、`ignore status` 搜索，没有相关 PR。当前 6 个 open PR 都与此无关。 |
| Base | `master` @ b06d0bd1afb3cf8537ad295454aeb3ef0ee1da13（2026-10-01，"fix: respect rate limits on 429 responses with a body (#2225)"） |

## 问题理解
issue 作者是 Sentry 员工 dingsdax。诉求：新增一个向后兼容的选项（建议叫 `trace_ignore_status_codes`），让 SDK 不追踪指定 HTTP 状态码（比如 404）的入站请求。默认值保持现状，即 404 仍然会被追踪。要求带测试和文档。

develop.sentry.dev 的 Traces 规范定义了 `traceIgnoreStatusCodes`：
- 值是整数集合，可以额外接受 `[min, max]` 闭区间。
- 事务结束前读取 `http.response.status_code` 属性，命中就把采样决策改成 not sampled。
- 只作用于入站请求。
- 在 minor 版本引入时默认为空。下一个 major 版本的推荐默认值是 `[[301,303],[305,399],[401,404]]`。
- 要输出 debug 日志。如果 SDK 支持 client report，还要记录 `event_processor` 丢弃原因。

## 合理性判断
- issue 由 Sentry 员工提出，带 good first issue 标签，规范里也写明了这个选项。
- sentry-python 已有同名选项 `trace_ignore_status_codes`（见 `sentry_sdk/consts.py`），所以 PHP 用同样的名字。
- 放在 core 而不是 sentry-laravel / sentry-symfony：规范把它定义成 SDK 选项。sentry-laravel 的 Tracing Middleware 已经在 transaction 上设置了 `setData(['http.response.status_code' => ...])`，core 实现后 Laravel 直接就能用。
- sentry-php 没有 client report 机制，所以只写了 debug 日志。

## 改动
- `src/Options.php`：新增 `trace_ignore_status_codes` 选项。
  - 默认 `[]`。
  - allowed type 为 `array`，再由 `validateTraceIgnoreStatusCodesOption` 校验：每一项必须是 int，或者恰好两个 int 的 `[min, max]`，且 min <= max。
  - 新增 `getTraceIgnoreStatusCodes()` / `setTraceIgnoreStatusCodes()`。
- `src/Tracing/Transaction.php`：`finish()` 中，已采样的事务如果 `data['http.response.status_code']`（int 或纯数字字符串）命中选项，就设为不采样，不再发送，并通过 logger 输出一条 info 日志。没有该 data 的事务（CLI、队列等）完全不受影响，因此只作用于入站请求事务。
- `src/functions.php`：`init()` 的 array-shape 文档里加了这个选项。
- `tests/OptionsTest.php`：在 optionsDataProvider 和默认值列表中加了对应项，新增校验用例 `testTraceIgnoreStatusCodesOptionIsValidatedCorrectly`。
- `tests/Tracing/TransactionTest.php`：新增 `testFinishRespectsTraceIgnoreStatusCodesOption`，覆盖精确匹配、区间、闭区间边界、数字字符串、不匹配、默认值等情况。新增 `testFinishIgnoresTraceIgnoreStatusCodesOptionWithoutStatusCode`。
- 按 AGENTS.md 的要求，没有改 README.md、CHANGELOG.md 和 `Client::SDK_VERSION`。

## 验证（PHP 8.3.6，工作目录 /home/user/work/sentry-php，分支 feat/trace-ignore-status-codes）
- 依赖安装：本环境无法通过 api.github.com 下载 zipball（403）。`phpstan/phpstan` 没有 source，只能先浅克隆 1.12.34 tag（commit 与 lock 一致），再用临时的 `COMPOSER=composer.local.json` 和 lock 副本，把 dist 指向本地 path 后执行 `composer install`。临时文件已删除，仓库内的 composer.json 和 composer.lock 都没有改动。
- Red：`git stash push -- src` 之后运行 `vendor/bin/phpunit --filter 'TransactionTest|OptionsTest'`，结果 `Errors: 14, Failures: 8`。失败的是所有新用例、`testAllOptionsAreCoveredByOptionsDataProvider` 和 `testDefaultOptionValues`。
- Green：同一命令结果为 `OK (261 tests, 328 assertions)`。
- 全量 `vendor/bin/phpunit`：`Tests: 1561, Skipped: 10`，全部通过。base 上是 1537 个测试、10 个 skipped，skipped 数量相同。
- `vendor/bin/php-cs-fixer fix --verbose --diff --dry-run`：0 个文件需要修改。
- `vendor/bin/phpstan analyse --memory-limit=512M`：`[OK] No errors`。
- `vendor/bin/mago --config=mago.toml analyze`：exit 0。剩下的 3 条 warning（OptionsResolver ×2、FileAttachment）在 base 上同样存在，没有新增。
- `composer check` 没有直接运行：以 root 运行时 composer 会拒绝执行脚本。改为逐条运行它包含的 4 个命令（见上）。
- 在干净的 master 上执行 `git am 0001-*.patch` 能成功应用，结果与工作分支一致。
- 没有跑 PHP 7.2：本机只有 PHP 8.3。代码只用了 7.2 可用的语法和函数，`ctype_digit` 在 `src/Transport/RateLimiter.php` 中已有使用。

## 需要提交者注意
- 仓库的 `validate-pr` workflow：外部 PR 改动达到 100 行或以上（本 PR 约 222 行），且 PR 作者和维护者都没有在关联 issue 下评论时，会自动发一条提示评论（不会关闭 PR）。建议先在 #1913 下留言说明打算实现，最好等维护者回应后再开 PR。
- issue 作者 dingsdax 是 Sentry 员工。
- 只有设置了 `http.response.status_code` data 的事务才会被过滤。sentry-laravel 已经设置了这个 data。sentry-symfony 目前只调用 `setHttpStatus()`（只写 scope context），需要后续单独提 PR 补上。也可以让 core 的 `Span::setHttpStatus()` 同时写 data，但这样会改变现有 payload，所以这次没做，PR 正文里已有说明。维护者如果希望这样做，可以再加。
- 需要在 sentry-docs 补一篇文档，PR 正文已提到。
- PR 模板要求填 Linear ID，外部贡献者没有，留给维护者处理。

## 如何提交
```bash
git clone https://github.com/getsentry/sentry-php && cd sentry-php
git checkout -b feat/trace-ignore-status-codes origin/master
git am /home/user/Playground/contributions/763-getsentry-sentry-php-1913/0001-feat-tracing-add-trace_ignore_status_codes-option.patch
composer install && composer check
gh repo fork --remote --remote-name fork && git push -u fork feat/trace-ignore-status-codes
gh pr create --repo getsentry/sentry-php --base master --head anyingiit:feat/trace-ignore-status-codes \
  --title "$(cat /home/user/Playground/contributions/763-getsentry-sentry-php-1913/pr_title.txt)" \
  --body-file /home/user/Playground/contributions/763-getsentry-sentry-php-1913/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`

## 独立复审（2026-10-01）
- 在 b06d0bd 上重新验证：把 `src/` 换回 master 版本后，`vendor/bin/phpunit --filter 'TransactionTest|OptionsTest'` 结果 `Errors: 14, Failures: 8`；恢复后 `OK (261 tests, 328 assertions)`。全量 `vendor/bin/phpunit`：`Tests: 1561, Skipped: 10`，全部通过。
- `php-cs-fixer fix --dry-run --diff`：0 个文件需要修改；`phpstan analyse`：`[OK] No errors`；`mago --config=mago.toml analyze`：exit 0，只有 master 已有的 3 条 warning。
- 在干净的 master worktree 上 `git apply --check` 通过；patch 与工作分支的 `git format-patch -1` 输出逐字节一致；作者 anyingiit，patch 中没有 AI 模型名。
- 已确认 sentry-laravel 的 `Tracing/Middleware.php` 会设置 `http.response.status_code` data。
- 代码本身没有发现需要修改的问题（校验器拒绝关联数组、反向区间、字符串；无 client 时直接返回；只对已采样事务生效）。
- 修正：`pr_body.md` 改为 brief 要求的 chefs-pick 格式（Description / Related issue / Checklist），仓库模板的 `resolves: #1913` 与 Linear ID 说明放进 Related issue，Reminders 中的约定提交标题放进 Checklist；更正了“非法值会使 resolver 校验失败”的说法（实际是记录 debug 日志并回退到默认值 `[]`），以及“debug log (`info`)”的含糊措辞。
