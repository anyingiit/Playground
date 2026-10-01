## Description

Running `conftest pull git::<repo>` a second time fails because the destination (`policy/` by default) already contains a checkout. go-getter's git getter then takes its *update* path, which fetches and checks out the URL's `ref`; with no `ref` in the URL that is an empty string, so the update fails (`empty string is not a valid pathspec` on older git, `invalid ref: ""` with current go-getter). Unlike the clone path, the update path does not fall back to the remote's default branch.

This change makes `downloader.Download` add `ref=HEAD` to a git source URL when the destination is already a git checkout and the URL has no `ref`, so the update fetches the remote's default branch — the same thing a fresh clone checks out. URLs with an explicit `ref`, subdirectory (`//dir`) sources and destinations that aren't a git checkout (including the empty-directory cases covered by the existing tests) behave as before.

A regression test (`TestDownloadGitUpdatesExistingCheckoutWithoutRef`) pulls a local `git::file://` repo twice, with a new commit in between, and checks the second pull succeeds and updates the files. It fails on `master` with `invalid ref: ""` and passes with this change.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #1022

## Checklist

- [x] Tests pass locally (`go test ./... -count=1` — all packages ok; new test red on `master` → green; `go vet ./downloader/`, `gofmt -l` clean)
- [x] Lint (`golangci-lint run ./...` v2.13.2, same version as CI — no issues in `downloader/`; the 12 remaining findings are pre-existing on `master`)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (no changelog in repo; release notes are generated)
- [ ] Documentation is updated (if applicable) — n/a (behavior fix, no doc change needed)
