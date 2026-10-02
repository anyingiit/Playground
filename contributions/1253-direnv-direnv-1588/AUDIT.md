# Malicious-code audit — direnv/direnv @ b00e451 (master, 2026-03-31)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/s2-1253/direnv` (133 text files scanned)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none (0 bytes) | benign |
| Pattern findings | none | benign |
| `GNUmakefile` (manual) | targets `build` (`go build`), `fmt` (`go fmt`, shfmt), `man` (go-md2man), `test-*` (go test, golangci-lint, shell scripts in `test/`), `install`, `dist`; no downloads or network fetches | benign — only `go build` / `go test` / `gofmt` / `go vet` were run, not make |
| `//go:generate` directives | none in the tree | n/a |
| `go.mod` deps | BurntSushi/toml, mattn/go-isatty, golang.org/x/mod, golang.org/x/sys — well-known modules, verified via go.sum | benign |
| Go test setup in `internal/cmd` (`*_test.go`) | plain unit tests, no `TestMain`, no network, only reads `../../version.txt` | benign |
| `.github/workflows/*.yml` | standard CI (setup-go, go build/test, make test-*) — not executed locally | benign |

Verdict: nothing suspicious; safe to build and run the targeted Go tests.
