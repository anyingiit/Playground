# plotly/plotly.py #4580 — px.scatter: per-point `opacity` 数组与 `color` 一起用时错位

| 项 | 值 |
|---|---|
| Issue | https://github.com/plotly/plotly.py/issues/4580 |
| Tier | 高星 (>5k stars, very active) |
| Labels | bug, P3, sev-3 |
| Status | 🟡 partial — patch + PR text done; full px suite run interrupted (rerun before submitting) |
| 重复 PR 检查 (2026-10-01) | `/pulls?q=4580` → 0 results；关键词 "opacity" → #5781（error bars 不继承 opacity，closes #4353，不同问题，但同改 `_core.py`，可能有文本冲突需 rebase）；issue 0 评论、无 assignee、无关联 PR |
| AI 政策 | 未发现禁止；repo 有 `good for agent` label（"Good issue for an agent to solve"），接受 agent 贡献；不需要 DCO，也无 AI trailer 要求 |
| Base | `main` @ d586d225b8577fa3a4ff8954bdd47ef3b9cc0c07 |

## 问题理解
`opacity` 传入逐点数组时，`infer_config` 直接 `trace_patch["marker"] = dict(opacity=args["opacity"])`，整条数组被复制到**每一条** trace。只要数据被拆成多条 trace（`color`/`symbol`/facet/animation_frame）或被重排（`px.ecdf` 排序），透明度就和点对不上。复现：
```python
px.scatter(y=[1,2,3,4], color=['r','b','r','b'], opacity=[1,.2,.3,.4])
# trace r: y=[1,3], opacity=(1,0.2,0.3,1-长度4)  ← 错
```

## 合理性判断
维护者已打 `bug` 标签；`opacity` 文档写的是 float，但 plotly.js `marker.opacity` 本身 arrayOk，且无分组时数组已"碰巧"可用，issue 期望的正是数组随数据切分。改动只影响"数组且长度等于数据行数"的情况，标量/长度不匹配保持旧行为，无破坏性。

## 改动
- `plotly/express/_core.py`
  - 新增 `_add_opacity_column(args)`：在 `build_dataframe` 之后，若 `opacity` 为 array-like 且长度 == 行数，以隐藏列（`_px_opacity`，冲突时加前缀 `_`）加入内部 dataframe（支持 pandas/polars/pyarrow），列名记在 `args["opacity_col"]`。
  - `make_trace_kwargs`：若该 trace_spec 的 `marker.opacity` 正是用户传的数组（identity 判断，因此 marginal/trendline 等其它 trace 不受影响），用本组的隐藏列替换。
  - `dimensions`（scatter_matrix 等）排除隐藏列。
- `tests/test_optional/test_px/test_px.py`：4 个新测试（5 种 dataframe backend 的 color 分组；symbol+facet、list/numpy 输入且 hovertemplate 不含 opacity；scalar 不变；scatter_matrix 维度不含隐藏列）。
- `CHANGELOG.md`：Unreleased / Fixed 条目（CI 有 "Check changelog"）。
- 未改 `_doc.py` 中 `opacity` 的 "float" 说明（该条文档被 pie/funnel/density_map 共用，那里是 trace 级标量），PR 里提出可按需补。

## 验证
环境：`uv venv` + `uv pip install -e . pandas polars pyarrow numpy pytest ruff==0.11.12 statsmodels scikit-image xarray pillow pytz`（Python 3.11）。
- Red→green：`python -m pytest -q tests/test_optional/test_px/test_px.py -k opacity`
  - 修复前（`git stash -- plotly`）：**8 failed, 1 passed**（通过的是 scalar 测试，预期）
  - 修复后：**9 passed**
- 全量 px：`python -m pytest -q tests/test_optional/test_px` → 未跑完（被中断）；提交前请重跑并在 pr_body.md 中填入结果
- `ruff format --check .`（CI 的 check-formatting job）→ 1672 files already formatted
- `ruff check` 改动文件 → All checks passed（全仓 `ruff check .` 有大量既存 F401/F541，与本改动无关，CI 也不跑）
- 手工验证：px.bar 分 color、animation_frame（frames 内也正确切分）、marginal_x+trendline（只有主散点 trace 被切分）、px.ecdf（排序后对应正确）、长度不匹配时保持旧行为。

## 需要提交者注意
- PR 模板为 plotly 自己的格式（Link to issue / Description / Demo / Testing strategy / Additional / Guidelines），pr_body.md 已按它写并包含 motivation/disclosure 段落。
- Guidelines 两个复选框已勾选——提交前请自己确认读过 CONTRIBUTING 与 CoC。
- CHANGELOG 条目链接的是 issue #4580；若维护者偏好链接 PR，开 PR 后可改成 PR 号。
- 与 #5781（同改 `plotly/express/_core.py` 的 opacity 相关逻辑）可能产生合并冲突，提交前 rebase 到最新 main。
- 不需要 DCO / Signed-off-by，也不需要 AI trailer。

## 如何提交
```bash
git clone https://github.com/plotly/plotly.py && cd plotly.py
git checkout -b fix-px-opacity-array-4580 origin/main
git am /path/to/contributions/075-plotly-plotly.py-4580/0001-*.patch
# 或直接：
tools/submit_pr.sh contributions/075-plotly-plotly.py-4580 plotly/plotly.py main fix-px-opacity-array-4580 contributions/075-plotly-plotly.py-4580/pr_title.txt contributions/075-plotly-plotly.py-4580/pr_body.md
```

## PR
- Title: 见 `pr_title.txt`
- Body: 见 `pr_body.md`
