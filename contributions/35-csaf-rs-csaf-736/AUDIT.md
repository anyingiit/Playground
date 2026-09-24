# Malicious-code audit — csaf-rs/csaf @ cd5bb07f1d8fb64115db5cf07728a1d46b3ab0f5 (+ submodule oasis-tcs/csaf @ e0da5a98)

Tool: `python3 /home/user/Playground/tools/audit_repo.py <dir>` on the main repo and on the `csaf/` submodule, plus manual review
of everything that runs on `cargo build` / `cargo test`.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| `csaf-ffi/build.rs` (auto-exec build script) | Empty `fn main() {}` with a comment ("no-op build.rs kept for future extension") | Benign |
| `csaf-rs/build/main.rs` + `build/ssvc_validation.rs` (declared via `build = "build/main.rs"`; not flagged by the tool, found manually) | Only prints two `cargo:rerun-if-changed` lines and parses `ssvc::SELECTION_LIST_SCHEMA` with `serde_json` (panics if invalid). No I/O, network, process spawning or env access | Benign |
| npm lifecycle hooks | none (no package.json in the Rust workspace) | n/a |
| Committed binaries | none in either tree | n/a |
| Pattern findings (curl/wget/eval/base64/obfuscation…) | none in either tree | n/a |
| `csaf/` submodule (OASIS CSAF spec repo: JSON schemas + test documents) | 0 auto-exec surfaces, 0 pattern hits; used only as JSON test data via relative paths from `csaf-rs/src/**/testcases.generated.rs` | Benign |
| Test dependencies (`rstest`, `criterion`, `tempfile`) and proc-macro deps | Well-known crates from crates.io, pinned in `Cargo.lock` | Benign |
| CI scripts (`scripts/`, `.github/workflows/`) | Not invoked by `cargo test`; not run here | Not executed |

**Verdict:** nothing suspicious; safe to build and run `cargo test` / `cargo clippy` locally.
