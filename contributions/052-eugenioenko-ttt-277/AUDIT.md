# Malicious-code audit — eugenioenko/ttt @ 5db5bcf (HEAD unchanged on 2026-10-01 resume; still current)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/ttt` (799 text files scanned), then manual review of everything that runs during build/test.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `tests/functional/vitest.config.js`, `tests/integration/vitest.config.js` | Plain vitest configs (timeouts / include globs) | Benign. The JS suites were **not run** here (they need pnpm and a built binary) |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| `herdr-plugin/scripts/install.sh:10` curl \| sh | Installs the project's own `install.sh` from its own repo on GitHub; this is the plugin installer for end users and is never invoked by build or tests | Benign, not run |
| `install.sh` (root) | Downloads the project's own release binary from GitHub releases into `~/.local/bin`; not used by build or tests | Benign, not run |
| `internal/app/plugin_api_test.go:268` raw IP 169.254.169.254 | Test table asserting the plugin HTTP API **blocks** cloud metadata addresses (SSRF guard) | Benign |
| secret-paths: `plugin-menu-checked.test.js:133`, `fileicons/icons_gen.go:36` | A Lua variable named `state = "checked"`; an icon mapping for `.npmrc` file names | Benign false positives |
| `Makefile` | `go build/test/vet`, `gofmt`, `golangci-lint`; docker chaos targets (not used) | Benign |
| `.github/workflows/ci.yml` | go vet, golangci-lint (latest), `go test ./...`, `go test -race ./...`, pnpm functional/integration/LSP lanes | Benign |
| `scripts/install-prerequisites.sh` | Installs ripgrep via the system package manager; only in CI, not run here | Benign, not run |
| `flake.nix` | nixpkgs / flake-utils inputs only | Benign, not run |
| Go test helpers (`tests/e2e/harness_test.go`; `exec.Command` in e2e/ui tests) | Harness writes sample files to `t.TempDir()`; the exec calls run only `git` on temp repos, `rg`, and `sh -c "exit N"` | Benign |
| No `func init()` / `TestMain` side effects found in `tests/e2e`, `internal/ui`, `internal/core/buffer` | — | Benign |

Overall verdict: **no malicious code found**. Only Go build/test/lint commands were run.
