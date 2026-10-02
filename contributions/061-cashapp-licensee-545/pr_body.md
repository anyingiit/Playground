## Description

When the `licensee` task runs with `--quiet` (`-q`), the per-artifact coordinate header (e.g. `com.example:sdk1:1.0.0`) was dropped while the ` - ERROR: ...` / ` - WARNING: ...` lines beneath it were still printed, so it was impossible to tell which artifact a problem belonged to.

Root cause: the header was always logged at `LIFECYCLE`, which Gradle suppresses in quiet mode, whereas its results are logged at `ERROR`/`WARN`. The header is now logged at the most severe level among its own results (`ERROR` if any error, `WARN` if any warning, `INFO` if only info / `ViolationAction.IGNORE`). Output without `--quiet` is unchanged, since `WARN`/`ERROR` and `LIFECYCLE` render identically there.

Added a `spdx-not-allowed-log-quiet` fixture (copy of `spdx-not-allowed-log`) and a `violationsLoggedQuiet` test that runs `licensee --quiet` and asserts the coordinate is printed above the error. It fails on `trunk` (output is only ` - ERROR: SPDX identifier 'Apache-2.0' is NOT allowed`) and passes with this change. Also added a `CHANGELOG.md` entry under Unreleased → Fixed.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #545

## Checklist

- [x] Tests pass locally (`./gradlew test --tests '*.LicenseePluginFixtureTest.violations*' --tests '*.LicenseePluginFixtureTest.unused*' --tests '*.LicenseePluginFixtureTest.failure*' --tests '*.LicenseePluginFixtureTest.allFixturesCovered*' --tests '*.SpdxLicensesTest'`: 43 tests, 0 failures, both Gradle versions; `./gradlew check -x test` (lint, spotlessCheck, ABI check, checkFixtureJars): passed. The new test fails without the fix.)
- [x] `CHANGELOG.md` is updated (if applicable) — Unreleased → Fixed
- [ ] Documentation is updated (if applicable) — n/a
