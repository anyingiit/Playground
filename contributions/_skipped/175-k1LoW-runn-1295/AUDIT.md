# Audit — k1LoW/runn @ 651af61 (shallow clone)

`python3 tools/audit_repo.py /home/user/work/runn` — 348 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none found | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none | benign |
| long-base64-blob `http_test.go:266` | a long repeated "veryvery…" step name string used as test data | benign |

Manual: only `go test` of targeted packages is run (no `make cert`, no integration tag / docker). Go test files in root package use httptest/local servers only for the tests run. Verdict: **safe to build and run targeted tests**.
