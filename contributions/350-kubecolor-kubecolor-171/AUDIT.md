# Malicious-code audit — kubecolor/kubecolor @ 189d201 (main, 2026-09-29)

Tool: `python3 /home/user/Playground/tools/audit_repo.py <clone>` (146 text files), then manual review.

| Hit / area | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface, npm hooks, committed binaries | tool reports none | — |
| `assets/packaging/rpmsign.sh`, `reprepro.sh` (mount ~/.gnupg into docker) | release-packaging helpers for signing rpm/deb with the maintainer's own key; never invoked by build/test | benign |
| `Makefile` | build/test/fmt/lint/corpus/config-schema targets; plain `go` commands only. `docs` target runs `go run github.com/charmbracelet/freeze@latest` (not used here) | benign |
| `//go:generate make config-schema.json` in `main.go` | regenerates JSON schema from config package; not run (go generate not needed) | benign |
| `init()` in `*/init_test.go`, `config/testconfig` | `os.Clearenv()`, force color, cmp options — no I/O beyond env | benign |
| `exec.Command` in `command/runner.go`, `command/complete.go` | runs `kubectl` / pager at runtime (that is the tool's purpose); no test file uses exec or net/http | benign |
| `internal/cmd/imagegen` | docs screenshot generator; not run | benign |
| `.github/workflows/ci.yml` | zizmor, `make testcover` with gotestsum, docker build, config-schema diff, corpus-update diff, go-version check | benign |

Verdict: **no malicious code found**; safe to run `go test` with a local GOCACHE.
