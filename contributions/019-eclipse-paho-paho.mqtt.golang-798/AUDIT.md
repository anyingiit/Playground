# Malicious-code audit — eclipse-paho/paho.mqtt.golang (master @ b1a3a41)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/paho` (83 text files scanned)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | none reported; Go module has no build scripts, no `go:generate` run by tests, no cgo | benign |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none (0 bytes) | benign |
| Pattern findings | none | benign |
| Manual: `unit_client_test.go` `init()` | starts `net/http/pprof` on `localhost:6060` during tests (debug aid, loopback only) | benign |
| Manual: `fvt*_test.go` | connect to a local MQTT broker configured in `fvt/` (skip/fail without broker); no downloads | benign |
| Manual: `go.mod` deps | gorilla/websocket, golang.org/x/net, golang.org/x/sync — well-known | benign |
| `.github/workflows/codeql-analysis.yml` | CodeQL only, not invoked by tests | benign |

**Verdict: no malicious code found — safe to build and run tests.**
