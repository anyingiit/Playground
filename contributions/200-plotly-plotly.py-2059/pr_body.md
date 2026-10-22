### Link to issue

Closes #2059

### Description of change

With a continuous `color`, marginal traces are colored with `args["color_continuous_scale"][0]`. For a named scale like `"Viridis"` that is the first character (`'V'`), and for a list of `[position, color]` pairs it is the pair itself, so `px.scatter(..., color=<numeric>, marginal_x="box", color_continuous_scale="Viridis")` raises an invalid `marker.color` error. This PR normalizes the scale with `ColorscaleValidator` (as is already done for the coloraxis) before taking its first color.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

### Demo

```python
import plotly.express as px
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="sepal_length",
                 marginal_x="box", color_continuous_scale="Viridis")
fig.data[1].marker.color  # before: ValueError (received 'V'); after: '#440154'
```

### Testing strategy

Added `test_marginal_color_with_continuous_color_scale` in `tests/test_optional/test_px/test_marginals.py` (named, lowercase, reversed `_r`, list of colors and list of pairs × histogram/box/violin/rug). 16 of its 20 cases fail on `main` (the list-of-colors cases already worked) and all pass with this change.

- `python -m pytest tests/test_optional/test_px --ignore=.../test_imshow.py --ignore=.../test_trendline.py`: 1083 passed, 3 failed (`test_render_mode`, which needs `statsmodels`, not installed locally)
- `ruff format --check .` and `ruff check` on the changed files: clean

### Guidelines

- [x] I have reviewed the [pull request guidelines](https://github.com/plotly/plotly.py/blob/main/CONTRIBUTING.md#opening-a-pull-request) and the [Code of Conduct](https://github.com/plotly/plotly.py/blob/main/CODE_OF_CONDUCT.md) and confirm that this PR follows them.
- [x] I have added an entry to the [changelog](https://github.com/plotly/plotly.py/blob/main/CHANGELOG.md) if needed (not required for documentation PRs).
