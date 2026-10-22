## What changed

`PickIssueScriptGuardTest::stripComment()` now honours backslash escapes: a backslash escapes the next character everywhere except inside single quotes (where it is literal, as in the shell). Before, `\"` inside a double-quoted string closed the string, so a `#` after whitespace further along was read as a comment start and the rest of the line was cut away — a process substitution later on that line would have slipped past the #461 guard.

A new data-provider test, `testStripCommentFollowsTheShellQuotingRules()`, pins the quoting rules (comment after code, `#` inside a word and in `${#items[@]}`, `#` inside double and single quotes, an escaped quote inside double quotes, an escaped backslash before the closing quote, a literal backslash inside single quotes, an escaped quote outside quotes). One case is the issue's scenario with a process substitution after the escaped quote — `echo "a \" # b" <(cat) # c` — and asserts the `<(cat)` survives the stripping, so the guard still sees it. The class docblock no longer says the stripper is exact only because the script has no escaped quote. CHANGELOG entry under `[Unreleased]` → `### Tests`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Closes #662

## How it was tested

- Red → green: with the new test but without the stripper change, `vendor/bin/phpunit tests/Unit/Bin/PickIssueScriptGuardTest.php` fails the "escaped quote inside double quotes" and "escaped quote outside quotes" cases (2 failures); with the change the file is green (15 tests).
- `vendor/bin/phpunit --testsuite Unit --no-coverage` → OK (1850 tests, 2 skipped — the same 2 skips as on `master`; no `ext-grpc` here, so the `Grpc` suite was not run).
- `vendor/bin/phpstan analyse` → no errors; `phpcs --standard=phpcs.xml.dist` and `rector process --dry-run` on the test file → clean.

## Checklist

- [x] Tests added or updated, and all checks pass
- [x] `CHANGELOG.md` updated under `[Unreleased]`
- [x] Documentation updated (n/a — the class docblock is updated)
- [x] Everything is written in English
- [x] The PR title is a Conventional Commit (`feat: ...`, `fix: ...`)
