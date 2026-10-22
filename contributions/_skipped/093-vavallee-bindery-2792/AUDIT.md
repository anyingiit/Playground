# Audit — vavallee/bindery @ f86bbf8 (main, shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/bindery` + manual review of what `go test ./internal/db/...` executes (no `TestMain`, no `exec.Command` in `internal/db`).

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` (gitleaks, golangci-lint, eslint, whitespace hooks) | Standard upstream hooks; pre-commit is not installed/run here | benign / not run |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| powershell-download (14) | i18n strings `downloadFile` and OPDS `DownloadFile` handler names | benign (false positive) |
| raw-ip-url (30) | SSRF-guard tests and docs using 169.254.169.254 / TEST-NET / documentation IPs as rejected inputs | benign |
| secret-paths (1) | a code comment in `bulk_autograb_refusal_test.go` | benign |
| webhook (1) | Discord webhook URL literal in a notifier URL-validation test, no network | benign |

Only `go test`, `go vet`, `gofmt` on the Go module were run (no web build, no Makefile targets that download tools).

Verdict: nothing malicious; safe to build and test the Go module.
