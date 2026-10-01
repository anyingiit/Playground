## Which problem is this PR solving?
- Part of #9717 (milestone M1: the remote gRPC storage byte-copy bug). M2–M4 are left for separate PRs, as the issue describes them as independent.

## Description of the changes
- The remote storage `Handler.GetTraces` and the `TraceReader` (`FindTraceIDs`, `FindTraceSummaries`) converted wire trace IDs with `copy(sized[:], bytes)`. For an 8-byte (64-bit) ID that fills the **high** half, while `model.TraceIDFromBytes` and all writers put it in the **low** half, so the remote path asked for / returned a different trace ID than the stored one.
- All three call sites now go through a small `traceIDFromBytes` helper that places 8 bytes in the low half. Other lengths keep the existing `copy` behavior, so nothing else changes (I did not want to start rejecting odd lengths in this PR; happy to switch to `model.TraceIDFromBytes` + an error if you prefer strict validation).
- The existing `FindTraceIDs` table case "trace ID with less than 16 bytes" asserted the old high-half placement; it now asserts the low half.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## How was this change tested?
- New regression tests `TestHandler_GetTraces_ShortTraceID`, `TestTraceReader_FindTraceSummaries_ShortTraceID`, and the updated 8-byte case in `TestTraceReader_FindTraceIDs`: all three fail on `main` and pass with the fix.
- `go test -race -count=1 ./internal/storage/v2/grpc/...` → ok
- `go test ./cmd/remote-storage/...` → ok, except `TestAdminServerHandlesPortZero`, which fails identically on unmodified `main` in my sandbox (environment-related, not touched by this change)
- `golangci-lint run ./internal/storage/v2/grpc/...` (v2.13.1 from `internal/tools`) → 0 issues; `golangci-lint fmt --diff` → no diff
- Full `make lint test` was not run.

## Checklist
- [x] I have read https://github.com/jaegertracing/jaeger/blob/main/CONTRIBUTING_GUIDELINES.md
- [x] I have signed all commits
- [x] I have added unit tests for the new functionality
- [ ] I have run lint and test steps successfully: `make lint test` — ran the package-scoped subset listed above
- CHANGELOG.md: n/a (generated from PR labels at release time)
- Documentation: n/a

## AI Usage in this PR (choose one)
See [AI Usage Policy](https://github.com/jaegertracing/jaeger/blob/main/AI_POLICY.md).
- [ ] **None**: No AI tools were used in creating this PR
- [ ] **Light**: AI provided minor assistance (formatting, simple suggestions)
- [ ] **Moderate**: AI helped with code generation or debugging specific parts
- [x] **Heavy**: AI generated most or all of the code changes
