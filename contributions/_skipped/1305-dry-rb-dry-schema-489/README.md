# dry-rb/dry-schema#489 — I18n.available_locales is mutated

| 项 | 值 |
|---|---|
| Issue | https://github.com/dry-rb/dry-schema/issues/489 |
| Tier | 自由 |
| Labels | bug, help wanted |
| Status | ⏭️ skipped — duplicate: open PR #519 already fixes this issue |
| Duplicate-PR check | 2026-10-01 23:02 UTC: `pulls?q=489` → **open PR #519 "Preserve configured I18n available locales"** by sjh9714 (2026-09-01), linked from the issue, references #489 |

## 跳过原因

复核时发现 issue 页面已链接 PR **#519**（https://github.com/dry-rb/dry-schema/pull/519，open，2026-09-01，作者 sjh9714）。
该 PR 做的正是本任务计划的修复：在 `lib/dry/schema/messages/i18n.rb` 存储翻译时不再修改用户配置的
`I18n.available_locales`，并在存储后清理 I18n 的 locale 缓存，附带回归测试。PR 尚无 review。
scout 阶段用 `available_locales` 关键字搜索未命中（PR 标题用的是 "available locales"，无下划线），因此漏判。

按 CONTRIBUTION_BRIEF 硬性要求 3（No duplicates），不再实现，未 clone、未运行任何代码（因此无 AUDIT.md / patch）。

其他检查（供参考）：issue open、未分配、无评论；labels 页面无 AI 相关规定。
