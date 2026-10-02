# AUDIT — emersion/go-smtp @ f08aae7 (shallow clone)

`python3 tools/audit_repo.py /home/user/work/go-smtp` — 19 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (Makefile/scripts/CI-invoked) | none found; only go.mod/go.sum (deps: go-sasl), *_test.go use in-process net.Pipe/listeners | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| Pattern findings | none | n/a |

Manual check: no `init()` side effects / `go:generate` / network fetches in tests. Safe to run `go test` / `go vet` / `gofmt`.
