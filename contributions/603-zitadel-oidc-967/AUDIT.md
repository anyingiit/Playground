# AUDIT — zitadel/oidc (commit 7cf807b, shallow clone)

`python3 tools/audit_repo.py /home/user/work/oidc` → 193 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none found; pure Go module, no `init`-time network code in test helpers touched | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none (0 bytes) | benign |
| Pattern findings | none | benign |

Manual check: only `go test`/`go vet` on `pkg/client`, `pkg/http` are run; test files use `httptest` local servers only. `.github/scripts/check-otel-k6-compat.sh` not executed.

Verdict: **safe to build/test.**
