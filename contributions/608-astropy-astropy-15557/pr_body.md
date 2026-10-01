### Description

This pull request is to address `SlicedLowLevelWCS` treating negative indices as pixel offsets before the first pixel instead of counting from the end of the array (#15557). For example, slicing a 5-pixel axis with `slice(-3, None)` gave world values for pixels -3..-1 rather than 2..4.

Negative integer indices and negative slice `start`/`stop` values are now resolved in `SlicedLowLevelWCS.__init__` against the `array_shape` of the WCS being sliced, following NumPy semantics (slice bounds below `-size` clip to 0, an integer index below `-size` raises `IndexError`). Resolution happens before the slices are combined with any existing slicing, so nested slicing such as `[2:8]` then `[1:-1]` now also gives the right result instead of an empty shape. If the WCS has no `array_shape`, a negative index cannot be interpreted and an `IndexError` is raised. Non-negative indices are unchanged.

Tests cover the example from the issue, negative slice starts/stops, negative integer indices, nested slicing, and the no-shape and out-of-bounds errors. A changelog entry is in `docs/changes/wcs/` (to be renamed to the PR number).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Fixes #15557

### AI Disclosure

Claude Code (MODEL_AND_VERSION_TO_FILL) was used to draft the code change, the tests, the changelog entry and this description. I reviewed the change, ran the tests below, and will handle review feedback myself.

Verified locally (Python 3.12):
- `pytest astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py` — 51 passed (the new tests fail without the fix: 9 failed)
- `pytest astropy/wcs astropy/nddata astropy/visualization/wcsaxes` — all passed
- `ruff check` / `ruff format --check` on the changed files — clean

- [ ] I certify that I am human and that I take full responsibility for this pull request including all interactions with reviewers.

### Merge method
- [ ] By checking this box, the PR author has requested that maintainers do **NOT** use the "Squash and Merge" button. Maintainers should respect this when possible; however, the final decision is at the discretion of the maintainer that merges the PR.
