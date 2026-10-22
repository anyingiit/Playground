### Link to issue

Closes #4580

### Description of change

When `opacity` is passed as a per-point array (e.g. `px.scatter(y=a, opacity=b, color=c)`), Plotly Express copied the *whole* array into `marker.opacity` of every trace. As soon as the data is split into several traces (by `color`, `symbol`, facets, animation frames) or reordered (e.g. `px.ecdf`), the opacity values no longer line up with the points. This PR stores an array-like `opacity` of matching length as a hidden column of the internal dataframe, so it is grouped/sorted together with the rest of the data, and each trace gets only its own slice in `marker.opacity`. Scalar `opacity` and arrays whose length doesn't match the data keep the existing behaviour; the hidden column is excluded from `scatter_matrix` dimensions and never shows up in hover labels.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

### Demo

```python
import plotly.express as px
fig = px.scatter(y=[1, 2, 3, 4], color=["r", "b", "r", "b"], opacity=[1, 0.2, 0.3, 0.4])
[list(t.marker.opacity) for t in fig.data]
# before: [[1, 0.2, 0.3, 0.4], [1, 0.2, 0.3, 0.4]]  (points of each trace get the wrong values)
# after:  [[1.0, 0.3], [0.2, 0.4]]
```

### Testing strategy

Added tests in `tests/test_optional/test_px/test_px.py`: per-point opacity split by `color` across all dataframe backends (pandas, pandas-nullable, pandas-pyarrow, polars, pyarrow), split by `symbol` + `facet_col` for list and numpy inputs (also asserting nothing leaks into the hovertemplate), `scatter_matrix` (hidden column not added to dimensions), and scalar opacity unchanged. The new array tests fail on `main` and pass with this change.

- `python -m pytest tests/test_optional/test_px` — new opacity tests: 9 passed (8 failed on main); full px suite: <fill in>
- `ruff format --check .` — 1672 files already formatted; `ruff check` on the changed files — all checks passed

### Additional information (optional)

I left the `opacity` docstring (`"float"`) untouched since the same doc entry is shared with `px.pie`/`px.funnel`/`px.density_map`, where opacity is a trace-level scalar; happy to update it if you'd like array support documented for marker-based functions.

### Guidelines

- [x] I have reviewed the [pull request guidelines](https://github.com/plotly/plotly.py/blob/main/CONTRIBUTING.md#opening-a-pull-request) and the [Code of Conduct](https://github.com/plotly/plotly.py/blob/main/CODE_OF_CONDUCT.md) and confirm that this PR follows them.
- [x] I have added an entry to the [changelog](https://github.com/plotly/plotly.py/blob/main/CHANGELOG.md) if needed (not required for documentation PRs).
