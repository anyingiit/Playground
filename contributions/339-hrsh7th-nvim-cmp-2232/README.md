# hrsh7th/nvim-cmp#2232: 文档窗口压在补全菜单上

| 项 | 值 |
|---|---|
| Issue | https://github.com/hrsh7th/nvim-cmp/issues/2232 |
| Tier | 高星（nvim-cmp，Neovim 主流补全插件） |
| Labels | bug |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 21:25 UTC：issue 无评论、无 assignee、无关联 PR。报告者只在自己的 dotfiles 仓库（MattesMrzik/nvim 111bd02）放了一个 monkey-patch 绕过，没有向上游提 PR。最近的 PR 列表里没有相关 PR |
| AI 政策 | 仓库无 CONTRIBUTING，.github 下无 AI 条款 |
| Base | `main` @ 2ffe79f |
| 提交规范 | 仓库用 release-please，提交信息格式与现有 `fix(#1303): …` 一致 |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
`custom_entries_view.open` 只在光标位于右半屏时把菜单左移。光标在左半屏但菜单过宽时，nvim 自己把浮窗挤回屏内，但 `entries_win.style`（即 `info()`）仍是请求的 col/width。docs_view 按 `info()` 算左右空间，于是把文档窗放到了实际被菜单占着的位置。

## 改动
- `lua/cmp/view/custom_entries_view.lua`：去掉"右半屏"条件，只要放不下就执行原有的左移/收窄逻辑。放得下的菜单不受影响，右半屏的行为不变。
- 新增 `lua/cmp/view/custom_entries_view_spec.lua`，3 个用例。
- 没有采用 issue 里提的 `nvim_win_get_position`，因为无 UI 时 nvim 不移动浮窗（已用 headless 探针确认），没法测试。现在的改法让存储的几何和实际绘制的一致，可以直接做单测。

## 验证
- 绿：`VUSTED_NVIM=nvim vusted ./lua`（nvim 0.11.4）→ Success: 76（基线 73，加 3 个新用例）。
- 红：只回退 src，新用例 1、2 失败，用例 3 通过。
- `luacheck lua` 0 warnings；stylua v2.1.0 `--check` 对改动文件干净（CI 也会自动跑 stylua 格式化）。
- 未跑：nightly nvim（CI 用 nightly）。

## 如何提交
```
tools/submit_pr.sh contributions/339-hrsh7th-nvim-cmp-2232 hrsh7th/nvim-cmp main fix-2232-menu-clamp contributions/339-hrsh7th-nvim-cmp-2232/pr_title.txt contributions/339-hrsh7th-nvim-cmp-2232/pr_body.md
```

## 独立复核
- 读了 issue 原文（WebFetch）：场景是条目比编辑器还宽、Neovim 把菜单挤到左边，但 `info()` 仍返回请求的几何，期望是放不下时不画文档窗。改动对准了这个根因。
- 代码推演：issue 场景（无边框、列 0、超宽条目）修复后 `info()` 为 col=0、width=columns-1，docs_view 算出 right_space=0、left_space=-1，文档窗关闭，符合 issue 的期望行为。左半屏溢出（列 20、宽 65、80 列）时菜单左移到 col 14，文档窗只会放在真正空着的左侧。右半屏的路径与原来完全一致；滚动条（无边框时 +1 列）由原有的 `-1` 余量覆盖。
- 边框：临时写了一个 `border='rounded'` 的 spec（超宽、左半溢出、能放下、右半能放下、右半溢出 5 种），全部 `col+width <= columns`，且存储的 col 与 `nvim_win_get_position` 一致；跑完已删除。
- col_offset 在夹紧之后才加，正值时仍可能越界，但这是右半屏原有的行为，不是本改动引入的回归。
- 小细节（不影响结论）：条件是 `<=`，所以在左半屏"刚好贴到最右一列"的菜单现在也会左移 1 列，与右半屏原有行为一致；PR 正文"能放下的菜单不受影响"在这个边界上略有简化。
- 红→绿：`git checkout main -- lua/cmp/view/custom_entries_view.lua` 后新 spec 用例 1、2 失败、用例 3 通过；恢复后通过。仓库已还原为 fix-2232、工作区干净。
- 全量 `vusted ./lua`：Success 76；`luacheck lua`：0 warnings / 0 errors；stylua 2.1.0 `--check` 对两个改动文件干净。
- `git format-patch -1 HEAD` 与包内 patch 逐字一致；作者和提交者都是 anyingiit <49945850+anyingiit@users.noreply.github.com>，无 Co-Authored-By。
- 包内除 pr_body.md 披露段的 "Claude Code" 外没有任何模型名。pr_body.md 描述准确、不夸大，含 motivation/disclosure 段。

结论：PASS
