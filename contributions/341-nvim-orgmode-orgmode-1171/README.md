# nvim-orgmode/orgmode#1171: 撤销 clock-out 后无法再次 clock-out

| 项 | 值 |
|---|---|
| Issue | https://github.com/nvim-orgmode/orgmode/issues/1171 |
| Tier | 高星（nvim-orgmode，约 3.5k star） |
| Labels | bug |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 21:38 UTC：issue 无评论、无 assignee；搜 "clock" 的 PR 都与此无关，没有引用 #1171 的 PR |
| AI 政策 | **允许，但要求披露**：AGENTS.md 要求 commit 带 `AI-assisted: <tool>` trailer（已加 `AI-assisted: Claude Code`）；维护者自己的提交也带这个 trailer |
| Base | `master` @ 78c9928 |
| 提交规范 | Conventional Commits，PR 模板（Summary/Related Issues/Changes/Checklist），pr_body 已按模板写；CHANGELOG 由提交自动生成 |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
clock out 后 `clocked_headline = nil`。撤销后 CLOCK 行又是运行状态，但 `update_clocked_headline` 只扫描 agenda 文件。文件不在 agenda 里时找不到，`,oxo` 就没有反应。已复现：在 agenda 文件里不会出现，在非 agenda 文件里稳定复现。

## 改动
- `lua/orgmode/clock/init.lua`：agenda 里找不到运行中的 clock 时，回退到当前 org buffer（先用 `has_running_clock_candidate` 快速过滤）。
- `tests/plenary/ui/clock_spec.lua`：新用例（非 agenda 文件：clock in → out → undo → out），结束时删掉临时文件，避免污染后续用例的 agenda 目录。

## 验证
- 红：只回退 src，新用例第 65 行失败（第二次 clock out 后 CLOCK 行仍未结束）。
- 绿：clock_spec 12/12 通过。
- 全量 `make test`：除 5 个与 uuidgen/环境相关的用例（id_spec、templates_spec×2、api_spec、hyperlink_spec）外全部通过；这 5 个在干净 master 上同样失败。
- stylua v2.1.0 对改动文件 `--check` 干净（CI 用 stylua-action）。

## 如何提交
```
tools/submit_pr.sh contributions/341-nvim-orgmode-orgmode-1171 nvim-orgmode/orgmode master fix-1171-clock-out-undo contributions/341-nvim-orgmode-orgmode-1171/pr_title.txt contributions/341-nvim-orgmode-orgmode-1171/pr_body.md
```
注意：submit_pr.sh 用 `--amend --reset-author`，会保留 commit message 里的 `AI-assisted` trailer。

## 独立复核

复核时间 2026-10-22，分支 `fix-1171` @ 47f30f1，复核后工作区干净（只临时改动过 src，已恢复）。

- **Issue**：用 WebFetch 看了 #1171。复现步骤是：打开一个新 org 文件 → `oxi` → `oxo` → `u` → `oxo` 没反应。issue 无评论、无关联 PR，和 README 的描述一致。
- **根因**：属实。`org_clock_out` 把 `clocked_headline` 置 nil，`OrgFiles:get_clocked_headline()` 只遍历 `self:all()`，也就是已发现的 agenda 文件（依赖 `_path_cache`）。我在 `tests/plenary/ui/` 下临时放了一个探针 spec，跑完已删除。结果：在 agenda 文件里按 clock in → out → undo → out 的流程，**master 源码同样能正常 clock out**，说明问题只出在不属于已加载 agenda 列表的文件上。补充一点：新用例里的临时文件其实落在上一个用例 agenda glob 的同一个目录下，只是因为它是在 load 之后创建的、不在 path cache 里，才不算 agenda 文件。所以准确的说法是"不在已加载的 agenda 文件里"，不影响结论。
- **改动正确性和副作用**（`lua/orgmode/clock/init.lua`）：
  - 回退只在 agenda 里没有运行中的 clock 时触发，而且只在 `filetype == org` 时生效。先用 `has_running_clock_candidate()` 做行扫描，再解析。
  - `load_file_sync` 对当前文件来说，一般是直接拿已加载 buffer 对应的 OrgFile，`reload` 在 changedtick 没变时直接返回。`org_clock_in` 本来就会对当前文件调用 `get_closest_headline`，所以性能开销可以忽略。
  - 探针验证：在无名 org buffer（`enew` + `ft=org`，含未结束的 CLOCK）和非 org buffer 里调用 `clock.org_clock_out` 都不报错（`current_file_path` 为空 → `is_org_file` 为假 → 返回 false）。
  - `init` 是在 `files:load()` 的 promise 回调里调用的，回退路径会同步等待当前文件，实际上当前文件通常已经加载，没发现问题。
  - clock in 现在会先结束当前文件（非 agenda）里正在跑的 clock。这和 agenda 文件的现有行为、Emacs 单一 clock 的语义一致，我认为是想要的效果。
  - 小瑕疵（不阻塞）：回退路径没有像 agenda 路径那样跳过 archive 文件。
  - 另一种更小的修法是 clock out 后保留 `clocked_headline`（`org_clock_goto` 的"most recently clocked task"提示也暗示应该保留），但那样需要处理 undo 之后 headline 对象过期的问题，也覆盖不到重启后的情况。现在的方案更稳妥。
- **红→绿**：只用 `git checkout HEAD~1 -- lua/orgmode/clock/init.lua` 回退 src，clock_spec 结果是 11 过 1 失败，失败的就是新用例（`clock_spec.lua:65`）。恢复之后 12/12 通过。分支仍为 fix-1171，工作区干净。
- **隔离性**：clock_spec 全部跑完 12/12 通过。回退 src、新用例失败时（临时文件没删掉），其余 11 个用例照样通过，说明不会污染后面的用例。小瑕疵：`vim.fn.delete` 放在断言后面，失败时不会执行，但临时目录是每个 nvim 进程独立的，影响有限。
- **全量套件**：用修复版跑了一次全量，正好 5 个失败（hyperlink id、org id uuid、api id、capture template ×2）。用 master 源码再跑一次，是同样这 5 个，再加上新用例。本机 `which uuidgen` 没有结果，所以"预先存在、和环境有关"的说法属实。
- **补丁和元数据**：`git format-patch -1 HEAD --stdout` 和包里的 .patch 逐字节一致。作者和提交者都是 `anyingiit <49945850+anyingiit@users.noreply.github.com>`。commit 里有 `AI-assisted: Claude Code` trailer，符合 AGENTS.md。在包内和 commit message 里搜了 opus/sonnet/haiku/gpt/gemini/claude，只出现 "Claude Code"。stylua 2.1.0 `--check` 两个改动文件都干净。
- **PR 文本**：标题符合 Conventional Commits。pr_body 按模板的 Summary / Related Issues（Closes #1171）/ Changes / Checklist 写，内容和我的实测一致（12 个用例、5 个预先存在的失败、红绿），没有夸大，带有披露段落。

结论：PASS
