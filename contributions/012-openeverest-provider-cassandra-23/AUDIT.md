# Malicious-code audit — openeverest/provider-cassandra @ b6ffbbf

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/provider-cassandra` (59 text files)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (install/build/test) | none reported | benign |
| npm lifecycle hooks | none (Go project) | n/a |
| Committed binaries | none (0 bytes) | benign |
| Pattern findings | none | benign |
| `gen.go` `//go:generate go tool provider-sdk generate` | runs the provider-sdk tool from go.mod (openeverest module) only on `make generate` | benign |
| `Makefile` | `test-unit` = `go test -race ./...`; tool installs via `go install` pinned versions; `install-crds` kubectl-applies upstream openeverest CRDs (not run here) | benign |
| `.github/actions/setup-k8s-tools` | downloads kubectl/chainsaw/k3d with sha256 verification (CI only) | benign |
| `Dockerfile` | standard golang builder + distroless | benign |
| Test files `internal/provider/*_test.go` | pure unit tests with fake controller-runtime client, no network/exec | benign |
| go.mod deps | k8ssandra, openeverest, k8s, controller-runtime, testify — well-known | benign |

Verdict: **no malicious code found**; safe to run `go test` / `go build` / `make generate`.
Go deps and toolchain (go1.26.4 via GOTOOLCHAIN=auto) were downloaded into a private cache `/home/user/work/gocache` (deleted afterwards).
Cleanup: /home/user/work/gocache (toolchain, modules, build and lint caches, ~3 GB), bin/ and cover.out were deleted after verification.
