# getsotto/sotto #393 — CLI: reject out-of-range machine-token lifetimes before local setup

| 项 | 值 |
|---|---|
| Issue | https://github.com/getsotto/sotto/issues/393 |
| Tier | 新锐 |
| Labels | bug, good first issue, help wanted |
| Status | 🚧 in progress — implemented, red→green done, patch exported; running full checks |
| Duplicate-PR check | 2026-09-24: `is:pr 393` → 0 results; `is:pr expires` → only #383 (merged, introduced the feature), no open PR for this issue; no assignees/comments |

## 为什么符合“新锐”
- 31 stars / 41 forks，Rust，E2E 加密的团队 secret 同步工具（CLI + server + web/WASM），781 commits，Apache-2.0。
- 本周（2026-09-24 当天）有多位不同的人类贡献者的 PR 被合并（Maxerns 维护者、cyncui、TayfurYldz 等），维护者真实活跃。

## 问题理解（草稿）
`sotto token create --expires-in-days N` 在解析阶段接受 0、366+，服务器只允许 1–365；在非项目目录中运行时会先创建本地 store.db 然后报 "no sotto.toml"，而不是报范围错误。需要在 clap 解析阶段限制 1..=365。
