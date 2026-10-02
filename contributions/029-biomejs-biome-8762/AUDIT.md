# AUDIT — biomejs/biome (HEAD 8d0b990, 2026-09-24)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/biome` (11978 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| `crates/{js,css,json,graphql,html,markdown}_analyze/build.rs` | Auto-generated: emit `cargo:rerun-if-changed` for rule dirs and bump mtime of the group `.rs` file (via `filetime`). No network, no process spawn | Benign |
| `crates/biome_diagnostics_categories/build.rs` | `quote!` codegen of category registry from `src/categories.rs` into `OUT_DIR` | Benign |
| `crates/biome_aria_metadata/build.rs` | Reads committed `aria-data/*.json`, generates Rust into `OUT_DIR` | Benign |
| `crates/biome_wasm/build.rs` | Generates TS bindings for the wasm crate (not built by the tests we run) | Benign |
| `.cargo/config.toml` | Only cargo aliases, `lto` for release, wasm rustflags | Benign |
| `packages/@biomejs/js-api/vitest.config.ts` | JS test config, not used (we run only cargo tests) | n/a |
| pipe-to-shell in `.github/workflows/release_*.yml` | wasm-pack installer in release CI only; not executed locally | Benign |
| "secret-paths" in `crates/biome_service/src/db/*.rs` | False positives: doc comments mentioning "local state" | Benign |
| `crates/biome_js_analyze/tests/spec_tests.rs` | Spec harness: parses fixture files, writes `.snap` files; no network/process spawn | Benign |
| npm lifecycle hooks / committed binaries | none | n/a |

Note: running `cargo --version` in the repo made rustup auto-install the pinned toolchain 1.98.1 (rust-toolchain.toml) — that is rustup behaviour, no repo code ran.

Verdict: nothing malicious found; safe to build and run `cargo test -p biome_js_analyze`.
