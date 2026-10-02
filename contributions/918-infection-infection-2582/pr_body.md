## Description

Follow-up to #2552: GitHub Actions logs render ANSI colors, so the `GitHubActionsLogTextFileReporter` (used when the text log goes to `php://stdout` with the GitHub logger enabled) now prints the mutant diffs colored - removed lines in red, added lines in green - like the CLI does for `--show-mutations`.

Unlike #2292 (colors in annotations, which GitHub does not render), this only touches the plain log output.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it - please feel free to close it, no hard feelings at all 🙂

## Changes

- `BaseTextFileReporter` gets a `formatDiff()` hook (identity by default, so `TextFileReporter` output is unchanged).
- `GitHubActionsLogTextFileReporter` overrides it to wrap lines starting with `-` / `+` in ANSI red / green. Only the diff goes through the hook, so the `$ command` line and the (indented) process output are never colored.
- Updated the expected output in `GitHubActionsLogTextFileReporterTest`.

## Checklist

- [x] Tests added/updated - `GitHubActionsLogTextFileReporterTest` fails without the `src/` change and passes with it; `vendor/bin/phpunit tests/phpunit/Reporter` -> OK (132 tests)
- [x] `make cs`, PHPStan, Rector check, `composer validate`, AutoReview suite (1761 tests), collision detector: green. Mago reports only the same pre-existing `MakefileTest` issues it reports on `master` in my local setup.
- [ ] Documentation updated - n/a (the GitHub log output already exists; this only colors it)
- [ ] CHANGELOG.md updated - n/a (no deprecation/BC break)
- [ ] Appropriate labels applied - suggested: `Feature`/`DX`, `Component / Reporter`, `Integration / GitHub`

## Reviewer Notes

- The `--- Original` / `+++ New` header lines are colored as well, the same as the CLI's multi-line fallback in `DiffColorizer`.
- I did not reuse `DiffColorizer`: it emits Symfony console tags (`<diff-add>`, ...) that need an `OutputFormatter`, and the file reporter writes raw lines to the stream.

## Related issues

Fixes https://github.com/infection/infection/issues/2582.
