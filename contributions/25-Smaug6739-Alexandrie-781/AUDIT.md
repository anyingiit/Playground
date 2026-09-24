# Audit — Smaug6739/Alexandrie (shallow clone of main @ ccf5603)

Tool: `python3 /home/user/Playground/tools/audit_repo.py alexandrie` (369 text files scanned) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported | benign |
| `frontend/package.json` postinstall = `nuxt prepare` | standard Nuxt type generation | benign — frontend not installed/run here |
| `docs/package.json` postinstall = `nuxt prepare` | same | benign — not run |
| Committed binaries | none | benign |
| Pattern findings | none | benign |
| `Makefile` | only `go run`, `bunx nuxt dev`, `minio server`, `migrate create` targets; none used | benign |
| Go `func init()` / `go:generate` in backend | none found (`grep -rn`) | benign |
| `backend/go.mod` dependencies | well-known modules (gin, minio-go, sqlx, golang-migrate, go-mail, testify …) fetched via the Go module proxy with go.sum verification | benign |
| `backend/tests/*` | integration tests that hit a running API at BaseURL; not run (need MySQL + server) | benign |

What was executed: only `go test` / `go vet` / `gofmt` on `backend/app` (the package touched), using an in-process `httptest` fake S3 server — no network services, no frontend install.

**Verdict: no malicious code found; safe to build/test the Go backend package.**
