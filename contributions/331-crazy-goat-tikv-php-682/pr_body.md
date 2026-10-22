## What changed

`tests/Unit/RawKv/RawKvBatchUnresolvedKeyTest.php` and `tests/Unit/TxnKv/CommitPrewriteKeyCoverageTest.php` no longer probe whether the fail-closed contract of #244 is implemented:

- Each file gets a `testResolverFailsClosedForAKeyOutsideTheReturnedRegions()` that pins the contract directly: `RegionResolver::batchResolveRegions(['z'])` with a PD window that does not cover `'z'` must throw `TiKvException` (the RawKV file also checks the redacted key in the message, as the neighbouring tests do).
- The probe (`requireFailClosedContract()` in the RawKV file, the inline `try`/`catch` in the commit test) and its "not implemented yet" branch — `expectNotToPerformAssertions()` plus an `E_USER_WARNING` — are deleted, so the dependent tests run unconditionally.
- The class docblocks no longer say that #244 "is not merged yet"; a CHANGELOG entry goes under `[Unreleased]` → `### Tests`.

Beyond being dead code, the placeholder branch hid regressions: with the fail-closed `throw` in `RegionResolver::batchResolveRegions()` disabled, both files on `master` still exit green, because the probe takes the early return: PHPUnit reports only `OK, but there were issues!` with the probe's single `E_USER_WARNING` (`RawKvBatchUnresolvedKeyTest`: 2 tests, 0 assertions; `CommitPrewriteKeyCoverageTest`: 2 tests, 5 assertions), and CI does not run with `--fail-on-warning`. With this change the same mutation fails one test in each file.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Closes #682

## How it was tested

- `vendor/bin/phpunit --testsuite Unit --no-coverage` → OK (1842 tests, 2 skipped — the same 2 skips as on `master`; no `ext-grpc` here, so the `Grpc` suite was not run).
- `vendor/bin/phpstan analyse` → no errors; `phpcs --standard=phpcs.xml.dist` and `rector process --dry-run` on both test files → clean.
- Mutation check described above (fail-closed `throw` disabled): `master` → both files exit 0 with one warning each; this branch → 1 failure per file (`testResolverFailsClosedForAKeyOutsideTheReturnedRegions`). Unmutated, each file is `OK (3 tests, 7 assertions)`.

## Checklist

- [x] Tests added or updated, and all checks pass
- [x] `CHANGELOG.md` updated under `[Unreleased]`
- [x] Documentation updated (n/a beyond the test docblocks)
- [x] Everything is written in English
- [x] The PR title is a Conventional Commit (`feat: ...`, `fix: ...`)
