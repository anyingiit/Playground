# microsoft/go-mssqldb #476 — Bulk copy: nil into NOT NULL fixed-length column desyncs the row

| 项 | 值 |
|---|---|
| Issue | https://github.com/microsoft/go-mssqldb/issues/476 |
| Tier | 自由 |
| Labels | (none) |
| Status | ⏭ skipped — issue 作者已有本地补丁并主动提出开 PR（软认领） |
| 重复 PR 检查 | 2026-10-01: issue open、无 assignee、无评论；/pulls?q=476 与 bulk/nil 关键词搜索均无相关 PR |

## 跳过原因

- Issue 由 @saelen 于 2026-09-25 提交，正文末尾明确写道："We run a local patch that does this and returns a typed error, so callers can tell this case apart. I'm happy to open a PR if that approach works for you."
- 也就是说，报告者手里已经有可用补丁，正在等维护者对方案表态后自己提 PR。距今仅 6 天，维护者尚未回复。我们此时再提一个实现会和原作者的 PR 撞车，不礼貌，也可能浪费维护者的时间，所以按 brief 第 3 条（已被认领则跳过）处理。
- 其他检查都通过了：issue open、无 assignee、无评论；/pulls?q=476 与关键词搜索均无相关 PR；仓库对 AI 很友好（有 AGENTS.md/CLAUDE.md/copilot-instructions），没有禁止 AI 贡献；审计通过（见 AUDIT.md）。
- 如果之后维护者回复，而原作者在约 2–3 周后仍未提 PR，可以重新考虑这个 issue：修复点在 `bulkcopy.go` 的 `makeRowData` 中，在调用 `makeParam` 之后，若 `param.buffer` 为空且列类型是定长类型（`typeInt1/Bit/Int2/Int4/Int8/Flt4/Flt8/Money/Money4/DateTime/DateTim4`），就报错并带上列名；可以用不连 SQL Server 的单元测试覆盖（构造 `Bulk{cn:&Conn{sess:&tdsSession{}}}` 和 `bulkColumns`，并给 `ti.Writer` 赋 `writeFixedType`）。
