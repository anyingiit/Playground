# vega/altair#3502 — 单个 Chart 上 `resolve_scale` 后再 layer/facet 报错信息不友好

| 项 | 值 |
|---|---|
| Issue | https://github.com/vega/altair/issues/3502 |
| Tier | 高星 |
| Labels | bug |
| Status | ✅ ready — patch + PR text 已完成 |
| 重复 PR 检查 | 2026-10-22：issue open、无 assignee、评论（rambip）无人认领；`gh pr list --search 3502` / `resolve_scale` 无相关 PR |
| AI 政策 | CONTRIBUTING / PR 模板 / AGENTS/CLAUDE.md 均无 AI 限制 |
| Base branch | `main` @ e0a40339 |
| DCO/CLA/changeset | 都不需要（release notes 由 PR 标题生成） |

## 问题理解
`alt.Chart(...).resolve_scale(color="independent")` 单独显示或放在 concat 里正常，但 `alt.layer(points)` / `points.facet(...)` 报 `SchemaValidationError: LayerChart has no parameter named 'mark'` / `UnitSpecWithFrame has no parameter named 'resolve'`，看不出原因。Vega-Lite schema 里 layer/facet 内部的 unit spec 不允许 `resolve`。

## 合理性判断
issue 作者（joelostblom，维护者）明确写了“a minimal fix in Altair would be to improve the error message”，并给出参考措辞（类似已有的 “Faceted charts cannot be layered…”）。改 Vega-Lite 行为不在本仓库范围，所以只做报错改进，不需要设计决策。

## 改动
- `altair/vegalite/v6/api.py`：新增 `_check_if_unit_chart_has_resolve(spec, "layer"|"facet")`；在 `_check_if_can_be_layered`（`alt.layer`、`+`、`+=` 都会走）和 `FacetChart.__init__` 里调用。对带 `resolve` 的 unit `Chart` 抛 `TypeError`：“Charts with a 'resolve' property cannot be layered/faceted. Instead, layer/facet … before calling `resolve_scale`, `resolve_axis` or `resolve_legend` on the layered/faceted chart.”
- 放在已有 facet-encoding 检查之后，原有错误信息优先级不变。concat / repeat 不受影响（它们本来就能工作）。
- 测试：`tests/vegalite/v6/test_api.py::test_resolve_on_unit_chart_layer_facet_errors`。

## 验证（Python 3.11 uv venv）
- Red（只回退 `altair/`）：新测试 `DID NOT RAISE TypeError` → 1 failed
- Green：1 passed
- `pytest -n 4 tests/vegalite tests/utils -m "not slow and not datasets_debug and not no_xdist"` → 538 passed, 4 skipped, 1 xfailed, 1 xpassed
- `pytest -n 4 tests/test_examples.py`（同 markers）→ 552 passed, 4 skipped（第一次和其他目录一起跑时有 29 个 example 失败，单独重跑及 base 上都全过，判断为并发/机器负载造成的偶发问题）
- `ruff check` ✓，`ruff format --diff --check` ✓；`mypy altair/vegalite/v6/api.py` 无 api.py 报错（测试文件只报缺 pandas-stubs，环境问题）
- 未运行：完整 `task test`（全量 mypy/ty、slow 测试、tests/test_toplevel.py 缺依赖）

## 需要提交者注意
- Conventional Commits 标题 `fix: ...`（仓库风格首字母大写）。无 DCO、无 AI trailer 要求，PR body 已有简短披露。
- 你另有一个未 review 的 altair PR #4162，互不冲突（不同文件区域）。
- 若维护者更想改成 warning 或自动把 resolve 提升到外层，可再调整；当前按 issue 建议做最小改动。

## 如何提交
```
git clone https://github.com/vega/altair && cd altair
git checkout -b fix/resolve-unit-chart-error
git am /path/to/202-vega-altair-3502/0001-*.patch
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。

## 独立复核（2026-10-23）
- 结论：PASS，无需修改。
- 上游：issue 仍 open、无 assignee、无人认领；无相关 open/merged PR（#4184/#4177/#4158/#4090 是 #4155 的通用报错改进，不冲突）。
- 新浅克隆 main @ e0a4033，`git am` 干净；作者 anyingiit。
- Red（回退 altair/）→ `DID NOT RAISE TypeError`；Green → 1 passed。
- `ruff check` / `ruff format --check` 通过；`pytest -n 6 tests/vegalite tests/utils -m "not slow and not datasets_debug and not no_xdist"` → 538 passed, 4 skipped, 1 xfailed, 1 xpassed（与 PR 正文一致）。
- 边界：repeat(row)、hconcat、带 resolve 的嵌套 LayerChart、`encode(facet=)` 均不受影响。`repeat(layer=[...])` 在带 resolve 的 unit chart 上仍是旧的 SchemaValidationError（base 同样如此，超出本 issue 范围，可作后续）。
