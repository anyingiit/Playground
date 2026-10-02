# AUDIT — restic/restic @ 5127c4a (2026-09-25), shallow clone

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/s2-1255/restic` (1277 text files scanned), then manual review of everything that runs during `go test ./internal/backend/sftp/...`, `go vet`, `gofmt`.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (npm/setup.py/build.rs) | none found | n/a |
| Committed binaries | none (0 bytes) | benign |
| `go:generate` directives | none in repo | n/a (not run anyway) |
| `Makefile` | `go run build.go` / `go test ./cmd/... ./internal/...` only | benign; not used (ran `go test` directly) |
| `build.go` | release build helper, not invoked | not run |
| hex-escaped blobs: `internal/repository/crypto/crypto_int_test.go:38`, fuzz corpus `FuzzSaveLoadBlob/...` | crypto test vectors / fuzz seed | benign test data |
| long base64: `internal/fs/sd_windows_test_helpers.go:16-21` | Windows security-descriptor test fixtures (windows-only build tag) | benign test data |
| powershell downloads in `.github/workflows/tests.yml:119-144` | CI-only Windows setup (seaweedfs, rclone, tar from restic/test-assets) | benign, CI only, not executed here |
| secret-paths: changelog text & s3.go comment mentioning `~/.aws/credentials` | documentation strings only | benign |
| Package under test `internal/backend/sftp`: `init()` only registers options; tests run local `sftp-server -e` if present (`RESTIC_TEST_SFTPPATH`) | read sftp_test.go, config.go, internal/test/vars.go | benign |
| go.mod deps | fetched from proxy.golang.org with go.sum verification | benign |

Verdict: **no malicious code found**; safe to build and run targeted tests.
