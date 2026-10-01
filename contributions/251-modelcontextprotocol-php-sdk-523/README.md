# modelcontextprotocol/php-sdk #523 — Let a framework integration opt out of the HTTP edge middleware without a warning

| 项目 | 内容 |
|---|---|
| Status | ✅ ready — 补丁、测试（red→green）、cs/phpstan/unit 全部完成 |
| Issue | https://github.com/modelcontextprotocol/php-sdk/issues/523 |
| Tier | 新锐 |
| Labels | 无 |
| 重复 PR 检查 | 2026-10-01：`is:pr 523` 0 结果；open PR 中搜 `middleware` 只有 #492（PHPStan level 8，无关）；issue 无 assignee、无评论认领 |
| Base | `main` @ 3175614 |

## 问题理解
`StreamableHttpTransport` 在 `middleware: []` 时每次构造都会 log warning。Drupal 的 mcp_server 是**故意**传空列表（CORS 由 Drupal `cors.config` 处理，Host 校验由 `trusted_host_patterns` 处理），PHP 每个请求都新建 transport → 每个 MCP 请求一条 warning。issue 要求提供显式 opt-out（构造参数或约定值），同时保留“意外传空列表”时的警告。另外警告文本里的 “protocol version validation” 已过时：handshake 时代的请求总是走 `handshakeMiddleware()`。

## 合理性判断
Issue 由下游集成作者提出，理由具体；改动纯增量（新增带默认值的尾参数），符合 Symfony BC 承诺。项目 CONTRIBUTING / CLAUDE.md 没有禁止 AI 贡献的条款（仓库本身就带 CLAUDE.md）。

## 改动
- `src/Server/Transport/StreamableHttpTransport.php`：构造函数新增尾参数 `bool $warnOnEmptyMiddleware = true`；为 false 时空列表不再 warning；警告文本去掉 “protocol version validation”，并提示新参数。
- `tests/Unit/Server/Transport/StreamableHttpTransportTest.php`：新增 `testEmptyMiddlewareListWithOptOutDoesNotWarn`（logger `never()->warning`，且确认默认中间件依旧被禁用）。原有“空列表会 warning”测试保持不变并通过。
- `docs/run/http.md`：补充 opt-out 说明与示例。
- `CHANGELOG.md`：0.9.0（未发布，最新 tag 为 v0.8.1）下新增一条。

## 验证（PHP 8.3.6）
- Red（未改 src）：`vendor/bin/phpunit --filter EmptyMiddleware tests/Unit/Server/Transport/StreamableHttpTransportTest.php` → `Error: Unknown named parameter $warnOnEmptyMiddleware`（Tests: 2, Errors: 1）
- Green：`vendor/bin/phpunit tests/Unit/Server/Transport/` → OK (156 tests, 386 assertions)
- `vendor/bin/phpunit --testsuite unit` → OK (1583 tests, 4 skipped)
- `vendor/bin/phpunit tests/Integration/DualEraEndpointTest.php` → OK (9)；`tests/Integration/HandshakeTest.php` → OK (13)；`--testsuite examples` → OK (5)
- `vendor/bin/php-cs-fixer fix --dry-run --diff`（make cs 等价，只检查）→ 0 of 575 files
- `vendor/bin/phpstan --memory-limit=-1` → No errors
- 未通过/未跑：`--testsuite inspector` 需要 `npx @modelcontextprotocol/inspector@2.2.0`，本环境无法下载 → 全部 error；在 base（stash 掉改动）上同样 8/8 error，与本改动无关。完整 `--testsuite integration` 在 300s 内未跑完（机器共享负载），只跑了与 HTTP transport 相关的两个文件。
- 环境备注：本环境 api.github.com/codeload 被拦，composer 用 `--prefer-source` + `use-github-api false` 安装，phpstan 用本地 clone 的 path dist（只影响本地环境，补丁不含 composer.lock）。

## 需要提交者注意
- 提交风格：标题 `[Server] ...`（仓库惯例），不需要 DCO，也没有 AI trailer 要求。
- PR 正文已包含使用 Claude Code 的披露段落。
- 维护者可能更倾向别的 API 形式（例如常量/哨兵值而不是 bool 参数），按 review 意见调整即可。

## 如何提交
```bash
git clone https://github.com/modelcontextprotocol/php-sdk.git && cd php-sdk
git checkout -b server-empty-middleware-opt-out origin/main
git am /path/to/contributions/251-modelcontextprotocol-php-sdk-523/0001-*.patch
# 推到自己的 fork 后：
tools/submit_pr.sh contributions/251-modelcontextprotocol-php-sdk-523 modelcontextprotocol/php-sdk main server-empty-middleware-opt-out contributions/251-modelcontextprotocol-php-sdk-523/pr_title.txt contributions/251-modelcontextprotocol-php-sdk-523/pr_body.md
```

PR 标题：见 `pr_title.txt`；PR 正文：见 `pr_body.md`。
