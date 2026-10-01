# AUDIT — open-policy-agent/conftest @ 8345c40

`python3 tools/audit_repo.py /home/user/work/conftest` (191 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none found; Go module, no `init()` network/exec in tests touched | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none | benign |
| `examples/jenkins/Jenkinsfile:6` `curl ... example.com/install.sh \| bash` | documentation example of a Jenkins pipeline, placeholder domain, never executed by build/test | benign |
| Makefile `test` / `lint` | `go test -v ./...`, `golangci-lint run --fix` only | benign |

Only `go test ./downloader/...` (+ `go vet`, `gofmt`) was run locally; tests use local temp git repos (`git::file://`), no network.

Verdict: no malicious code found.
