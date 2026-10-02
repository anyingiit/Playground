# modelcontextprotocol/go-sdk#1328 — LoggingTransport drops session state updates (SKIPPED)

| 项 | 内容 |
|---|---|
| Issue | https://github.com/modelcontextprotocol/go-sdk/issues/1328 |
| Tier | 新锐 |
| Labels | 无（未标 help wanted / good first issue） |
| Status | ⏭️ skipped — 已被 issue 作者认领（作者称修复与回归测试已就绪，等待维护者确认方案后自己提 PR） |
| Base 检查 | main @ 53effc0 (2026-10-01) |
| Duplicate-PR check (2026-10-01 23:30 UTC) | `pulls?q=1328`：无相关 PR；关键词 `LoggingTransport`：#1267（open，DropResponse，会在 loggingConn 增加相邻 forwarder，但不修本问题）；`sessionUpdated`：#1274/#1199/#1107 已合并、#1266 open，均不涉及 loggingConn 转发 |

## 跳过原因

1. **已被认领**：issue 于 2026-10-01 由 Zhuoxi2000 提出，正文最后写明
   "I have this fix ready, with regression tests that fail on main and pass with it. I can send it as a PR if this approach works for you."
   作者已经有完整修复（重命名为 `clientSessionUpdated` / `serverSessionUpdated` 并让 `loggingConn` 转发，含 `propagateCancellation`），只是在等维护者认可方案。再提一个竞争 PR 属于重复劳动、也不礼貌。
2. **仓库流程**：CONTRIBUTING.md 规定未标 'Help Wanted' 的 issue 应先在 issue 上询问并等待确认再贡献；本 issue 无标签、无维护者回复。
3. 合理性本身没问题（`loggingConn` 未实现内部 `clientConnection`/`serverConnection` 接口，确实导致包装后行为变化），AI 政策方面 CONTRIBUTING.md 无禁令（仓库有 AGENTS.md）。仅因认领与流程原因跳过。

未运行任何仓库代码（未构建/测试），因此无 AUDIT.md；浅克隆已删除。
