# DioxusLabs/taffy #835 — Document `known_dimensions` vs `available_space` on `LayoutInput`

| 项 | 值 |
|---|---|
| Issue | https://github.com/DioxusLabs/taffy/issues/835 |
| Tier | 高活跃高Star |
| Labels | documentation, good first issue |
| Status | 🚧 in progress — audit |

## 候选排除记录（本次搜索中放弃的候选）
- lycheeverse/lychee #2143: 两个 PR (#2144, #2233) 被关闭，维护者要"从根本上移除 `error:` sentinel"，设计由维护者主导。
- lycheeverse/lychee #2193: 前提不成立——在 HEAD (2c1fb3a) 上 lychee 实际**不会**重试 5xx（只重试 429/超时/部分网络错误），
  用本地 HTTP server 实测 521/500/503 各只请求 1 次、429 请求 4 次。原因：`Status::Error(RejectedStatusCode(_))` 的
  `should_retry` 只对 429 返回 true（d22d188, 2025-05），而 `RetryExt for StatusCode` 里的 5xx 规则只用于缓存判断。
  可作为 issue 评论草稿提供给维护者，不适合直接提 PR。
- rust-lang/*（LLM policy 需预先获得 reviewer 同意）、gleam、typst、fish-shell、PyO3/pyrefly/diesel/zizmor（good first issue 禁 AI）、
  astral-sh/*、biome、harper、topgrade、sharkdp/fd（要求 PR 描述由人类撰写）→ 跳过。
- jj #9375（设计不明确）、oxc #22955（剩余规则均被阻塞）、git-cliff #1638/#1579、onefetch #1527、lldap #1202/#994、
  arrow-rs #11032、pixi #5672、burn #4312/#544、turso 等 → 已有 PR 或已完成。
