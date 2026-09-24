# celler-cache/celler #75 — Validate existence of config file after login

| 项 | 值 |
|---|---|
| Issue | https://github.com/celler-cache/celler/issues/75 |
| Tier | 自由 |
| Labels | enhancement, good first issue, help wanted |
| Status | 🚧 in progress — audit done, implementing |
| 重复 PR 检查 | 无关联 PR（PR 列表中无 login/config 相关 PR），无 assignee，无评论 |

## 笔记
- `celler login` 通过 `ConfigWriteGuard` 的 `Drop` 保存配置，保存失败只 `tracing::error!`，命令仍然返回成功。
