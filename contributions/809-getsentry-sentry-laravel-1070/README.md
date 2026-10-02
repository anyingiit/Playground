# getsentry/sentry-laravel #1070 — Add class_serializer for `Illuminate\Http\Client\Response`

| 项 | 值 |
|---|---|
| Issue | https://github.com/getsentry/sentry-laravel/issues/1070 |
| Tier | 自由 |
| Labels | Errors, Good First Issue, Improvement, Laravel |
| Status | ✅ ready（已独立复审；phpstan 未在本地运行，见下） |
| 重复 PR 检查 | 2026-10-01：`pulls?q=1070` 0 结果；issue 页面没有 linked PR、assignee 和评论。 |
| Base | `master` @ b6a56ed |

## 问题理解
异常的栈帧参数或变量里如果有 Laravel HTTP client 的 `Response` 对象，Sentry 只显示类名，看不到状态码、URL 等信息。sentry-php 提供 `class_serializers` 选项，可以给特定类注册序列化函数。issue 希望 SDK 默认给 `Illuminate\Http\Client\Response` 注册一个。

## 合理性判断
- issue 由维护者 Litarnus 创建，带 Good First Issue 标签，没有人认领。
- 实现方式：只加一个默认的 class serializer，不新增配置项，用户自己配置的同类 serializer 优先，符合 AGENTS.md 中“尽量不加新配置”的要求。
- PII：headers 和完整 URL（含 query、userinfo）只在 `send_default_pii` 开启时输出；body 一律不输出，原因是体积大、可能含敏感数据，读取还可能耗尽不可 seek 的 stream。PR 正文已说明，维护者需要的话可以再加。

## 改动
- 新增 `src/Sentry/Laravel/Serializer/HttpClientResponseSerializer.php`（@internal，invokable，兼容 PHP 7.2），输出以下字段：
  - `status`、`reason`
  - `url`：只在有 transferStats 时输出，PII 关闭时去掉 userinfo、query 和 fragment
  - `content_type`
  - PII 开启时另外输出 `headers`，展平成字符串，避免被 serializer 的 max depth 截断
- `src/Sentry/Laravel/ServiceProvider.php` 的 `configureAndRegisterClient()`：先用 `class_exists` 检查类是否存在；用户没有为该类配置 serializer 时，把默认 serializer **追加到用户列表末尾**（sentry-php 按注册顺序取第一个 `instanceof` 匹配的 serializer，追加在后面才不会盖掉用户为父类或接口如 `ArrayAccess` 注册的 serializer）；用户配置的值不是数组时不做处理。
- 新增测试 `test/Sentry/Features/HttpClientResponseSerializerTest.php`（6 个用例，含“用户为接口注册的 serializer 优先”）。
- 按 AGENTS.md 的要求没有改 CHANGELOG.md 和 README.md；PR 正文给出了 release note 建议。

## 验证（PHP 8.3.6，composer 解析到 Laravel 13 / Testbench 11 / PHPUnit 11.5）
- Red（`git show HEAD~1:src/Sentry/Laravel/ServiceProvider.php > src/Sentry/Laravel/ServiceProvider.php`，还原到 master 的 ServiceProvider）：`vendor/bin/phpunit --filter HttpClientResponseSerializerTest` → Tests: 6, Errors: 1, Failures: 3。两个“用户 serializer 优先”的用例在改动前本来就通过，属于预期（它们防的是回归）。
- Green：同一命令 → OK (6 tests, 12 assertions)
- 全量 `vendor/bin/phpunit` → OK (247 tests, 728 assertions)。13 个 PHPUnit Deprecations 在无关测试里也有，属于既有情况。
- `vendor/bin/php-cs-fixer fix --verbose --diff --dry-run`（即 `composer cs-check`）→ Found 0 of 66 files that can be fixed
- **没有运行 `composer phpstan`**：phpstan/phpstan 只有 dist 包，下载走 api.github.com zipball，在本环境被代理 403 拦截。用 git 拉取 phpstan.phar 的操作也被权限策略拒绝。安装时用临时的 composer.local.json 去掉了 phpstan，其余依赖用 `--prefer-source` 装好。**提交前请在本地跑一次 `composer phpstan`。**
- 没有在 PHP 7.2 和低版本 Laravel 上实测；代码只用了 7.2 可用的语法（无 typed property、箭头函数等），`transferStats` 和 `effectiveUri` 都做了 isset 或 method_exists 检查。

## 需要提交者注意
- 独立复审（2026-10-01）：把默认 serializer 从 `array_merge(默认, 用户)`（默认排在最前，会抢先匹配、盖掉用户为父类/接口注册的 serializer）改成追加在用户列表末尾，并补了对应测试；提交信息标题去掉了 `(#1070)`（getsentry squash merge 会自动追加 PR 号），改为正文 `Closes #1070`。已在 master 新 worktree 上验证 `git am` 可干净应用。
- AGENTS.md 不禁止 AI，PR 正文已披露。不需要 DCO 和 Signed-off-by。
- **validate-pr bot**：getsentry 的 validate-pr 会检查超过 100 行的社区 PR（本 PR 225 行）。要求 PR 作者在关联 issue 下参与过讨论（创建或评论），而且有维护者参与过。不满足时 bot 只留一条提示评论，不会关闭 PR。建议提交前先在 #1070 下留言表示要做这个（维护者 Litarnus 是 issue 作者，满足“维护者参与”这一条）。
- PR 标题要用 conventional commit 格式（`feat:`），已写在 pr_title.txt。
- 请在本地补跑 `composer phpstan`。如果出现新的报错，多半在 `$response->transferStats` 的属性访问或 `__invoke($response)` 的参数类型上，可以视情况加 `@var` 注释或调整 baseline。

## 如何提交
```bash
git clone https://github.com/getsentry/sentry-laravel && cd sentry-laravel
git checkout -b feat/http-client-response-serializer origin/master
git am /home/user/Playground/contributions/809-getsentry-sentry-laravel-1070/0001-feat-Add-class-serializer-for-Illuminate-Http-Client.patch
composer install && composer check
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/809-getsentry-sentry-laravel-1070 getsentry/sentry-laravel master feat/http-client-response-serializer contributions/809-getsentry-sentry-laravel-1070/pr_title.txt contributions/809-getsentry-sentry-laravel-1070/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
