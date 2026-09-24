# uutils/coreutils #9060 — who/unix.rs: improve code coverage

| 项 | 值 |
|---|---|
| Issue | https://github.com/uutils/coreutils/issues/9060 |
| Tier | 高活跃高Star |
| Labels | U - who, good first issue |
| Status | 🚧 in progress — audit ✅, commit + patch exported, running full checks |
| Duplicate-PR check | 无 assignee、无评论、无 linked PR；`who repo:uutils/coreutils is:open` 的 open PR 为 #14495(Windows 实现)/#9092(pid header)/#13389(stdout 写错误)/#11039(PID 存活)，均非覆盖率测试 |

## 选题过程（原目标被跳过）
- 原目标 servo/rust-smallvec#673（`TaggedLen` → `LocatedLength`）：issue 本身无人认领、无 PR，但仓库 `AGENTS.md` 与 Servo 贡献指南（book.servo.org → AI contributions）明确禁止 LLM 生成的代码/PR。按 brief 第 2 条（合理性判断需参考 AGENTS/CONTRIBUTING）**跳过整个 servo/***。
- 备选排查：astral-sh/ruff（AI_POLICY 禁止自主 agent 贡献、PR 正文须本人撰写）、clap（需先在 issue 获许可）、nushell（AGENTS.md 拒绝 agent PR）、ratatui（允许 AI 但 good-first-issue 已有 PR 或已完成）、tokio（无合适 easy issue）。
- 选定 uutils/coreutils：CONTRIBUTING “AI policy” 明确允许 AI 辅助贡献（需本人理解每一行、不得源自 GNU 代码、PR 描述简短且用自己的话）。
