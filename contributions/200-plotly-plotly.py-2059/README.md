# plotly/plotly.py #2059 — px marginal 在命名连续色阶下取到色阶名首字母当颜色

| 项 | 值 |
|---|---|
| Issue | https://github.com/plotly/plotly.py/issues/2059 |
| Tier | 高星 (very active) |
| Labels | bug, P3 |
| Status | ✅ ready — patch + PR text 已完成 |
| 重复 PR 检查 (2026-10-22) | issue open、无 assignee、评论中无人认领（最后评论 2023 年仅确认仍复现）；`gh pr list --state all --search 2059` → 0；关键词 "marginal colorscale"/"color_continuous_scale marginal"/"marginal color" → 只有无关的 #5707（heatmap marginal，已合并）、#5780（trendline 不进 marginal，open，不同问题） |
| AI 政策 | 无 AGENTS.md/CLAUDE.md；CONTRIBUTING/.github/labels 均无 AI 限制（之前 075 记录有 `good for agent` 标签） |
| Base | `main` @ 0de8a381c36511a23b2ca7b6295f1a4bc72af434 |

## 问题理解
连续 `color` + `marginal_x/y` 时，`make_trace_specs` 用 `args["color_continuous_scale"][0]` 给 marginal trace 设 `marker.color`。当色阶是字符串名（`"Viridis"`、`"magma"`）时取到首字母 `'V'`/`'m'` → plotly 校验报错；当色阶是 `[[pos, color], ...]` 时取到 `[0, 'red']`（box 报错，histogram 被当作颜色数组静默接受，也是错的）。`px.defaults.color_continuous_scale="Viridis"` 同样触发。

## 合理性判断
维护者 nicolaskruchten 2020 年确认是 bug（引入字符串名/二维列表色阶时漏改此处），2023 年有人确认 5.12 仍复现；main 上复现确认。修复很小、无行为争议。

## 改动
- `plotly/express/_core.py`：取首色前先 `ColorscaleValidator("colorscale", "make_figure").validate_coerce(...)` 归一化为 `[[pos, color], ...]`，取 `[0][1]`（与同文件 coloraxis 的处理一致；该 validator 已在文件顶部 import）。
- `tests/test_optional/test_px/test_marginals.py`：新参数化测试（5 种色阶写法 × histogram/box/violin/rug）。
- `CHANGELOG.md`：Unreleased / Fixed 条目，链接 issue #2059（CI 有 "Check changelog" job）。

## 验证
环境：`uv venv --python 3.12` + `uv pip install -e . pandas numpy pytest polars pyarrow ruff==0.11.12`（conftest 需要 polars/pyarrow；未装 statsmodels/xarray/scikit-image）。
- Red→green：`python -m pytest -q tests/test_optional/test_px/test_marginals.py -k continuous_color_scale`
  - 修复前（`git stash -- plotly`）：16 failed, 4 passed（通过的是 `["red","blue"]` 列表写法，预期）
  - 修复后：20 passed
- `python -m pytest -q tests/test_optional/test_px --ignore=tests/test_optional/test_px/test_imshow.py --ignore=tests/test_optional/test_px/test_trendline.py` → 1083 passed, 10 skipped, 4 xfailed, **3 failed**（均为 `test_render_mode[*]`：`ModuleNotFoundError: statsmodels`，环境缺依赖，与改动无关）
- 未运行：test_imshow.py（需 xarray/scikit-image）、test_trendline.py（需 statsmodels）；tests/test_core 未跑（未改动 core）。
- `ruff format --check .` → 1672 files already formatted；`ruff check` 改动文件 → All checks passed

## 需要提交者注意
- 不需要 DCO / CLA / Signed-off-by，也无 AI trailer 要求；PR body 已含 disclosure。
- PR 模板为 plotly 自有格式；Guidelines 两个复选框已勾，提交前请自己确认读过 CONTRIBUTING 与 CoC。
- CHANGELOG 条目链接的是 issue #2059；开 PR 后可改为 PR 号链接（仓库其它条目多链 PR，维护者常补 "with thanks to @xxx"）。
- 与 201（#4040）同改 `CHANGELOG.md` 的同一位置，若两者都提交，后提交的那个需 rebase 解决 CHANGELOG 小冲突。

## 如何提交
```bash
git clone https://github.com/plotly/plotly.py && cd plotly.py
git checkout -b fix-px-marginal-named-colorscale-2059 origin/main
git am /path/to/contributions/200-plotly-plotly.py-2059/0001-*.patch
```

## PR
标题见 `pr_title.txt`，正文见 `pr_body.md`。

## 独立复核 (2026-10-23)
- 上游复查：#2059 仍 open、无 assignee、无认领；`gh pr list --state all --search 2059` → 0。patch 在当前 main (0de8a38) 上单独 `git am` 干净（与 201 各自独立都能应用；两者同改 CHANGELOG 同一位置，先合并一个后另一个需 rebase）。
- 复核验证（Python 3.12 uv venv：pandas numpy pytest polars pyarrow narwhals ruff==0.11.12）：red→green 修复前 16 failed/4 passed，修复后 20 passed（test_marginals.py 全部 181 passed）；`tests/test_optional/test_px`（忽略 imshow/trendline）1083 passed, 3 failed（test_render_mode，缺 statsmodels）；ruff format/check 通过。
- 代码审查：用已 import 的 `ColorscaleValidator` 归一化后取 `[0][1]`，与同文件 coloraxis 处理一致；`_r` 反转、小写名、颜色列表、`[pos,color]` 列表都覆盖。PR 文本准确，无改动。
