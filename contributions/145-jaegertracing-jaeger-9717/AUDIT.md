# AUDIT — jaegertracing/jaeger @ a58fb8e (shallow clone)

`python3 tools/audit_repo.py /home/user/work/jaeger` — 1766 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported | n/a |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| secret-paths ×5 in `examples/otel-demo/opensearch-expand-volume.sh` (`local statefulset_json=$2`, `local state=$1`, …) | Yes — bash `local` variable declarations in a demo kubectl helper, matched the regex on the word "local"/"state"; not executed by our tests | Benign (false positive) |

Only `go test` / `go vet` / `gofumpt` on `internal/storage/v2/elasticsearch/...` packages are run. Go test files in those packages contain no `init()`/TestMain that reach network or shell out (manually checked).

Verdict: **no malicious code found**, safe to run targeted Go tests.
