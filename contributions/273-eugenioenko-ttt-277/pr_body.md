## Description

Opening a file with no write permission (e.g. `chmod 444`) gave no hint that it was read-only, and saving overwrote it silently. As the issue notes, `Buffer.SaveFile` writes a temp file and renames it over the target, and that rename succeeds when the containing directory is writable.

Changes:
- `buffer.recordDiskInfo` (runs on load and on save) now sets `Buffer.ReadOnlyOnDisk` when the file has no write bits.
- The tab title shows `(readonly)` for such files. This reuses the suffix that read-only viewer tabs already use (`OpenFileReadOnly`), so the two don't show up together.
- `File > Save` on a read-only file opens a `Cancel / Overwrite` confirmation, with Cancel as the default. Overwrite falls through to the existing "modified on disk" check and then the normal save. The saved file keeps its 0444 mode because `SaveFile` already preserves permissions.
- LSP rename's `SaveOnRename` skips read-only files and leaves them dirty instead of overwriting them without asking.

Tests:
- `internal/core/buffer`: `TestReadOnlyOnDisk` checks that the flag is set for a 0444 file, is cleared after saving to a writable file, and is off for a new buffer.
- `tests/e2e/readonly_file_test.go`: checks that the tab indicator appears, that Save opens the dialog and Cancel leaves the file untouched, and that Overwrite saves the buffer and keeps the file read-only.

With the fix reverted, `TestReadOnlyOnDisk`, `TestReadOnlyFileShowsIndicator` and `TestReadOnlyFileSavePromptsAndCancelKeepsFile` fail. With the fix, all of them pass.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #277

## Checklist

- [x] Tests pass locally: `go test ./...` passes, `go vet ./...` is clean, `golangci-lint run ./...` reports 0 issues and `gofmt -l` is clean
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a
