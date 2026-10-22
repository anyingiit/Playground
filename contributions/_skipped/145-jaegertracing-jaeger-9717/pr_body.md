## Which problem is this PR solving?
- Part of #9717 (milestone **M4 — remove the read-side padding**). M1 is being handled separately in #9721; M2/M3 are not touched here.

## Description of the changes
- `dbmodel.TraceID.ToOTEL` / `dbmodel.SpanID.ToOTEL` (ES/OS v2 tracestore) used to left-pad shorter hex strings with zeros. Since every writer goes through pdata and stores 32-char trace IDs / 16-char span IDs, the padding only existed for legacy short-form documents. Both functions now require exactly 32 / 16 hex characters and return `trace ID from DB must be 32 hex chars, got N` (resp. `span ID ... 16 ...`) otherwise. They also decode straight into the `pcommon` array instead of padding + copying.
- Deleted `tracestore/core/fixtures/es_01.json` (16-char IDs) and its companion `domain_01.json`; neither is referenced by any test.
- Tests that only covered the padding (`64-bit trace ID right-aligned`, `shorter span ID right-aligned`) now assert the rejection instead. Tests that relied on short/empty IDs being silently padded (`TestFromDBModelErrors`, `TestSetParentId`, `TestParentIdWhenRefTraceIdIsDifferent`, `TestSpanWriter_RejectedSpansError`, the reader / span-search "malformed" cases) now use full-width IDs or expect the new width error.

Behavior note for reviewers: an empty `traceID`/`spanID` in a stored document used to decode as an all-zero ID and now returns an error. ES writers never produce such documents, but I wanted to call it out.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## How was this change tested?
- Red → green: with only the updated `ids_test.go` applied, `go test ./internal/storage/v2/elasticsearch/tracestore/core/dbmodel/ -run ToOTEL` fails (short/empty IDs accepted, old error text); with the fix it passes.
- `go test ./internal/storage/v2/elasticsearch/...` — all packages pass.
- `go vet ./internal/storage/v2/elasticsearch/...` — clean.
- `gofumpt -d` (v0.11.0, as pinned in `internal/tools`) on changed files — no diff.
- `golangci-lint run ./internal/storage/v2/elasticsearch/tracestore/...` (v2.13.1 from `internal/tools`) — only a pre-existing `revive` hit in `core/writer.go:277`, which this PR does not touch.
- Not run: the full `make lint test` and the ES/OpenSearch integration tests (need a live cluster).

## Checklist
- [x] I have read https://github.com/jaegertracing/jaeger/blob/main/CONTRIBUTING_GUIDELINES.md
- [x] I have signed all commits
- [x] I have added unit tests for the new functionality
- [x] I have run lint and test steps successfully (targeted subset, see above)
- [ ] `CHANGELOG.md` — n/a, generated from PR titles/labels at release time
- [ ] Documentation — n/a, internal storage code

## AI Usage in this PR (choose one)
See [AI Usage Policy](https://github.com/jaegertracing/jaeger/blob/main/AI_POLICY.md).
- [ ] **None**: No AI tools were used in creating this PR
- [ ] **Light**: AI provided minor assistance (formatting, simple suggestions)
- [ ] **Moderate**: AI helped with code generation or debugging specific parts
- [x] **Heavy**: AI generated most or all of the code changes
