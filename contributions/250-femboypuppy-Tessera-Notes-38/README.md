# femboypuppy/Tessera-Notes#38: Emoji picker: Enter before the emoji data loads does nothing

| 项 | 值 |
|---|---|
| Issue | https://github.com/femboypuppy/Tessera-Notes/issues/38 |
| Tier | 自由（TypeScript） |
| Labels | good first issue, area: shell |
| Status | ✅ ready，独立复核 PASS（未提交） |
| 重复 PR 检查 | 2026-10-22 20:30 UTC：`repo:femboypuppy/Tessera-Notes emoji` PR 搜索 → 0；issue 无评论、无 assignee、Development 为空 |
| AI 政策 | 项目本身由 Claude Code agent 构建（BUILT_WITH_AGENTS.md），无禁 AI 条款；已合并过外部贡献（#77、#79） |
| Base | `main` @ 2f0281d |
| DCO / CLA | 均无 |
| 需先认领 | **是（建议）**：CONTRIBUTING "Pick a first issue" 第 2 步要求先评论 "I'd like to take this"。提交前在 issue 下评论认领（注明 PR 已就绪），之后再开 PR |
| commit | Conventional Commits，仓库有 commit-msg 钩子校验；无 trailer |

## 问题理解
首次打开 emoji picker 时数据（动态 import 的 emojibase）还在加载，`results` 为 null。此时在搜索框输入 "rocket" 立刻回车，Enter 处理器取 `results?.[0]` 为空，什么也不做。

## 改动
- `packages/ui/src/components/emoji-picker.tsx`：
  - 加载中（无 data、未失败、query 非空）按 Enter 时记下 `pendingEnter`（ref）。
  - effect 在 `results` 出来后选第一个并清掉标记。
  - 再次输入（onChange）会清掉标记。
  - `pick` 改成 `useCallback([onSelect])`，满足 `exhaustive-deps`。
- `packages/ui/src/components/components.test.tsx`：2 个测试：加载中回车选中 🚀（仅一次）；回车后改查询则不选。

## 验证
- 红：只回退 emoji-picker.tsx，第 1 个测试失败（第 2 个是守卫，原本也通过）。
- 变异：删掉 onChange 里清标记那行，第 2 个测试失败。
- 绿：EmojiPicker 3/3；`pnpm test` 全量 184 文件 / 1590 测试通过；`packages/ui` typecheck 通过；改动文件 eslint `--max-warnings 0` 与 prettier 通过。
- CHANGELOG 发版时由 commit 历史生成，不手改。

## 如何提交
1. 在 issue #38 评论认领：`I'd like to take this — I have a small fix with a test ready and will open a PR shortly.`
2. `tools/submit_pr.sh <本目录> femboypuppy/Tessera-Notes main fix/emoji-enter-while-loading pr_title.txt pr_body.md`（不加 `--signoff`/`--trailer`）

## 独立复核（2026-10-22 21:00 UTC）
PASS。复核者在新克隆上确认：红→绿、变异结论成立；全量 `pnpm test`（184/1590）、`pnpm typecheck`、`pnpm lint` 全部通过；commit-msg 钩子通过。逐项核对了边界情况（加载失败、加载前卸载、清空查询、连按 Enter、父组件传内联 onSelect、StrictMode），并用临时测试跑过其中四项，均无问题。已采纳：第二个测试补上"加载中"前置断言；检查项改写为全量命令都通过；键盘一项注明只有 jsdom 测试覆盖；测试步骤提示用 DevTools 节流。
