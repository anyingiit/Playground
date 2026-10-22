# hanami/hanami#1626 — db provider should configure gateway URLs from parent

| 项 | 值 |
|---|---|
| Issue | https://github.com/hanami/hanami/issues/1626 |
| Tier | 高星（hanami/hanami） |
| Labels | 无（维护者 timriley 2026-08 开） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~20:55 UTC：issue 无评论/assignee/关联 PR；open PR #1647 改同文件的 `ensure_database_gem`，不同 hunk，不冲突 |
| AI 政策 | 无（无 AGENTS.md / PR 模板，CONTRIBUTING 未提） |
| Base | `main` @ 6f51c41 |
| DCO / CLA | 无 |
| 需先认领 | 否 |
| 注意 | CHANGELOG 条目写的是 `(@anyingiit in #1626)`（issue 号）；仓库惯例是 PR 号，**开 PR 后把 #1626 改成 PR 号再推一次**更好 |

## 改动
`Providers::DB#configure_gateways`：slice 的某个 gateway 在 ENV 里找不到 URL 时，若 `configure_from_parent` 开启，回退到父级同名 gateway 的 URL（`parent_database_url`）。优先级 ENV > 父级；父级其他 gateway 仍不复制。URL 相同后，已有的 `apply_parent_gateway_config` 会顺带复制父 gateway 的其他配置，共用连接。正文对 issue 里的"优先级"问题给出选择和可选替代方案。

## 验证
- 新增 2 个 spec：父级显式 URL 被 slice 继承且共用 gateway、`MAIN__DATABASE_URL` 优先（改前失败）；`configure_from_parent = false` 时仍报错（回归保护）。
- spec/integration/db 60/0；全量前后失败集合一致（20 个 assets/CSP/logging/detailed errors，本地无 JS 工具链，main 上同样失败）。rubocop 无告警。
- hanami-cli 的 db 命令按 URL 分组，slice 继承父 URL 后视为同一数据库（此前这类应用直接报错）。

## 如何提交
```
tools/submit_pr.sh contributions/280-hanami-hanami-1626 hanami/hanami main db-parent-gateway-urls contributions/280-hanami-hanami-1626/pr_title.txt contributions/280-hanami-hanami-1626/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
- 新克隆干净应用；红→绿、全量（同 seed）、rubocop 复现；父级先 finalize，嵌套 slice 链式继承正确；测试环境下不重复转换 URL；hanami-cli 不会让以前能用的配置变化。
- 建议：CHANGELOG 用 PR 号 → 写进"注意"；正文说明通用 `DATABASE_URL` 仍优先于父级并给出替代方案 → 已加；第二个 spec 注明是回归保护 → 已改。结论：PASS
