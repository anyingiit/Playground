## Description

Standalone snapshots (`MatchStandaloneSnapshot`, `MatchStandaloneJSON`, `MatchStandaloneYAML`) derive their file name from the test name. Until now only `/` was replaced, so characters such as `:`, `<`, `>`, `"`, `|`, `?`, `*` and `\` ended up in the file name, which is invalid on Windows (and awkward elsewhere). A `%` in the test name also broke the `_%d` format verb that numbers standalone snapshots, since the path is passed through `fmt.Sprintf`.

This adds a small `sanitizeFilename` helper (used in `constructFilename`) that replaces path separators, the Windows-reserved characters above, `%` and control characters with `_`. Test names without these characters produce exactly the same file names as before, so existing snapshots are unaffected; snapshots whose names did contain them will be written under the sanitized name (the old file shows up as obsolete via the usual `snaps.Clean`). Explicitly configured filenames (`snaps.Filename`) are left untouched.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #156

## Checklist

- [x] Tests pass locally (`make test` — all packages ok; `make test-trimpath` — ok; `golangci-lint run ./...` — 0 issues; `gofumpt -l -w -extra .` + `golines . -w` — no changes). New subtest `TestSnapshotPath/should_return_standalone_snapPath_with_sanitized_test_name` fails without the fix and passes with it.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, internal behavior; the `snapshotPath` doc comment is updated
