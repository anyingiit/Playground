LLM generated content, by Claude Code (reviewed by a human before submission)

#### Reference Issues/PRs

Part of #10652 (task 1), see also #3429.

#### What does this implement/fix? Explain your changes.

`SupervisedIntervals` was excluded from `test_get_test_params_coverage` (via the `tests:skip_by_name` tag) and listed in `EXCLUDE_SOFT_DEPS`, because `get_test_params` only returned more than one parameter set when `numba` is installed - without `numba` it returned a single dict.

This PR adds a second parameter set that does not use the `numba`-based feature functions (`n_intervals=2`, `min_interval_length=4`, `randomised_split_point=False`, default features), so `get_test_params` now returns at least two sets also when `numba` is not installed. The two existing `numba`-function feature sets are kept and appended when `numba` is present (4 sets in total then). With that:

* the `test_get_test_params_coverage` skip tag is removed from `SupervisedIntervals`
* `SupervisedIntervals` is removed from `EXCLUDE_SOFT_DEPS` in `sktime.tests._config`

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below; I went through the new parameter set by hand as #10652 asks. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it - please feel free to close it, no hard feelings at all 🙂

#### Does your contribution introduce a new dependency? If yes, which one?

No.

#### What should a reviewer concentrate their feedback on?

* whether the new no-soft-dependency parameter set is "interesting" enough (it changes `n_intervals`, `min_interval_length` and `randomised_split_point` vs. the defaults, and uses the default feature set)

#### Did you add any tests for the change?

No new test function - removing the skip tag means the existing `test_get_test_params_coverage` (and the rest of the suite) now runs on `SupervisedIntervals` with the new parameter set.

Checked locally (Python 3.11, `pip install -e .` + `numba<0.68`):

* `check_estimator(SupervisedIntervals, raise_exceptions=False)`: 224 tests, all PASSED (including `test_get_test_params_coverage[SupervisedIntervals]`)
* `pytest -n 2 sktime/tests/tests/test_test_utils.py sktime/transformations/tests/test_intervals.py sktime/tests/test_all_estimators.py -k "SupervisedIntervals or test_excluded_tests_by_test or test_run_test_for_class or test_intervals"`: 191 passed, 1 skipped
* in an environment without `numba`, `SupervisedIntervals.get_test_params()` returns a single `{}` on `main` and a list of 2 sets with this change
* `ruff format --check` / `ruff check` (v0.13.1, as in pre-commit) on the changed files: clean

#### Any other comments?

Scope: only `SupervisedIntervals`; I checked that it is not covered by the other open task-1 PRs (#11335, #11218, #11067, #11023, #11058, #10980, #10839, #11226, ...).

#### PR checklist

##### For all contributions
- [ ] I've added myself to the [list of contributors](https://github.com/sktime/sktime/blob/main/CONTRIBUTORS.md) with any new badges I've earned :-)
- [x] The PR title starts with either [ENH], [MNT], [DOC], or [BUG].

## Checklist

- [x] Tests pass locally (see "Did you add any tests" above)
- [ ] `CHANGELOG.md` is updated (if applicable) - n/a, sktime generates the changelog from PR titles at release time
- [ ] Documentation is updated (if applicable) - n/a, test parameters only
