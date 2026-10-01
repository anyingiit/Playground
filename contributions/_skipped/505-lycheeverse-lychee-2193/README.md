# lycheeverse/lychee #2193 — Allow opting status codes out of the retry classification

| 项 | 值 |
|---|---|
| Issue | https://github.com/lycheeverse/lychee/issues/2193 |
| Tier | 自由 (~3k stars, 活跃) |
| Labels | enhancement, good first issue |
| Status | ⏭ skipped — issue 前提在当前 main (c11d779) 上不成立：HTTP 5xx 响应本来就不会被重试，所请求的选项对 521/523/525/530 无任何效果 |
| 重复 PR 检查 | 2026-10-01: /pulls?q=2193 无相关 PR；关键词 "retry" 无相关 PR；issue 未指派、无评论认领 |
| AI 政策 | CONTRIBUTING/README/.github 中无 AI 相关限制 |

## 问题理解
新增配置 `retry_skip_status_codes` / CLI `--retry-skip-status-codes`，列出的状态码即使属于"可重试"类别（如 5xx）也不重试，但仍按失败报告。默认空，行为不变。

## 合理性判断 / 跳过原因（2026-10-01）

在 main `c11d779` 上实现了完整的 `retry_skip_status_codes`（lib `ClientBuilder` 字段 + `WebsiteChecker::retry_request` 过滤 + CLI/config + example toml）并写了 wiremock 回归测试，结果发现 issue 的前提不成立：

- `WebsiteChecker::check_default` 用 `Status::new(response, accepted)` 把非 accepted 的响应包装成 `Status::Error(ErrorKind::RejectedStatusCode(code))`。
- `impl RetryExt for ErrorKind`（`lychee-lib/src/retry.rs:84`）对 `RejectedStatusCode` 只在 `429 TOO_MANY_REQUESTS` 时返回 `true`；`reqwest_error()` 分支只在网络/超时错误时出现（代码里没有用 `error_for_status`）。
- 因此 `impl RetryExt for StatusCode`（5xx/408/429 → true）对网站检查的重试循环实际上只有 429 生效；它另外只用于 `HostPool::cache_result` 决定是否放进内存缓存。
- 实测：`max_retries(3)` + wiremock 返回 `500` 并 `.expect(4)` → **只收到 1 次请求**（`Expected == 4, matched 1`）。我的改动只会减少重试，所以 base 上同样是 1 次；521 同理不会被重试。

结论：issue 想要“让 521/523/525/530 不消耗重试预算”，但这些状态码在当前代码里本来就不重试；新选项只会对 429 有影响，与 issue 动机无关。没有可以 red→green 的回归测试（"不重试"在 base 上已经成立），按规则跳过，不做 patch。

### 可选的后续（需要人判断，不在本次范围）
提交者可以在 issue 下留言指出上述事实（`retry.rs` 中 `ErrorKind::should_retry` 只对 `RejectedStatusCode(429)` 返回 true，所以 5xx 响应并未被重试），询问维护者：是 5xx 本应被重试（`retry.rs` 的单测 `assert!(StatusCode::INTERNAL_SERVER_ERROR.should_retry())` 暗示了这个意图）而这是个 bug，还是 issue 可以关闭。等维护者给出方向后再动手。

## 验证记录
- audit：见 AUDIT.md（安全）
- `cargo test -p lychee-lib --lib retry`（含新加的探测测试）→ 500 只请求 1 次，证明 5xx 不重试
- 未生成 patch；工作目录与 target 已删除
