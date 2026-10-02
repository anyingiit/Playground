## Description

🤖🤖 This PR was prepared with an AI coding agent (see disclosure below).

`ProcessHandler.system()` in `IPython/utils/_process_posix.py` binds `child` inside the `try:` block (`child = pexpect.spawn(...)`). If the `KeyboardInterrupt` arrives while pexpect is still spawning the child (as seen on the conda-forge aarch64/ppc64le builds in `test_system_interrupt`), `child` is never assigned and the `except KeyboardInterrupt:` handler fails with:

```
UnboundLocalError: cannot access local variable 'child' where it is not associated with a value
```

Fix:

- initialise `child = None` before the `try:`;
- in the `except KeyboardInterrupt:` handler, if there is no child yet there is nothing to forward `^C` to or terminate, so print `^C` (same as `getoutput()` does) and return `-signal.SIGINT`. That keeps the existing convention of `system()` (a negative number for "terminated by signal N"), so callers such as `%sx`/`!cmd` see a normal interrupted status instead of a crash.

The normal path and the "interrupted after spawn" path are unchanged.

A regression test, `tests/test_process.py::test_system_interrupt_during_spawn`, monkeypatches `pexpect.spawn` to raise `KeyboardInterrupt`, so the race is reproduced deterministically. It fails with the `UnboundLocalError` above without the fix.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and reviewed by me. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #12164

## Checklist

- [x] Regression test added (`tests/test_process.py::test_system_interrupt_during_spawn`)
- [ ] `CHANGELOG.md` / whatsnew entry — n/a (bug fix; `docs/source/whatsnew/pr/` is for new features and incompatible changes only)
- [ ] Documentation is updated — n/a (no user-facing behaviour change besides not crashing)
