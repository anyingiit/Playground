# stevearc/conform.nvim#877: ConformInfo 不应用 formatters_by_ft 里的 LSP filter

| 项 | 值 |
|---|---|
| Issue | https://github.com/stevearc/conform.nvim/issues/877 |
| Tier | 高星（conform.nvim，Neovim 主流格式化插件） |
| Labels | bug |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 21:45 UTC：issue 无评论、无 assignee、无关联 PR |
| AI 政策 | 无 CONTRIBUTING，.github 下无 AI 条款 |
| 外部贡献 | 最近合并的大多是外部 PR（#893、#894、#886 等） |
| Base | `master` @ 016802d |
| 提交规范 | conventional（`fix: …`），release-please 生成 CHANGELOG |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
`health.lua` 的 show_window 调 `get_format_clients({ bufnr })` 时没带 filetype 选项（name/id/filter），而 `format()` 和 `list_formatters_to_run()` 都会合并这些选项，所以 ConformInfo 显示的 LSP 和实际用来格式化的不一致。

## 改动
- `lua/conform/init.lua`：新增 `---@private` 的 `M.list_lsp_format_clients(bufnr)`，构造选项的方式与 `list_formatters_to_run` 相同。
- `lua/conform/health.lua`：改用它，并删掉不再使用的 `lsp_format` require。
- 新增 `tests/health_spec.lua`。

## 验证
- 红：只回退 lua/，新用例失败（显示 `LSP: lua_ls, other_ls`）。
- 绿：health_spec 通过；全量 `./run_tests.sh`（nvim 0.12.6）只有 3 个依赖 treesitter parser 的用例失败（fuzzer、injected inline.ts、runner e2e），干净 master 上同样失败（parser 下载 403）。
- `luacheck lua tests` 干净；stylua v2.1.0 对改动文件 `--check` 干净。
- 说明：测试需要 nvim 0.12（nvim-treesitter main 分支要求），0.11 跑不起来。

## 如何提交
```
tools/submit_pr.sh contributions/342-stevearc-conform.nvim-877 stevearc/conform.nvim master fix-877-info-lsp-filter contributions/342-stevearc-conform.nvim-877/pr_title.txt contributions/342-stevearc-conform.nvim-877/pr_body.md
```

## 独立复核
复核时间 2026-10-22，仓库 `/home/user/work/conform.nvim`，分支 fix-877 @ 4319b74（base master @ 016802d），nvim 0.12.6。

- **Issue**：用 WebFetch 看了 #877，状态 open，无评论、无关联 PR。报告者的分析（health.lua 调 `get_format_clients` 时只传 bufnr）和本修复对得上。
- **正确性**：`list_lsp_format_clients` 用的是 `get_opts_from_filetype(bufnr)`，和 `format()`、`list_formatters_to_run()` 是同一个来源，所以 `formatters_by_ft` 写成函数的情况、复合 filetype、`"_"` 兜底都会处理。`"*"` 在 `format()` 里本来就不参与选项合并（setup 时还会对它报警），这里也不参与，两边一致。和 `list_formatters_to_run` 不同的是没有合并 `default_format_opts`，但 `format()` 从 `default_format_opts` 只取 timeout_ms/lsp_format/quiet/stop_after_first，不取 id/name/filter，所以对客户端列表没有影响，不算偏差。health.lua 是在打开浮窗之前调用这个函数的，当前 buffer 仍是原 buffer，其余逻辑没动，ConformInfo 没看到回归。删掉的 `lsp_format` require 确实没有别的地方用到。
- **`---@private` 和文档生成**：init.lua 里已经有 4 个同样标了 `---@private` 的 `M.*` 函数（list_formatters_for_buffer、resolve_formatters、format_lines、get_formatter_config），先例充分。我 clone 了 stevearc/nvim_doc_tools，在仓库副本上跑了 `python3 scripts/main.py generate`，README.md 和 doc/ **没有变化**，不需要重新生成。
- **红→绿**：修复已经提交，`git stash push lua` 没有东西可存，所以改用 `git checkout 016802d -- lua` 回退 lua/。回退后 health_spec 失败（health_spec.lua:24 断言失败）；`git checkout HEAD -- lua` 恢复后通过（1/1）。
- **全量测试**：`./run_tests.sh` 只有 fuzzer formats correctly、injected formatter inline.ts、runner e2e sets the correct output 这 3 个失败。把 lua/ 换成 master 版本后，这 3 个照样失败，日志里能看到 parser 下载 403，和本改动无关。
- **lint**：`luacheck lua tests --formatter plain` 退出码 0；stylua 2.1.0 对 3 个改动文件和整个 lua/、tests/ 跑 `--check` 都干净。
- **Patch**：`git format-patch -1 HEAD --stdout` 和包里的 patch 逐字节一致。author 和 committer 都是 anyingiit <49945850+anyingiit@users.noreply.github.com>，提交信息里没有 Co-Authored-By。
- **AI 名称**：在整个包里 grep opus/sonnet/haiku/gpt/anthropic/gemini，没有命中。"Claude" 只出现在 pr_body.md 的披露段里（Claude Code 工具名）。
- **pr_body.md**：内容准确，没有夸大，还写明了传给 `format()` 的选项 ConformInfo 无法知道。披露段在。"the same way `list_formatters_to_run()` builds the options" 这句在 id/name/filter 上成立（见上），可以接受。
- 复核结束时仓库还在 fix-877，工作区干净（.testenv 是未跟踪目录）。

结论：PASS
