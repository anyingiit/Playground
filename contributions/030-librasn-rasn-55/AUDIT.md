# Malicious-code audit — librasn/rasn (commit d83db21, 2026-09-24)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/rasn` (213 text files) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (build.rs, setup hooks) | `find . -name build.rs` → none in workspace; no npm lifecycle hooks | benign (nothing runs at build time except rustc + proc-macros in `macros/`) |
| Proc-macro crates `macros/`, `macros/macros_impl` | derive macros generating codec impls from `syn` ASTs; no fs/net/process access | benign |
| Committed binaries (28 small `.bin` files in `tests/data`, `standards/pkix/tests/data`, `fuzzing/in`) | 2 B – 13.7 KB, loaded only via `include_bytes!` as fuzz-regression inputs to `ber::decode` | benign (test data, never executed) |
| `justfile` | wraps `cargo fmt/clippy/build/test/doc`; `toolchain` recipe runs `rustup` (not used here) | benign |
| `.github/workflows/*.yml`, `.github/semver-checks-shim/cargo-semver-checks` | CI: install just/cross/valgrind, run just recipes; shim only forwards to real cargo-semver-checks with default features | benign (not run locally) |
| Pattern findings (curl\|sh, base64 blobs, eval, network in tests) | none reported | — |
| Git dev-dependency `cryptography-x509` (pyca/cryptography tag 44.0.2) | used by `standards/pkix` tests for cross-checking; upstream pyca repo, pinned tag | benign |
| Dependencies | `Cargo.lock` from crates.io only; optional `rasn-compiler` (feature `compiler`) is the upstream sister project | benign |

**Verdict: no malicious code found; safe to build and test.**
