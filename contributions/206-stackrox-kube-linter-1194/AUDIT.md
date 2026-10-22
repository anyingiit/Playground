# Malicious-code audit — stackrox/kube-linter @ abea26c (main, 2026-10-21)

Tool: `python3 -I $PG/tools/audit_repo.py <clone>` (582 text files) → no auto-executing hooks, no npm lifecycle hooks, no committed binaries, no pattern findings.
The tree differs from the commit audited for contribution 056 (e23dee8) only by a `go.mod`/`go.sum` bump (`bmatcuk/doublestar` 4.10.2→4.10.3, `klauspost/compress` 1.18.4→1.18.7, both well-known modules, checksums in go.sum).

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `Makefile` | go mod tidy/verify, pinned tool installs from `tool-imports/`, `go generate`, `go test` | benign |
| `go:generate` (`pkg/templates/gen.go`, `pkg/config/gen.go`) | local codegen (`go run ./codegen`) writing params/generated files | benign |
| `e2etests/` (build tag `e2e`), bats scripts | run built binary on testdata; not executed here | benign |
| `.github/workflows/*` | CI only | benign (not run) |
| test `init()`/`TestMain` | template registrations only, no network/exec | benign |

Verdict: **no malicious code found**; safe to run `go test` for the touched package with GOCACHE inside the work dir.
