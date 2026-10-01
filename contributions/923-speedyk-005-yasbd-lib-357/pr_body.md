## Objective

The base rules did not know the common technical abbreviations `c.d.f.` (cumulative distribution function) and `w.r.t.` (with respect to), so text like `The model estimates the c.d.f. F.` or `The results are discussed w.r.t. V-TSMixer.` was cut into extra sentences after the abbreviation (reported from citracer in #357).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Changes

- Added `c.d.f` to base `REFERENCE_ABBRVS` (Scientific / Technical group), so it does not split when followed by a capital letter, number or bracket (`the c.d.f. F`), as suggested in the issue.
- Added `w.r.t` to base `INLINE_ONLY_ABBRVS` (Bridge/connectors group), since it never ends a sentence.
- Added English regression cases to `tests/test_data/english.py`: the issue's example, plus a `w.r.t.` + lowercase continuation guard.
- `CHANGELOG.md` entry under Unreleased → Fixed, and a row in `CONTRIBUTORS.md`.

Note: a sentence-final `c.d.f.` followed by a capitalized word (e.g. `We compute the c.d.f. It is monotone.`) is not split. Every `REFERENCE_ABBRVS` entry already behaves this way (`See the fig. It is clear.` doesn't split either), so I didn't touch it in this PR.

### Types of change

- [ ] New feature (language support, new utility, etc.)
- [x] Bug fix (non-breaking change fixing an issue)
- [ ] Code quality / performance improvement
- [ ] Documentation update
- [ ] Other (please describe):

## Verification

- [x] I ran `pytest` and all tests pass: `128 passed, 1081 subtests passed` (with `.[dev]` + `spacy langcodes py3langid`, as CI installs them). Without the rule change, the new `en` case fails (`'The model estimates the c.d.f.' != 'The model estimates the c.d.f. F.'`).
- [x] I ran `ruff format` / `ruff check` on the changed files: `base.py` is clean. The `ruff format --check` diff in `tests/test_data/english.py` and the repo-wide warnings in `benchmarks/bench_warm_cases.py` and `examples/query_summary.py` were already there on `main`, so I left them alone.
- [x] I have added tests for my changes (if applicable).
- [x] My changes don't require documentation updates, or I've updated them (CHANGELOG + CONTRIBUTORS).

## Related Issues

- Fixes #357
