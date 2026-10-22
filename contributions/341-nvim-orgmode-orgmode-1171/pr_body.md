## Summary

This PR fixes clocking out again after a clock out was undone (#1171).

`Clock:org_clock_out()` sets `self.clocked_headline = nil` after clocking out. When the clock out is undone, the `CLOCK:` line is running again, but the clock no longer remembers the headline, so `update_clocked_headline()` has to find it. It only asks `OrgFiles:get_clocked_headline()`, which scans the agenda files. If the file is not one of them (e.g. a new org file, as in the issue), nothing is found and `<prefix>xo` does nothing.

`update_clocked_headline()` now falls back to the current file (only when it is an `org` buffer, and only when it has a `CLOCK:` line without an end, using the existing `has_running_clock_candidate()` check) and takes its clocked-in headline. The same lookup is used by clock in, cancel and goto, so those also see a clock that is running in the current file.

## Related Issues

Closes #1171

## Changes

- `lua/orgmode/clock/init.lua`: `Clock:_get_clocked_headline_in_current_file()`, used by `update_clocked_headline()` when no agenda file has a running clock.
- `tests/plenary/ui/clock_spec.lua`: new test "should clock out again after undoing a clock out". It uses a file that is not among the loaded agenda files: clock in, clock out, `undo`, clock out again. The file is deleted at the end so it does not leak into the agenda files of the following tests.

## Checklist

I confirm that I have:

- [x] **Followed the
      [Conventional Commits](https://www.conventionalcommits.org/)
      specification** (e.g., `feat: add new feature`, `fix: correct bug`,
      `docs: update documentation`).
- [x] **My PR title also follows the conventional commits specification.**
- [x] **Updated relevant documentation,** if necessary. (No docs change needed.)
- [x] **Thoroughly tested my changes.**
- [x] **Added tests** (if applicable) and verified existing tests pass with
      `make test`. The new test fails without the change (the second clock out leaves `CLOCK: [...]` open) and passes with it. `clock_spec.lua` passes (12 tests). In the full `make test` run, the only failures are 5 tests (org id uuid, capture expression ×2, api id, hyperlink id). They fail the same way on `master` in my environment, which has no `uuidgen`.
- [x] **Checked for breaking changes** and documented them, if any. (None.)

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code (the commit carries the `AI-assisted: Claude Code` trailer, per AGENTS.md) and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂
