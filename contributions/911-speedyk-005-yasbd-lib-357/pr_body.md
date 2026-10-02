## Objective

The base rules did not know the common abbreviations `c.d.f.` (cumulative distribution function) and `w.r.t.` (with respect to), so text like `The model estimates the c.d.f. F. The results are discussed w.r.t. V-TSMixer.` was split into four sentences instead of two.

## Changes

- Added `c.d.f` to `Rules.REFERENCE_ABBRVS` (Scientific / Technical group), as proposed in the issue.
- Added `w.r.t` to `Rules.INLINE_ONLY_ABBRVS` (Bridge/connectors group), as proposed in the issue.
- Added three cases to `test_universal_regression` in `tests/test_boundary_detector.py` (the issue example plus a capitalized word after each abbreviation). All three fail on `main` and pass with this change.
- Added a `CHANGELOG.md` entry under Unreleased / Fixed and a row for myself in `CONTRIBUTORS.md`.

`scripts/reformat_sets.py` does not change `base.py` after this edit. It does rewrite the unrelated `en.py`/`fa.py` sets on current `main`, so I left those out to keep this PR atomic.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

### Types of change

- [ ] New feature (language support, new utility, etc.)
- [x] Bug fix (non-breaking change fixing an issue)
- [ ] Code quality / performance improvement
- [ ] Documentation update
- [ ] Other (please describe):

## Verification

- [x] I ran `pytest` and all tests pass (`127 passed, 2 skipped, 1079 subtests passed`; the 2 skips are the spaCy component tests because spaCy isn't installed locally).
- [x] I ran `ruff format . && ruff check --fix .` (`ruff format --check src tests` / `ruff check src tests`: clean).
- [x] I have added tests for my changes (if applicable). With the rule change reverted, the 3 new cases fail. With it applied, they pass.
- [x] My changes don't require documentation updates, or I've updated them. `CHANGELOG.md` is updated.

## Related Issues

- Fixes #357
