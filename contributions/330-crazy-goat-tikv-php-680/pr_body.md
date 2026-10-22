## What changed

Two small fixes in `src/Client/Region/RegionErrorHandler.php`, as described in #680:

- The invalidation guard now reads `$cache instanceof RegionCacheInterface` (the short name the file already imports) instead of the fully-qualified `\CrazyGoat\TiKV\Client\Cache\RegionCacheInterface`.
- The first paragraph of the `check()` docblock now states the NotLeader exception: a NotLeader error at a site owned by a `RetryExecutor` is left cached even when a cache and a region id are passed, as the docblock explains further down.

One deviation from the issue's definition of done, on purpose: the guard is **not** dropped. It is not always true — `$cache` is `?RegionCacheInterface`, so the `instanceof` is the null check that stops `invalidate()` from being called on `null` when a caller passes a region id without a cache (`testRegionErrorWithoutCacheDoesNotThrowFromInvalidation()` pins it; removing the guard makes that test fail with an `Error`). Spelling it `$cache !== null` does not survive the lint either: Rector's `FlipTypeControlToUseExclusiveTypeRector` rewrites it back into the fully-qualified `instanceof`, which is how the trap got there. So the guard keeps the `instanceof` form with the short name, and a short FAQ entry in `docs/helpers/faq.md` records why, so the next audit does not file it again. CHANGELOG entry under `[Unreleased]`. No behaviour change.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Closes #680

## How it was tested

- `vendor/bin/phpunit --testsuite Unit --no-coverage` → OK (1840 tests, 2 skipped — the same 2 skips as on `master`; no `ext-grpc` here, so the `Grpc` suite was not run).
- `vendor/bin/phpstan analyse` → no errors; `phpcs --standard=phpcs.xml.dist` and `rector process --dry-run` on the changed file → clean (Rector resolved fresh, so it is the version CI picks).
- Guard check: replacing the guard with `true` makes `RegionErrorHandlerTest::testRegionErrorWithoutCacheDoesNotThrowFromInvalidation` fail; with the patch the file is green (33 tests).

## Checklist

- [x] Tests added or updated, and all checks pass (existing tests cover the guard; no new test needed for a docblock/spelling change)
- [x] `CHANGELOG.md` updated under `[Unreleased]`
- [x] Documentation updated (`docs/helpers/faq.md` entry)
- [x] Everything is written in English
- [x] The PR title is a Conventional Commit (`feat: ...`, `fix: ...`)
