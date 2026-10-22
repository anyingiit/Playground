<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KPKpHzfAxy5KoBhHBfd3QVb)_

## Description

```python
int = 42
del int
int('42')  # F821 undefined name 'int'
```

At module scope the rebinding replaces the `Builtin` binding, and `del` then removed the name entirely, so later uses were reported as undefined even though the builtin is visible again at runtime. (In function and class scopes this already worked, since lookups fall through to the module scope.)

`handleNodeDelete` now re-adds the `Builtin` binding when a module-level name that shadowed a builtin (including custom builtins) is deleted. Deleting a builtin that was never rebound is left as it is today (this doesn't touch the separate `del <builtin>` handling discussed in #355).

One side effect worth mentioning: `int = 1; del int; del int` no longer reports the second `del`, since the name now resolves to the builtin again; this matches how a plain `del int` is treated today.

Tests added in `test_undefined_names.py`: shadow + `del` + use, and the `_` case from the issue (custom builtin, used inside a function). Both fail without the change.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #548

## Checklist

- [x] Tests pass locally — `PYFLAKES_ERROR_UNKNOWN=1 coverage run -m unittest discover pyflakes`: 799 tests OK (28 skipped); `flake8 pyflakes setup.py` clean; the new code is fully covered (the only uncovered lines are `test_permissionDenied`, skipped because the run was as root)
- [ ] `NEWS.rst` — n/a (written at release time)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
