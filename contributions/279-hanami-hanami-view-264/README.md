# hanami/hanami-view#264 — clear error for named scopes without scope_namespace

| 项 | 值 |
|---|---|
| Issue | https://github.com/hanami/hanami-view/issues/264 |
| Tier | 自由（hanami） |
| Labels | help-wanted（维护者 timriley 开，2025-03） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~21:00 UTC：issue 无评论/assignee/关联 PR；5 个 open PR 都不涉及 scope |
| AI 政策 | 无（无 AGENTS.md，CONTRIBUTING 未提） |
| Base | `main` @ 7a529ff |
| DCO / CLA | 无 |
| 需先认领 | 否 |
| 注意 | CHANGELOG 条目写的是 `(@anyingiit in #264)`（issue 号）；该仓库惯例写 PR 号，**开 PR 后可把 #264 改成 PR 号再推一次**（同 169 的做法），不改也可接受 |

## 改动
`ScopeBuilder.resolve_scope_class` 在用 `scope_namespace` 前检查，未配置时抛 `Hanami::View::UndefinedConfigError`（"no +scope_namespace+ configured"），与 `paths`/`template` 未配置时一致；CHANGELOG Unreleased/Fixed 一行。

## 验证
- scope_builder_spec 4/0；回退 lib/ 后新例子失败（得到 NoMethodError）。
- 全量 494/2，2 个 tilt_spec 失败在 main 上同样存在。rubocop 无告警。

## 如何提交
```
tools/submit_pr.sh contributions/279-hanami-hanami-view-264 hanami/hanami-view main scope-namespace-error contributions/279-hanami-hanami-view-264/pr_title.txt contributions/279-hanami-hanami-view-264/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
- 新克隆干净应用；红→绿、全量、rubocop 复现；UndefinedConfigError 选择合理；缓存块内抛错不会缓存；hanami 框架侧只有在无 views/scopes 时不设 namespace，此前本就崩溃，不会破坏现有行为。
- 建议：CHANGELOG 改用 PR 号 → 写进上方"注意"。结论：PASS
