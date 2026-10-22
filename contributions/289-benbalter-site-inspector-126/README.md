# benbalter/site-inspector#126 — HSTS preload readiness 仍用 18 周阈值

| 项 | 值 |
|---|---|
| Issue | https://github.com/benbalter/site-inspector/issues/126 （good first issue） |
| Tier | 自由 |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 22:20 UTC：仓库无 open PR，issue 无评论/assignee/关联 PR |
| AI 政策 | CLAUDE.md 只限制 agent 发版/打 tag，无 AI 禁令；正文含 disclosure 段 |
| Base | `main` @ 6cd7b30 |
| DCO / CLA / 认领 | 无 / 无 / 不需要 |

## 改动
`Hsts::PRELOAD_MIN_MAX_AGE = 31_536_000`，`preload_ready?` 改用它；拆分 preload spec 并加阈值边界示例；"knows if it's enabled" 改断言 `enabled?`；CHANGELOG `## 4.0.0 / ### Fixed` 加一行（与 #131 的 #127 条目同处）。

## 验证
- rspec（LANG=C.UTF-8）191/0（6 pending，同 main）；回退 lib/ 后新示例失败。
- rubocop 无告警；`gem build` 成功。

## 如何提交
```
tools/submit_pr.sh contributions/289-benbalter-site-inspector-126 benbalter/site-inspector main hsts-preload-one-year contributions/289-benbalter-site-inspector-126/pr_title.txt contributions/289-benbalter-site-inspector-126/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
PASS：新克隆 main 干净应用，红→绿、全量、rubocop 复现，符合 hstspreload.org 要求，无竞争 PR。建议补 CHANGELOG（#131 有先例）→ 已补，并在正文加 `gem build` → 已加。
