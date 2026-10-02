# AUDIT — cloudflare/pint @ 373a5a2

`python3 tools/audit_repo.py /home/user/work/pint` (259 text files), run before any build/test.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported; Makefile targets are plain `go build/test/tool` | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none | benign |
| raw-ip-url `internal/checks/promql_series_test.go:49` `http://127.127.127.127:9999` | loopback-range address used as an unreachable Prometheus in a unit test | benign |

Extra manual check: `go tool` invocations in Makefile use pinned modfiles under `tools/*/go.mod` (golangci-lint, deadcode, betteralign) — standard tooling. Test harness (`cmd/pint` testscripts) only runs the pint binary on local fixtures.

**Verdict: no malicious code found; safe to build/test.**
