## Description

`DynamicObject::enumerate` in the Python bindings collected the iterator with `filter_map`, silently dropping every `Err` returned by `__next__`. An iterator that keeps raising never reaches `StopIteration`, so `{% for x in items %}` over it spun forever at 100% CPU (also reachable on free-threaded Python when a dict is mutated concurrently).

This change stops at the first error and yields it as an invalid value (the "fallible iteration" pattern documented on `Value`). The VM validates each loop item, so the original Python exception (here `ValueError`) is raised from `render_str`, consistent with how lookup errors are surfaced since #814. Values produced before the error are kept as before.

A regression test (`test_iteration_errors`) uses an iterator that raises 100 times before stopping, so a regression fails instead of hanging; it also asserts `__next__` is called only once. A CHANGELOG entry is added under Unreleased.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #956

## Checklist

- [x] Tests pass locally (`maturin develop` + `pytest` in `minijinja-py`: 49 passed; new test fails without the fix with "DID NOT RAISE ValueError"; `pyright python`: 0 errors; `cargo fmt --check` and `cargo clippy -p minijinja-py -- -D warnings` clean)
- [x] `CHANGELOG.md` is updated (if applicable) — entry under Unreleased
- [ ] Documentation is updated (if applicable) — n/a
