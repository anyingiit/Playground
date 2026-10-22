# plotly/plotly.py #4040 — x/y 列名列表中有拼写错误时报出误导性的 "same length" 错误

| 项 | 值 |
|---|---|
| Issue | https://github.com/plotly/plotly.py/issues/4040 |
| Tier | 高星 (very active) |
| Labels | bug, P3 |
| Status | ✅ ready — patch + PR text 已完成 |
| 重复 PR 检查 (2026-10-22) | issue open、无 assignee；评论：维护者 nicolaskruchten 2023-02 欢迎帮助，abarpan3 2023-07 贴了思路截图询问反馈但从未开 PR（3 年多无后续，不算认领）；`gh pr list --state all --search 4040` → 0；关键词 "misleading error"/"is_col_list"/"same length"/"typo column" → 无相关 PR |
| AI 政策 | 无 AGENTS.md/CLAUDE.md；CONTRIBUTING/.github/labels 均无 AI 限制 |
| Base | `main` @ 0de8a381c36511a23b2ca7b6295f1a4bc72af434 |

## 问题理解
`build_dataframe` 先用 `_is_col_list` 判断 x/y 是否是"全部为列名的列表"来决定 wide mode；只要有一个名字不是列（拼写错误），就不进 wide mode，列表被当作数据（长度 2），随后在 `process_args_into_dataframe` 中与 x（长度 100）比较，报 "All arguments should have the same length"，没有提示是列名写错。

## 合理性判断
维护者明确确认应给出更好提示并欢迎 PR，同时指出难点是 wide mode 判定发生得早。这里不改 wide mode 判定（避免行为变化），只在"该列表不可能是合法数据"时把误导性报错换成清晰报错。

## 改动
- `plotly/express/_core.py`：新增 `_check_col_list_typos(field, argument, df_input, length)`，在 `process_args_into_dataframe` 的 list/array 分支中对 `x`/`y`（仅当提供了 data_frame）调用。触发条件：参数是非空 list/tuple、元素全是 str、有元素不是列名、长度 ≠ data_frame 行数，并且（长度 ≠ 已处理参数长度 **或** 混有真实列名）。否则保持原行为（例如 `px.scatter(df, x=["u","v","w"], y="b")` 这类字符串数据仍可用）。
- `tests/test_optional/test_px/test_px_input.py`：`test_wrong_column_name_in_list`（5 种 dataframe 后端，4 种场景）+ `test_list_of_strings_as_values_with_data_frame`（守护原有行为）。
- `CHANGELOG.md`：Unreleased / Fixed 条目，链接 issue #4040。

## 验证
环境同 200：Python 3.12 venv，`pip install -e . pandas numpy pytest polars pyarrow ruff==0.11.12`。
- Red→green：`python -m pytest -q tests/test_optional/test_px/test_px_input.py -k "column_name_in_list or strings_as_values"`
  - 修复前（`git stash -- plotly`）：5 failed, 1 passed（通过的是守护测试，预期）
  - 修复后：6 passed
- `python -m pytest -q tests/test_optional/test_px --ignore=tests/test_optional/test_px/test_imshow.py --ignore=tests/test_optional/test_px/test_trendline.py` → 1069 passed, 10 skipped, 4 xfailed, **3 failed**（均为 `test_render_mode[*]`：缺 statsmodels，环境问题，main 上同样失败）
- 未运行：test_imshow.py / test_trendline.py（需 xarray/scikit-image/statsmodels）、tests/test_core。
- `ruff format --check .` → 1672 files already formatted；`ruff check` 改动文件 → All checks passed

## 需要提交者注意
- 不需要 DCO / CLA / Signed-off-by，也无 AI trailer 要求；PR body 已含 disclosure。
- Guidelines 两个复选框已勾，提交前请自己确认。
- CHANGELOG 条目链接 issue #4040，开 PR 后可改为 PR 号。
- 与 200（#2059）在 `CHANGELOG.md` 同一位置追加条目，两者都提交时后者需 rebase 解决小冲突。
- 已知未覆盖的边角：列表里**全部**都是拼错的名字、且它是第一个被处理的参数（如 `x=["X1","X2"], y="data1"`）时，仍会落到原来的长度报错（y 那一侧）；为避免把合法的字符串数据误判为列名，未扩大触发条件。PR 里可按维护者意见再调整。

## 如何提交
```bash
git clone https://github.com/plotly/plotly.py && cd plotly.py
git checkout -b fix-px-wide-typo-error-4040 origin/main
git am /path/to/contributions/201-plotly-plotly.py-4040/0001-*.patch
```

## PR
标题见 `pr_title.txt`，正文见 `pr_body.md`。
