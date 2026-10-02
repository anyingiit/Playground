# AUDIT — parquet-go/parquet-go (depth-30 clone of main @ eaeafbd)

`python3 tools/audit_repo.py /home/user/work/parquet-go` — 481 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none found; pure Go module, no cgo build scripts, no TestMain downloads | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries: `testdata/shredded_variant/*.variant.bin` (4–36 B), `compress/testdata/pngdata.bin` (50 KB) | test fixtures read as data by tests (variant encoding cases, compression corpus); never executed | benign |
| Pattern findings | none | — |

Manual check: `Makefile` targets only run `go fmt`, `go tool modernize`, `go test`; CI workflow `test.yml` runs `go test`/`go vet`-style commands. Nothing fetches or executes remote code during tests.

Verdict: **safe to build and test.**
