# Malicious-code audit — thebanri/limoni @ 730214bd07789d8b07904dd00a1682ed65b89575

Clone: `git clone --depth 20 https://github.com/thebanri/limoni.git` (default branch `main`, tag v0.9.0).
Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/limoni` (460 text files scanned),
run **before** any `go build` / `go test`. Then manual review of everything that executes during build/test.

| Hit / surface | Reviewed | Verdict |
| --- | --- | --- |
| `benchmarks/runners/ratatui/build.rs` (cargo build script) | Read in full: reads `Cargo.lock`, extracts the `ratatui` version, emits `cargo:rustc-env=RATATUI_VERSION=...`. No network, no process spawning, no file writes. Not built by this contribution (Rust runner is a separate benchmark, not part of `go test`). | Benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none (0 bytes) | n/a |
| Pattern findings (curl/eval/base64 exec/etc.) | none | n/a |
| `func TestMain` | none in the repo | n/a |
| `func init()` in `session/registry.go`, `session/session_test.go`, `core/grapheme/grapheme.go`, `core/grapheme/mode.go` | Type registration, rune-property table fill, reading `LIMONI_GRAPHEME` env var. | Benign |
| `exec.Command` in tests: `cmd/limoni/main_test.go:146` | Scaffolds each project template into `t.TempDir()`, adds a `replace` to the local checkout, and runs `go mod tidy/build/vet/test` there. Only effect: downloads the module's declared deps (`golang.org/x/crypto`, `golang.org/x/sys`) through the Go proxy. | Benign |
| `go.mod` deps | Only `golang.org/x/crypto v0.55.0`, `golang.org/x/sys v0.47.0` (official Go sub-repos). | Benign |
| `.github/workflows/*` (benchmarks, ci, pages, platform-smoke) | Not executed locally. | n/a |

**Verdict: no malicious code found. Safe to build and test.** Changed code in this contribution touches only
`graphics/graphics.go`, `graphics/graphics_test.go`, `CHANGELOG.md`.
