# Audit — SurgeDM/Surge @ ce77b5de (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/Surge` + manual review of Go test hooks (`TestMain`, `exec.Command`).

| Hit | Reviewed | Verdict |
|---|---|---|
| extension/vitest.config.ts (JS test runner config) | Not executed — only Go code is built/tested here | benign / not run |
| surge_version.exe (25 MB committed binary) | Not referenced by any Go code, test, script or workflow; looks like an accidentally committed build artifact | not executed; worth mentioning to nobody (out of scope) |
| scripts/install.sh:6 `curl … \| sh` | Comment showing the documented install one-liner | benign |
| cmd/cli_test.go:790 raw IP `198.1.1.1:7800` | String assertion in an error-message test; no network | benign |
| `TestMain` in cmd/, internal/{types,probe,config,orchestrator,tui,tui/components} | goleak.VerifyTestMain / isolated temp dirs setup | benign |
| cmd/lock_test.go `exec.Command(os.Args[0], ...)` | Re-runs the test binary itself as a helper process | benign |
| internal/tui/commands.go `open`/`xdg-open` | Opens downloaded file on user request; not hit by tests | benign |

Verdict: nothing malicious; safe to run `go build` / `go test` / `go vet` / gofmt / golangci-lint on the Go module.
