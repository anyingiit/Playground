# Malicious-code audit — stackrox/kube-linter @ e23dee8 (main, 2026-09-30)

Tool: `python3 /home/user/Playground/tools/audit_repo.py <clone>` (582 text files) → no auto-executing hooks, no npm lifecycle hooks, no committed binaries, no pattern findings. Then manual review of everything that runs on build/test:

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `Makefile` | `deps` (go mod tidy/verify), golangci-lint/goreleaser installed from pinned `tool-imports/*` modules, `go generate`, `go test ./... -race`, e2e targets. No downloads besides Go modules | benign |
| `go:generate` (`pkg/templates/gen.go`, `pkg/config/gen.go`) | `go run ./codegen` — local code generators (`pkg/templates/codegen/main.go`, `pkg/config/codegen/parse.go`) that parse Go source and write `*_generated.go`/params files; only `exec` is running `gofmt`/`goimports`-style formatting of output | benign |
| `e2etests/*.go` (build tag `e2e`) | `sanity_test.go` git-clones github.com/helm/charts and runs the built kube-linter on it; `invalid_object_test.go` runs kube-linter on testdata. Not executed here (only with `-tags e2e`) | benign |
| `e2etests/bats-tests.sh`, `check-bats-tests.sh` | run kube-linter binary on `tests/checks/*.yml` and compare JSON via jq; write to `/tmp/kubelinter` | benign |
| `.github/workflows/*.yaml` | build/lint/test, auto-merge for dependabot (`gh pr merge`), release; yajsv download only in CI SARIF job | benign (not run locally) |
| Unit test setup (`TestMain`/`init` in tests) | only `docs/custom_resource_template_test.go` plus template `init()` registrations — no network/exec | benign |

Verdict: **no malicious code found**; safe to build and run unit tests (`go test`) with GOCACHE inside the work dir.
