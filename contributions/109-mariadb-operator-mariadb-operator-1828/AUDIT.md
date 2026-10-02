# Audit — mariadb-operator/mariadb-operator @ b04f95f3 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/mariadb-operator` (933 text files) + manual review of Makefile / make/*.mk targets that will be run (`make test`, `make gen`/`manifests`/`code`, `make lint`), `.github/workflows/ci.yml`, `.agents/skills/*`.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported; Go module has no `init`-time network/exec in test helpers relevant to `api/`, `pkg/` unit tests | benign |
| npm lifecycle hooks / committed binaries | none | benign |
| make/deps.mk:87 `curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/HEAD/install.sh \| sh` | Official golangci-lint installer, only run by `make golangci-lint` (dependency of `make lint`), installs into `./bin` (LOCALBIN). Prefer `go install`/prebuilt with pinned `GOLANGCI_LINT_VERSION` if lint is needed | benign (upstream official installer) |
| Makefile:51 `DOCKER_CONFIG ?= $(HOME)/.docker/config.json` | Variable used by docker/release targets we will not run | benign / not run |
| make/dev.mk:136 `KUBECONFIG=$(HOME)/.kube/config` | Env for `make init`/agent local run against KIND; not run here | benign / not run |
| .vscode/launch.json:144,171 `KUBECONFIG` | Editor debug configs | benign / not run |
| pkg/galera/client/client.go:35 | False positive (error string "getting local state") | benign |
| make/deps.mk other targets (`envtest`, `ginkgo`, `controller-gen`, ...) | `GOBIN=./bin go install <module>@<version>` from proxy.golang.org (envtest uses `@latest`) | benign |
| `.agents/skills/*` (`.claude/skills` symlink) | Markdown skills (PR review, comment, release notes); only instruct agents, contain no executable payload | benign |
| go.mod `go 1.27.0` | Host Go 1.24.7 auto-downloads go1.27.0 toolchain via GOTOOLCHAIN=auto (verified working) | ok |

Verdict: nothing malicious; safe to run `go build`, `make code`/`make manifests`/`make gen` (controller-gen etc. via `go install`), `make test` (ginkgo + envtest binaries) with -j2-ish concurrency. Integration tests (`make test-int*`) need a KIND cluster + MetalLB and will not be run here.
