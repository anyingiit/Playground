# AUDIT — prometheus/common @ ca4f6e1 (main, 2026-09-28)

`python3 tools/audit_repo.py /home/user/work/s2-1254/common` — 177 text files scanned:
no auto-executing hooks, no npm lifecycle hooks, no committed binaries, no pattern findings.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Go has no install/build hooks; `go test ./expfmt/...` only compiles the package + its tests | `expfmt/*_test.go` use only stdlib, client_model, protobuf, testify-free table tests | benign |
| `//go:generate` directives | `grep -rn go:generate` → none in `expfmt` | benign |
| `Makefile` `generate-testdata` (`cd config && go run generate.go`) | not invoked by us; generates TLS test certs for `config` | benign / not run |
| `Makefile.common` `curl … promu`, `curl … golangci-lint install.sh` | standard Prometheus shared Makefile; downloads official release tools only when `make` targets are used; we did not run those targets | benign / not run |
| `.github/workflows/*` | CI only (golangci-lint, tests); not executed locally | benign |
| `expfmt/fuzz.go` (`//go:build gofuzz`) | build-tagged fuzz entrypoint, not compiled in normal tests | benign |

Verdict: nothing suspicious; safe to run `go test` / `go vet` / `gofmt` on the `expfmt` package.
