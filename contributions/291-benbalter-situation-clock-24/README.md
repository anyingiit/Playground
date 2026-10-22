# benbalter/situation-clock#24 — Unix 时间小字号只对名为 "EPOCH" 的时钟生效

| 项 | 值 |
|---|---|
| Issue | https://github.com/benbalter/situation-clock/issues/24 （good first issue） |
| Tier | 自由 |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 22:45 UTC：无 open PR，issue 无评论/assignee/关联 PR |
| AI 政策 | CLAUDE.md 只说推 gh-pages 即部署、开 PR 安全；无 AI 禁令；正文含 disclosure 段 |
| Base | `gh-pages` @ b9826c7 |
| DCO / CLA / 认领 / CHANGELOG | 无 / 无 / 不需要 / 仓库无 |

## 改动
`assets/style.css`：`.epoch .time` → `.clock[data-timezone="EPOCH"] .time`（一行）。

## 验证
- `npm test`、`npm run lint`、`npm run build` 通过。
- `epoch_check.cjs`（本目录，不随补丁提交）：在构建产物里加 "Unix"/EPOCH 和 "EPOCH"/UTC 两个时钟，用 headless Chromium 量 `.time` 字号。改前 FAIL（64px/40px），改后 PASS（40px/64px），默认时钟不变。

## 如何提交
```
tools/submit_pr.sh contributions/291-benbalter-situation-clock-24 benbalter/situation-clock gh-pages epoch-font-by-timezone contributions/291-benbalter-situation-clock-24/pr_title.txt contributions/291-benbalter-situation-clock-24/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
PASS：新克隆干净应用，test/lint/build 通过，红→绿复现，三条验收标准满足，选择器优先级无冲突，script.ts/README 无需改。建议正文说明按名字生成的 class 仍保留 → 已补。
