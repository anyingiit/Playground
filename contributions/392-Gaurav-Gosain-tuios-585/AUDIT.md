# AUDIT — Gaurav-Gosain/tuios @ 9c8f0df

`python3 tools/audit_repo.py` (4184 text files). Same clone as contribution 391. Ran only `go build ./...`, `go vet` and `go test` for `./internal/input/ ./internal/config/ ./internal/app/ ./cmd/tuios/` (no e2e, no Playwright, no install scripts).

| Hit | Reviewed | Verdict |
|---|---|---|
| `clienttests/playwright.config.mjs` | browser e2e config, not run | not run |
| `install.sh`, `install-web.sh`, `cmd/tuios/update.go` (`curl … \| bash` strings) | installer usage text printed to users | benign, not run |
| `rm -rf` / `curl evil \| sh` strings in `*_test.go`, `internal/risk` | test fixtures for the risk detector and shell-quoting tests | benign |
| `internal/theme/tints_gen.go` hex blob | generated colour table constant | benign |
| `vt/testdata/corpus/*.bin`, `plot/world.bin`, transcriptview `.bin` fixtures | terminal byte streams / map data read by tests | benign |
| `TestMain` in internal/input, config, terminal | `testutil.RunIsolated` points XDG dirs at a temp dir | benign |

Verdict: no malicious code found.
