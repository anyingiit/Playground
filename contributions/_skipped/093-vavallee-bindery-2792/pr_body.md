## Summary

`AuthorAliasRepo.Merge` bound a raw `time.Now().UTC()` when it reparented the source author's books, so modernc.org/sqlite stored `books.updated_at` in Go's `time.String` shape (`2026-10-01 18:26:26.795488699 +0000 UTC`) instead of the RFC3339Nano that every other `books` writer has used since #914. The fix wraps the value in `timeValueArg(...)`, the same helper `books.go` and `editions.go` already use. That is a one-line change.

The other raw bind in `Merge` (`UPDATE author_identifiers ... updated_at = ?`) is unchanged. That table is written with a raw `time.Time` everywhere, including `upsertIdentifierTx`, so changing only the merge path would give it mixed shapes. If you want that table normalised too, I think it should be a separate change.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Closes #2792

## How it was verified

New test `TestMerge_WritesBookUpdatedAtAsRFC3339` (`internal/db/author_aliases_test.go`) merges two authors and reads `CAST(updated_at AS TEXT)` for the reparented book.

- On `main` (fix reverted, test kept) it fails for the reason given in the issue:
  `merge stored books.updated_at in Go default shape "2026-10-01 18:26:26.795488699 +0000 UTC"; want RFC3339Nano`
- With the fix applied, it passes.

## Checklist

- [x] Every commit carries a `Signed-off-by` that matches its author (`git commit -s`)
- [x] Changelog fragment added as `changelog.d/2792-merge-updated-at.md`, not an edit to `CHANGELOG.md`
- [x] Tests added or updated
- [ ] `docs/DEPLOYMENT.md` updated if env vars, config, or upgrade path changed — n/a
- [ ] Wiki pages under `docs/` updated if user-facing behaviour changed — n/a
- [x] No new dependency

## Test plan

- [x] `go test -count=1 ./internal/db` — ok
- [x] `go test -race -count=1 ./internal/db -run 'TestMerge|TestAlias'` — ok
- [x] `go build ./...`, `go vet ./...`, `gofmt -l internal/db` (clean)
- [x] `go test -p 2 -count=1 ./cmd/... ./internal/...` — all packages ok
- [ ] `golangci-lint run ./...` — not run locally; CI will run it
