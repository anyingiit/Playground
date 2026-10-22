# AUDIT — charmbracelet/lipgloss (clone @ 6a419c6, 2026-09-11, `git clone --depth 1`)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/s2-1258/lipgloss` (98 text files scanned)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported; manually checked: no `//go:generate`, no `func init` in non-example code, no `TestMain`, no Makefile (only `Taskfile.yaml`: `golangci-lint run`, `go test ./...`) | benign |
| npm lifecycle hooks | none (pure Go module) | n/a |
| Committed binaries | none (0 bytes) | benign |
| Pattern findings | none | benign |
| `.github/workflows/*` | reusable workflows from `charmbracelet/meta` (build/lint/coverage/release); not executed locally | benign |
| Dependencies (`go.mod`) | charmbracelet/colorprofile, x/ansi, x/term, ultraviolet, rivo/uniseg, etc. — all well-known Charm deps fetched from proxy.golang.org; reviewed `colorprofile@v0.4.3/env.go` (`Detect` → `tmux info` subprocess, the subject of the issue) | benign |

Verdict: nothing suspicious; safe to build and run `go test` / `go vet` locally.
