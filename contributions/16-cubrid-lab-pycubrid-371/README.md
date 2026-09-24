# cubrid-lab/pycubrid #371 — validate fetchmany(size) before fetching rows

| 项 | 值 |
|---|---|
| Issue | https://github.com/cubrid-lab/pycubrid/issues/371 |
| Tier | 自由 |
| Labels | area: driver, bug, good first issue, help wanted, size: S |
| Status | 🚧 in progress — audit done, implementing |
| Duplicate-PR check | 开始时：无 fetchmany 相关 open PR（#378 是 arraysize setter 校验，不同问题）；issue 无 assignee、无认领评论 |

## Notes
- 维护者 yeongseon 提的 issue，要求 float / 负数 size 抛 ProgrammingError，sync/async parity，加回归测试。
- 仓库近期合并外部 PR（#379 tayfuryldzz、#382 varshith84）。AGENTS.md 面向 AI agent，CONTRIBUTING 无 AI 禁令。
