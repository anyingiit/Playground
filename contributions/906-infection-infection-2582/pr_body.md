## Description

When Infection runs on GitHub Actions with `--logger-text=php://stdout`, the text log is printed by `GitHubActionsLogTextFileReporter` (added in #2552), which groups the sections with `::group::`. As discussed in #2552, the GitHub Actions log viewer renders ANSI colors, so the mutant diffs in that log can be colored like a terminal diff.

This PR colors the diff lines of that reporter only:

- hunk headers (`@@ @@`) in cyan,
- removed lines in red,
- added lines in green.

The `--- Original` / `+++ New` header lines (everything before the first `@@`) are left as-is: they start with `-`/`+` but are not changes. A changed line that itself looks like a header (e.g. `--- $b;` after the hunk header) is still colored.

Implementation: `BaseTextFileReporter` gets a `formatDiff()` hook that returns the diff unchanged, so the plain `TextFileReporter` (and any log written to a file) produces exactly the same output as before. `GitHubActionsLogTextFileReporter` overrides it.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Changes

- Adds a `formatDiff()` hook to `BaseTextFileReporter` (identity by default).
- `GitHubActionsLogTextFileReporter` colors the diff lines with ANSI escape sequences.
- Updates `GitHubActionsLogTextFileReporterTest` expectations and adds a test for the header / context / header-looking change lines.

## Related issues

Fixes https://github.com/infection/infection/issues/2582.

## Checklist

- [x] Tests added/updated — `vendor/bin/phpunit tests/phpunit/Reporter/GitHubActionsLogTextFileReporterTest.php`: 7 tests OK (2 fail without the `src/` change); full unit suite `vendor/bin/phpunit --exclude-group e2e`: OK (6813 tests, 20 skipped, 2 incomplete — environment-gated)
- [x] `make cs` (no changes), `make phpstan`, `make validate`, `make test-autoreview` (1761 tests OK), `make rector-check`, `make detect-collisions`, `make check-agents-adr-list` pass locally (PHP 8.3). `make mago` reports 8 issues in `tests/phpunit/AutoReview/Makefile/MakefileTest.php`, identical on `master` in my local setup (dependencies had to be installed from source), unrelated to this change. zizmor / e2e / self-mutation not run (no Docker / coverage driver here).
- [ ] Documentation updated — n/a (log-output styling only; happy to open a site PR if you'd like it mentioned)
- [ ] CHANGELOG.md updated — n/a (no deprecation / BC break)
- [ ] Appropriate labels applied (e.g. `feature`, `Component / Reporter`, `Integration / GitHub`) — maintainers
