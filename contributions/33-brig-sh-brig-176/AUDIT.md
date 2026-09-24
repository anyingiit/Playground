# Malicious-code audit — brig-sh/brig @ 039aabe (main, 2026-09-21)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/brig` (268 text files), then manual review
of everything that runs during `go build` / `go test` / `script/smoke.sh`.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (npm lifecycle, setup.py, build.rs, …) | none present (pure Go module) | benign |
| Committed binaries | none (0 bytes) | benign |
| `install.sh:4` pipe-to-shell | a usage comment (`curl -fsSL https://brig.sh/install \| sh`) documenting the project's own installer; not executed by build/test | benign |
| `cmd/brig/secret.go:545` `~/.ssh/id_ed25519` | help text example for `brig secret create -f` | benign |
| `internal/wrap/workspace.go:316` `~/.docker/config.json` | code comment explaining a symlink-escape defence | benign |
| `Makefile` | `go build` / `go test -race` / `go vet` / `gofmt`; `snapshot` uses goreleaser (not run) | benign |
| `TestMain` in 4 packages | only `profile.Load()` (parses embedded profile YAML) | benign |
| `exec.Command` in tests | re-exec of the test binary (brigd), `git config -f <tmp>`, `/bin/sh <tmp stub script>`, `go list -deps`, macOS `security` (darwin-only, not built here) | benign |
| `script/smoke.sh` | drives the built binary against a stub `hull` runtime inside `mktemp -d`, cleaned on exit | benign |
| `go.mod` deps | `godbus/dbus/v5`, `golang.org/x/sys`, `sigs.k8s.io/yaml` (+ yaml/v2 indirect) — well-known | benign |

**Verdict: no malicious code found; safe to build and test.** GOCACHE/GOMODCACHE kept under `/home/user/work/brig-cache` and deleted afterwards.
