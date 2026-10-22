# 425 — BSC-ES/autosubmit#3104: PROJECT_SUBMODULES_DEPTH parsing

| Item | Details |
|---|---|
| Issue | https://github.com/BSC-ES/autosubmit/issues/3104 |
| Tier | Free (BSC workflow manager; 422 is in the same repo) |
| Labels | bug, discussion, good first issue; milestone 4.2.1; opened by maintainer kinow |
| Base branch | `master` (patch built on 5919cd9) |
| Status | ✅ 可提交 |
| Duplicate check | 2026-10-22: the issue has no comments, no assignee and no linked PR. A PR search for "submodules depth" found no related PR. |
| AI policy | None |
| CLA/DCO | None |

## Problem
- What the issue reports: the warning says the default -1 is used, but `[]` is returned.
- What I found while reproducing it:
  - an integer config value (YAML `3`, kept as an int after loading) raises an uncaught TypeError;
  - a YAML list is ignored (only the misleading "Using default value -1" warning is logged);
  - a non-numeric string raises an uncaught ValueError.

## Change
- `get_project_submodules_depth` now accepts an int, a list, or a string form of either.
- Invalid values log the warning and return `[-1]`.
- For the caller, `[-1]` is equivalent to `[]`: both give `max_depth=-1`.
- Added tests and a CHANGELOG entry (4.2.0 Bug fixes).

## Verification
- Red: 8 of the 13 new cases fail.
- Green: 13 passed.
- `test/unit/config` and `test/unit/git`: 282 passed, 2 skipped.
- `ruff check` passes.

## How to submit
```
git clone https://github.com/BSC-ES/autosubmit && cd autosubmit && git checkout -b fix-submodules-depth origin/master
git am /path/to/0001-*.patch
```
Note: this is the second autosubmit PR this round, after 422. The two can be submitted at the same time. Both touch CHANGELOG, but at different positions: 425 at the top of the Bug fixes list and 422 at the end. They do not conflict.

## 独立复核（2026-10-22）

复核环境：全新克隆 `BSC-ES/autosubmit` 到 /home/user/work/review425，`git checkout 5919cd9`，`git am` 补丁成功应用。使用 /home/user/work/autosubmit/.venv 的 python（`-m pytest`，`PYTHONPATH` 指向复核克隆，已确认 `autosubmit.__file__` 指向 review425），`USER=root`。

已核实：
- Issue #3104：WebFetch 确认标题与描述一致（警告称默认 -1，实际返回 `[]`），标签 bug/discussion/good first issue，里程碑 4.2.1，无评论、无指派、无关联 PR。
- 解析逻辑：int `3`→`[3]`；list `[1, 2]`/`["1","2"]`→`[1, 2]`；字符串 `"3"`/`"-1"`/`"[1,2]"`/`"[ 1 , 2 ]"`→正确；`"abc"`、`""`、`"[]"`、`"[1,a]"`、`"[1, 2"`、`"3.5"`、`None`、dict→警告 + `[-1]`。
- 调用方：唯一生产调用方是 `autosubmit/git/autosubmit_git.py` 的 `clone_repository`。`[]` 与 `[-1]` 都得到 `max_depth = -1`；按子模块索引深度的分支只在 `max_depth > 0` 时进入，`[-1]` 不会被当作 `--depth -1` 使用，所以所有分支行为一致。该函数经 `copy_code` 被 `create` 和 `refresh` 调用，PR 描述属实。
- 真实配置加载：在 conf/ 写入 `GIT.PROJECT_SUBMODULES_DEPTH: 3` 并执行 `reload(force_load=True)`，值保持为 `int`；补丁前抛出 `TypeError: argument of type 'int' is not iterable`，补丁后返回 `[3]`。
- 红→绿：仅回退 configcommon.py 时，13 个新用例中 8 个失败；应用补丁后 13 个全部通过。
- `pytest test/unit/config test/unit/git`：282 passed, 2 skipped。
- `ruff check`（0.17.1，与 pyproject 固定版本一致）对改动文件：All checks passed。docstring 风格与 `Log.warning(f"...")` 写法符合仓库惯例。
- CHANGELOG：条目位于 4.2.0（当前未发布版本，最新 tag 为 v4.1.17.1）的 Bug fixes 列表，格式与相邻条目一致。与 422 补丁在两种顺序下（425→422、422→425）都能 `git am` 干净应用，无冲突。
- 提交：作者 anyingiit <49945850+anyingiit@users.noreply.github.com>；提交信息中没有 AI 模型名；内容基本准确。
- pr_body.md：英文，前两行是署名块，含 AI 辅助披露段落。

复核时做的小修改：
- pr_body.md：清单原来只有 3 项，已按 `.github/PULL_REQUEST_TEMPLATE.md` 补全为模板的 8 项，并加上 `**Check List**` 标题。
- pr_body.md 与 README.md：旧代码遇到 YAML 列表时会记录一条（误导性的）警告，并非"silently ignored"，措辞已改为"被忽略（只记录误导性的 -1 警告）"。

非阻塞的观察（不需要改补丁）：
- 提交信息里仍写着 "a YAML list was silently ignored"。旧代码其实会记录警告，所以措辞略不精确，但不影响正确性，可在提交前顺手改成 "ignored"。
- `True` 会解析为 `[1]`，`2.7` 会截断为 `[2]` 且不发警告。这和 `int()` 的语义一致，属于边缘输入，可以接受。
- YAML 空列表 `[]` 返回 `[]` 且不发警告。对调用方来说与 `[-1]` 等价。

结论：PASS。修复正确、行为安全，测试与 PR 描述中的数字都能独立复现，lint 通过，与 422 无冲突；pr_body 的小问题已在包内修正。
