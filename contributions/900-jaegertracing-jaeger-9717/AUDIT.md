# Audit — jaegertracing/jaeger @ a58fb8e (shallow clone)

`python3 tools/audit_repo.py /home/user/work/jaeger` — 1766 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none | benign |
| secret-paths ×5 in `examples/otel-demo/opensearch-expand-volume.sh` (`local statefulset_json=…`, `local state`) | regex matched bash `local` keyword; script is a k8s volume helper for the demo, never run by tests | benign (false positive) |

What is executed here: only `go test` on `internal/storage/v2/grpc/...` (and `go vet`/gofmt on touched files). Go test has no install hooks; the packages' TestMain only run goleak checks. Verdict: **safe to build/test**.
