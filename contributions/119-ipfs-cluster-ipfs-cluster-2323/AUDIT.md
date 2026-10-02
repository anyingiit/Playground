# Audit — ipfs-cluster/ipfs-cluster @ 60b35f2

Tool: `python3 tools/audit_repo.py /home/user/work/ipfs-cluster` (233 text files).

- Auto-executing surface (install/build/test hooks): none. No npm lifecycle hooks. No committed binaries.
- Pattern hits: 6 × long-base64-blob — all are libp2p test identity private keys in `config/identity_test.go` and `sharness/config/*/identity.json`. These are well-known test fixtures, not payloads.
- go.mod: no `replace` directives; `go 1.26` directive; the go1.26.0 toolchain is fetched from the official Go proxy (golang.org/toolchain).
- `go:generate` (protoc, stringer) exists but was not run; only `go test`/`go vet` on `./api/rest/...` and `./api/pinsvcapi/...` were run. The Makefile and sharness were not used.
- CI: only `.github/workflows/tests.yml`.

Verdict: **safe** to build and run the targeted Go tests.
