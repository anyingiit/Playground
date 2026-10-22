### Link to issue

Closes #4040

### Description of change

When `x`/`y` is a list of column names with a typo, PX doesn't enter wide mode, treats the list as data, and fails with a misleading "All arguments should have the same length" error. This PR adds a check in `process_args_into_dataframe`: if a list of strings passed to `x`/`y` contains names that aren't columns of `data_frame` and its length doesn't match the previously-processed arguments (i.e. the "same length" error would be raised anyway), it raises an error naming the missing column(s) and listing the available ones instead. Lists of strings used as data keep working as before, even if some of them happen to match column names. A typo in an `x` list that is processed before any other argument still gets the old length error, since at that point the list could still be valid data.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

### Demo

```python
px.line(df, x="x", y=["data1", "Data2"])
# before: ValueError: All arguments should have the same length. The length of argument `y` is 2, whereas ...
# after:  ValueError: Value of 'y' looks like a list of column names, but 'Data2' is not the name of a column
#         in 'data_frame'. Expected one of ['x', 'data1', 'data2'] but received: ['data1', 'Data2']
```

### Testing strategy

Added `test_wrong_column_name_in_list` (all dataframe backends; typo in `y`, all names wrong, and typo in `y` without `x` for pandas), which fails on `main`, and `test_list_of_strings_as_values_with_data_frame` to check that lists of strings used as data (including ones containing column names) still work.

- `python -m pytest tests/test_optional/test_px --ignore=.../test_imshow.py --ignore=.../test_trendline.py`: 1069 passed, 3 failed (`test_render_mode`, which needs `statsmodels`, not installed locally)
- `ruff format --check .` and `ruff check` on the changed files: clean

### Guidelines

- [x] I have reviewed the [pull request guidelines](https://github.com/plotly/plotly.py/blob/main/CONTRIBUTING.md#opening-a-pull-request) and the [Code of Conduct](https://github.com/plotly/plotly.py/blob/main/CODE_OF_CONDUCT.md) and confirm that this PR follows them.
- [x] I have added an entry to the [changelog](https://github.com/plotly/plotly.py/blob/main/CHANGELOG.md) if needed (not required for documentation PRs).
