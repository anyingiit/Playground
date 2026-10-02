# Malicious-code audit — gosnmp/gosnmp @ d2a3184e8a0f (2026-09-19)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/gosnmp` (66 text files scanned)

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported; Go has no install hooks; no `init()` network/exec code in package | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none (0 bytes) | benign |
| long-base64-blob `v3_usm_test.go:178,185` | hex-encoded SNMPv3 test packets passed to `hex.DecodeString` and unmarshalled | benign (test fixtures) |
| long-base64-blob `helper_test.go:547` | base64 of a captured SNMP response used as a parser fixture | benign (test fixture) |
| `Makefile` | `go test ./...` + license-header awk check | benign |
| `build_tests.sh`, `local_tests.sh`, `snmp_users.sh` | CI helpers (set up snmpd users / run tests); not executed here | benign, not run |
| `.github/workflows/*` | go generate / golangci-lint / go test / net-snmp tests | benign |

Only `go test`, `go vet`, `gofmt`, `golangci-lint` and `make lint` were run locally. Verdict: **no malicious code found.**
