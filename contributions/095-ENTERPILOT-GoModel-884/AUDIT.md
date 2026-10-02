# Audit — ENTERPILOT/GoModel @ 39c217e1 (shallow clone of `main`, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/GoModel` + manual review of Go test hooks (`TestMain`, `exec.Command` in tests), Makefile and `.pre-commit-config.yaml`.

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` (pre-commit hooks) | Standard hygiene hooks, goimports, `make test-race`, `go mod tidy`; pre-commit was not installed/run here | benign / not run |
| long base64 `signature` in `tests/contract/testdata/**/messages_extended_thinking*.json` | Anthropic extended-thinking signature in recorded API fixtures | benign |
| `docs/install/install.sh:4` `curl … \| sh` | Comment showing the documented install one-liner | benign / not run |
| `docs/install/install.ps1` `Invoke-WebRequest` | Release installer downloading archive + checksums from the project's release URL | benign / not run |
| `TestMain` in tests/integration, tests/e2e, tests/perf, run/, internal/pluginload | Tag-gated suites (docker/e2e) or fixture setup; only the unit packages touched here were run | benign |
| `exec.Command` in tests (`go list`, `go env`, `go build -buildmode=plugin`, docker, mongo replset script) | Toolchain invocations / docker for integration tests; integration/e2e not run | benign |
| Makefile `install-tools` (go install golangci-lint pinned, pip pre-commit) | Pinned upstream tools | benign |

No committed binaries, no npm lifecycle hooks in the Go module path.

Verdict: nothing malicious; safe to run `go build` / `go test` / `go vet` / gofmt on the Go module.
