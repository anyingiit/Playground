# Audit — go-jet/jet (shallow clone, master, 2026-10-01)

`python3 tools/audit_repo.py /home/user/work/jet` — 323 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none | benign |
| Pattern findings | none | benign |

Manual review: pure Go library; only `go test` of `./mysql` and `./internal/jet` package unit tests run (no DB, no cgo, no `go generate`, no TestMain network setup in those packages). CI workflows (`.github/workflows/*.yml`) only run gosec / golangci-lint / CodeQL. Verdict: safe to build and test.
