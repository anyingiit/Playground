# Malicious-code audit — privateerproj/privateer-sdk @ 66b9dce (main, 2026-10)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/privateer-sdk` (154 text files) → no auto-executing hooks, no npm lifecycle hooks, no committed binaries, no pattern findings. Manual review below.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `func init()` in any Go package (runs on `go test`) | none in the repo | — |
| `os/exec` users: `command/run.go`, `command/types.go`, `command/harness/benchmark.go`, `internal/install/manifestexec.go` | launch installed plugin binaries / `publish-manifest` subcommand only when the CLI runs a plugin; tests use mocks / `t.TempDir()` | benign |
| Tests with HTTP (`ai/*_test.go`, `internal/{auth,catalog,oci,publish,install}/*_test.go`, `pluginkit/apicalls_test.go`) | all use `net/http/httptest` local servers; no external endpoints | benign |
| `Makefile` | `go mod tidy / build / vet / test` only | benign |
| `.github/workflows/*.yml` | CI: `go vet`, `go test -race` + coverage gate, `go build`; golangci-lint v2.11.4; PR-title lint; release-drafter | benign |
| `go.mod` toolchain `go 1.26.2` | fetched by `GOTOOLCHAIN=auto` from the official Go proxy (checksum-verified by `go`) | benign |

Verdict: **no malicious code found**; safe to build and run the unit tests with GOPATH/GOCACHE under /home/user/work.
