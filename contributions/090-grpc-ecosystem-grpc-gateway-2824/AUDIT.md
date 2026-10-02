# Malicious-code audit — grpc-ecosystem/grpc-gateway @ 80a27b1 (main, shallow clone)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/grpc-gateway` (532 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported | n/a |
| `examples/internal/browser/package.json` postinstall `playwright install chromium` | Only for the browser e2e example; not touched or run (no npm install performed) | benign, not executed |
| Committed binaries | none | n/a |
| Pattern findings | none | n/a |

Manual checks on the code that is compiled/run by the tests used here
(`internal/httprule`, `internal/descriptor`, `protoc-gen-openapiv2/internal/genopenapi`):
no `TestMain`, no `os/exec`, no network use in the test files. Go module dependencies are
fetched from the Go proxy (checksums verified via go.sum).

**Verdict: no malicious code found; safe to run `go test` on the packages above.**
