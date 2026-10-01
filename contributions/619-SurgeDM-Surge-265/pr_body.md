## Description

Adds a `file_exists_action` setting (General tab) so users can choose what Surge does when the destination file already exists:

- `rename` (default, unchanged behavior) — save the new download as `name(1).ext`
- `overwrite` — keep the requested name; the completed download replaces the existing file

How it works:

- `ResolveDestination` reads the setting. In overwrite mode an existing **regular file** with the requested name is no longer treated as a collision. Names that belong to an active download, names with a pending `.surge` working file and directories still fall back to `name(N).ext`, so overwrite can never clobber another in-flight or paused download.
- The replace itself happens in the existing finalize step (`.surge` → final rename, or the EXDEV copy fallback). `finalizeCompletedFile` used to treat "final path exists" as success after a failed rename. With overwrite mode, that would report success while keeping the old file, so it now does that only when the `.surge` working file is gone.
- TUI: pressing Enter on the row switches between `< Rename >` and `< Overwrite >`, the same way the Theme row cycles. `docs/SETTINGS.md` documents the new key.

The issue also mentions a "prompt every time" mode. I left it out on purpose because downloads also come from the CLI, the HTTP API and the browser extension, where nobody can answer a prompt. I'm happy to follow up with a TUI-only prompt if you want it. This PR builds on the scope of the earlier #268 (closed as stale) and includes the overwrite-mode tests that were requested there.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #265 (rename + overwrite; "prompt" mode not included, see above)

## Checklist

- [x] Tests pass locally
  - New tests: `TestResolveDestination_FileExistsAction`, `TestFinalizeCompletedFile_OverwritesExistingFile`, `TestFinalizeCompletedFile_FailedReplaceIsNotSuccess` (orchestrator), `TestFileExistsActionValidation` (config), `TestSettings_FileExistsActionCycles` (tui). They fail without the change and pass with it.
  - `go test -race ./...` passes, except for `internal/strategy/single` `TestSingleDownloader_PreallocateFailure_ReleasesFileHandle`, which fails the same way on `main` in my environment (the tests run as root, so the read-only file it relies on is still writable).
  - `gofmt -l` (clean), `go vet` on the touched packages, `go build ./...`, `go test ./internal/lint/...`
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (the repo has no CHANGELOG)
- [x] Documentation is updated (if applicable) — `docs/SETTINGS.md`
