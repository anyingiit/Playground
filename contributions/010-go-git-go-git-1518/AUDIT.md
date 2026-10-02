# Malicious-code audit — go-git/go-git @ a5f9c22 (main, 2026-09-24)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/go-git` (735 text files) + manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface / npm hooks / committed binaries | none reported (pure Go module, no build.rs/setup.py/package.json at root) | benign |
| `plumbing/transport/ssh/ssh_test.go:125-126` `rm -rf /` | Test table data: asserts that a malicious `git-lfs-authenticate` arg is **shell-quoted** (`'download'\''; rm -rf / ; #'`). String is never executed. | benign (security test) |
| `plumbing/hash/hash_test.go:69,74` long hex blobs | SHA-1 collision test vectors (hex of colliding objects). | benign |
| `plumbing/format/objfile/common_test.go:51` base64 blob | zlib-compressed loose-object fixture decoded by the test. | benign |
| `Makefile:24` `curl ... golangci-lint/install.sh \| sh` | Official golangci-lint installer pinned to `$(GOLANGCI_VERSION)` (v2.13.1); only in `validate-lint` target. Not run by `go test`. I ran golangci-lint via `go run` of the same pinned version instead of piping to sh. | benign |
| `plumbing/transport/http/dumb.go` `downloadFile` | Dumb-HTTP protocol fetcher (library feature), matched on the word "download". | benign |
| `exec.Command` in tests (`remote_test.go:2448`, `internal/test/gitenv`, `plumbing/transport/git`, `tests/objectverify`) | Re-exec the test binary itself with a trace env var; run the local `git` binary with a sanitised env; `git daemon` for transport tests. No network targets beyond localhost. | benign |
| `TestMain` (root, plumbing/object, x/…, tests/objectverify, utils/trace) | Sets trace targets from env, registers a test config loader; objectverify one looks up `git`. | benign |
| Test fixtures | Pulled via Go module `github.com/go-git/go-git-fixtures/v6` (checksummed by go.sum / sum.golang.org). | benign |
| CI (`.github/workflows/*.yml`) | build/test/lint, commit-message regex check, DCO check, CodeQL, scorecard. Nothing invoked by local tests. | benign |

**Verdict: no malicious code found; safe to build and run `go test` locally.**
