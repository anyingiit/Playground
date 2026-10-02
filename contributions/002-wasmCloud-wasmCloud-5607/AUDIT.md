# Malicious-code audit — wasmCloud/wasmCloud @ f9b37fc (release: v2.10.0)

Tool: `python3 tools/audit_repo.py` + manual review. **Verdict: no malicious code found; safe to build/test.**

| Hit | Location | Reviewed verdict |
|---|---|---|
| build.rs (auto-exec) | `examples/grpc-hello-world/*/build.rs` | Benign: tonic/prost codegen only; examples are not part of the `wash`/`wash-runtime` build or tests |
| pipe-to-shell | `install.sh` usage comments, test-install-scripts workflow comment | Benign: documented official installer usage; not executed by build/test |
| powershell download | `install.ps1`, `.github/actions/setup-protoc` | Benign: official installer / CI protoc setup downloading from GitHub releases |
| raw IP | `wash-runtime/src/plugin/egress.rs:353` (`169.254.169.254`) | Benign: test asserting cloud-metadata egress is **blocked** |
| secret paths | `~/.kube/config` in xtask e2e + operator Makefile; `~/.docker/config.json` comment | Benign: standard kubeconfig/docker credential lookup for e2e tooling |
| npm hooks / committed binaries | none | — |

What was executed here: `cargo test`/`cargo clippy` on `wash` and `wash-runtime` (their `build.rs`-free crates plus crates.io deps), `cargo +nightly fmt`.
