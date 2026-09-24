# Malicious-code audit — complytime/complyctl @ 20fc2d4

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/complyctl` (3122 text files) + manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` (auto-exec surface) | pre-commit hooks (trailing-whitespace, go-fmt, go-unit-tests, local SPDX script); only runs if `pre-commit install` — not installed/used here | benign |
| npm lifecycle hooks | none | n/a |
| committed binaries | none | n/a |
| long-base64-blob ×3 `vendor/golang.org/x/crypto/ssh/kex.go` | RFC 3526 Oakley DH group primes | benign |
| pipe-to-shell ×2 `vendor/github.com/spf13/cobra/Makefile`, `vendor/github.com/goccy/go-yaml/Makefile` | upstream golangci-lint install hints in vendored libs' own Makefiles; never invoked by complyctl build/test | benign |
| powershell-download ×8 (go-tuf fetcher, x509 root certs) | TUF `DownloadFile` API / PEM cert data | benign (false positive) |
| raw-ip-url ×3 (otel .lycheeignore, go-openapi doc comments) | documentation examples | benign |
| secret-paths ×7 (docker config.json lookups in oras/ggcr/docker cli, comments) | standard registry credential lookup in vendored libs; not exercised by the tests run | benign |
| webhook/paste/tunnel ×16 (go-openapi "RequestBinder") | false positive on "bin" substring | benign |

Test-time surface reviewed manually: `Makefile` `test-unit` = `go test -race ./...` (no downloads; deps are vendored, `-mod=vendor`); `pkg/provider/export_test.go` (test helpers only); `cmd/complyctl/cli/root.go` `init()` only creates a lazy logger; no `TestMain` in the packages under test. Tests only create temp dirs/executable shell stubs.

**Verdict: no malicious code found; safe to build and run unit tests.**
