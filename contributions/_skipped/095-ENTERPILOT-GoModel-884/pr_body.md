## Description

Writes down the JSON library rule from #884 and fixes the drift it listed. No user-visible change.

- `docs/adr/0014-json-libraries.md`: goccy by default, gjson for read-only extraction from raw bytes, `encoding/json` only where its exact semantics are needed (with a comment saying which), yaml.v3 for config. `AGENTS.md` points to it.
- `sqlutil` gets `EncodeJSONStrings` / `DecodeJSONStrings` (NOT NULL column, `nil` -> `"[]"`, errors returned). `users/store_sql.go` (`allowed_models`, was stdlib) and `virtualmodels/store.go` (`user_paths`) now use them instead of their own copies. Error messages keep the column name.
- `messages_native.go`: the comment now gives the real reason for stdlib (the splice relies on stdlib's `RawMessage` + `InputOffset` behaviour), not "goccy lacks InputOffset".
- `auditlog/body.go` already explains its stdlib `Valid` on `main`, so it is left as is.

**Motivation / disclosure:** I had some spare AI-assistant quota and am using it to help projects with open good-first-issues. This change was prepared with an AI coding assistant and verified as listed below. If it doesn't fit or you'd rather not take it, please feel free to close it.

## Related issue

Closes #884

## Checklist

- [x] Tests pass locally: `go test ./cmd/... ./config/... ./ext/... ./internal/... ./run/...` (all ok). New `TestEncodeJSONStrings`, `TestDecodeJSONStrings`, `TestJSONStringsRoundTrip` in `internal/storage/sqlutil`.
- [x] `golangci-lint` v2.13.1 on the touched packages: 0 issues; `gofmt -l` clean; `go vet`, `go build ./...` ok.
- [ ] `CHANGELOG.md` — n/a (no CHANGELOG; suggested label `release:internal`)
- [x] Documentation — new ADR-0014, one line in `AGENTS.md`
