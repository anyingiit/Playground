# Malicious-code audit — stephenafamo/bob @ 13ef1b5 (main, 2026-08-31)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/bob` (363 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (setup.py/build.rs/npm lifecycle/conftest) | none found | benign |
| Committed binaries | none | benign |
| `powershell-download` x2 in `website/package-lock.json` | npm `integrity` sha512 hashes that happen to match the pattern; website (docusaurus) is not built or installed here | benign (false positive) |
| Manual: `os/exec` in Go sources (`test/gen/gen.go`, `gen/language/go.go`) | only run `go env GOMOD`, `go mod init/edit/tidy`, `go <args>` for the code-generation tests | benign |
| Manual: `func init()` / network use in `orm`, `dialect/psql`, root package | none relevant (pgtypes `net` import is for MAC address parsing) | benign |
| CI (`.github/workflows`) | `go test -race ./...` and golangci-lint only | benign |

Only `go test` on `./orm`, `./dialect/...` and the root package and `gofmt`/`go vet` are run here; no database containers, no website build.

Verdict: **no malicious code found**; safe to build/test.
