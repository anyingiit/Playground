## Description

Reusing a `Writer`/`GenericWriter` with `Reset` produced files whose column chunks had `path_in_schema=[""]` (and, when sorting columns are configured, zeroed `sorting_columns`) for every file after the first.

Root cause: `writer.reset` calls `format.RowGroup.Reset` on the row group metadata of the previous file, and `RowGroup.Reset` / `ColumnMetaData.Reset` clear `SortingColumns` and `PathInSchema` in place. But the writer builds that metadata with slices it keeps using: each column chunk's `PathInSchema` is the column writer's `columnPath`, and `SortingColumns` is the writer's `sortingColumns` from the config. Clearing them in place wiped the column paths and sorting columns used for every later file.

Fix: in `writer.reset`, set those shared slices to `nil` on the old row group before calling `Reset`, so the in-place clear only touches memory the row group owns. Nothing changes for the footer decoder, which is what the in-place `Reset` semantics are meant for.

`TestWriterResetPreservesColumnChunkMetadata` writes three files with one `GenericWriter` (with a descending sorting column) and checks `PathInSchema` and `SortingColumns` in each footer. It fails on `main` for files 2 and 3 (`got=[""]`, `got=[{ColumnIdx:0 Descending:false ...}]`) and passes with this change.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #602

## Checklist

- [x] Tests pass locally (`go test -trimpath -race ./...` — all packages ok, go1.24.9 linux/amd64; new test red on `main`, green with the fix; `go vet -tags purego .` clean; `gofmt -l .` and `go tool -modfile go.tools.mod modernize -test .` report nothing)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the changelog is no longer maintained per PR
- [ ] Documentation is updated (if applicable) — n/a, bug fix with no API change
