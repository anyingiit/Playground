# Malicious-code audit — unstablebuild/rune @ 587cdfd

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/rune` (2249 text files scanned), then manual review of every hit and of the code that runs during `go test` / `make`.

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml`, `internal/ide/idelsp/.pre-commit-config.yaml` | check-yaml, end-of-file-fixer, golangci-lint, gohawk (pinned to a commit), local `make generate` and license checks | benign; pre-commit is not installed or run here |
| 18 committed `tree-sitter.so` files under `internal/ide/syntax/syntaxtest/*` and `internal/ide/idelsp/symbolresolve/go` | Test fixtures: tree-sitter grammars that the syntax tests dlopen. They are only staged by specific tests such as `stageTreeSitterGo` in `ide_test.go`. | benign: these are expected grammar fixtures. I did not run the tests that load them; my test runs were filtered with `-run` |
| `internal/ide/idecmd/expander_test.go:399` "rm -rf / payload" | Name of a test case for string-expansion data. Nothing is executed. | benign |
| `.github/workflows/e2e.yml:37` curl astral.sh/uv \| sh | CI-only uv installer from the official source | benign, not run |
| `cmd/rune/docs/src/components/Install/index.tsx:7` install.sh | Install command shown on the docs website | benign |
| `169.254.169.254` in webfetch `safeclient_test.go` / `fuzz_test.go` | SSRF-block tests that assert the metadata IP is rejected | benign |
| `~/.ssh/id_rsa` in `deploy/*/Dockerfile` | Writes the build-arg SSH key for private-module fetch in deploy images | benign, not run |
| `~/.ssh/id_*` in `internal/workspace/workspacessh/*` | Comments and tests for OpenSSH-style default-key discovery, inside temp/test containers | benign |
| `Makefile` | `BUILD_DATE := $(shell ... go run ./cmd/buildstamp)` runs at parse time on any `make` invocation. `test` = `go test -vet=off ./... -race`, `format` = `go fmt`, `lint` = `golangci-lint run`, `generate` = `go generate` + `npm run keybindings` in docs | benign. I did not invoke `make`; I ran the equivalent `go`/`gofmt` commands directly |
| `.github/actions/setup-build/action.yml` | setup-go plus apt install of X11/GL/ALSA headers | benign |
| `.github/workflows/lint.yml`, `test-linux.yml` | golangci-lint v2.14.0, gohawk, gofmt + license-header scan, `xvfb-run make test` | benign |
| `internal/ide` package: `TestMain` / `init()` in the package being tested | none found | — |

Conclusion: nothing malicious found. I ran only `go test` (targeted with `-run`), `go vet`, `gofmt`, and `golangci-lint` against `./internal/ide/`.
