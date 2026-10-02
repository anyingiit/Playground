## Description

A run whose only non-pass outcome is `NeedsReview` ends in a clean `TestFail` with no error, and the harness reported it as `Unexpected exit from <service> with no error or success`, with the summary line at `ERROR` (#311). The cause: `runOne` marks only `TestPass` as successful, and `closeClient` had no branch for a clean non-pass exit.

Changes:

- `command`: `runOne` stores the plugin's exit code on `PluginPkg` in a new `ExitCode` field (`InternalError` when the RPC client can't be set up). The logging moves out of `closeClient` into `logResult`. A clean `TestFail` is now logged at `Warn` as `Plugin for <service> completed with non-passing results`. Anything else that has no error and isn't a success still gets the "Unexpected exit" message, which now includes the exit code.
- `pluginkit`: the per-suite summary line (`> ...: N Passed, N Warnings, N Failed, N Possible`) for a `NeedsReview` suite is logged at `Warn` rather than `Error`, the same level as the per-assessment `NeedsReview` lines. `Failed` and `Unknown` stay at `Error`. The level choice is in a new `logSuiteSummary` helper so it can be unit tested.

On the open design question in the issue (should `NeedsReview` get its own exit code?): I kept the minimal option. `ExitCodeFor` still maps `NeedsReview` to `TestFail`, so the exit status doesn't change and neither do CI gates built on `pvtr run`. The fix only changes how the result is logged. A dedicated exit code would change `shared/exitcodes.go`, `exitSeverity` and the behaviour downstream users see, so that seems like a call for the maintainers and could be a follow-up. I also left the `debug` subcommand's exit status (point 3 in the issue) unchanged. Happy to add either if you want them in this PR.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Refs #311 (fixes the "Unexpected exit" message and the summary log level. The dedicated exit code and the `debug` exit status are left for a decision.)

## Checklist

- [x] Tests pass locally: `go vet ./...` clean; `go test -race ./... -coverprofile coverage.out -covermode atomic` all packages ok (total coverage 68.7%, CI gate 45%); `go build ./...` ok; `golangci-lint run` (v2.11.4) reports 0 issues. The new `TestLogResult` (command) and `TestLogSuiteSummary` (pluginkit) fail when the new branches are removed and pass with them.
- [ ] `CHANGELOG.md` is updated (if applicable): n/a, release notes come from release-drafter.
- [ ] Documentation is updated (if applicable): n/a, only log messages changed.
