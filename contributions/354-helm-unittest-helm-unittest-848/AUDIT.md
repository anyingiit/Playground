# Malicious-code audit — helm-unittest/helm-unittest @ 0d79286 (main, "Add opt-in parallel execution of test suites (#906)")

Re-checked 2026-10-01: fresh clone still at 0d79286, audit applies unchanged.

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/w6-helm-unittest-848` (547 text files), then manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface / npm hooks / committed binaries | none reported | — |
| `install-binary.sh` / `install-binary.ps1` download functions | plugin install scripts that download the release tarball from the project's own GitHub releases and verify the checksum; only run by `helm plugin install`, never by `go test` | benign |
| `Dockerfile:27` `gpg --export > ~/.gnupg/pubring.gpg` | builds the release image keyring for plugin signature verification; not run locally | benign |
| `go:generate`, `TestMain`, `os/exec`, `net/http` in Go sources | `grep -rn` over all `*.go`: none found | — |
| `func init()` | only `cmd/helm-unittest/helm_unittest.go`: registers cobra flags | benign |
| `Makefile` | build/install/docker/test helpers (`go test ./... -v -cover -race`, plugin copy into `$HELM_PLUGINS`); not invoked — tests run directly with `go test` | benign |
| `.github/workflows/go.yml` | `go test -cover ... ./...`, SonarCloud, junit upload; matrix ubuntu/macos/windows | benign |
| `go.mod` dependencies | helm v3/v4, k8s apimachinery/client-go, yaml libs, cobra, testify — all well-known upstream modules fetched via the Go module proxy with go.sum verification | benign |

Verdict: **no malicious code found**; safe to run `go test` for the affected packages in an isolated GOCACHE under /home/user/work.
