# Audit — LaurenzV/hayro @ febaff5 (2026-10-01)

`python3 tools/audit_repo.py /home/user/work/hayro` (297 text files)

| Hit | Reviewed | Verdict |
|---|---|---|
| `hayro-jpeg2000/src/j2c/build.rs` flagged as cargo build script | Opened file: it is a normal library module (`j2c::build`, code-block setup), not a crate-root `build.rs`; no crate in the workspace declares a build script | Benign |
| `.github/workflows/deploy-pages.yml:40` curl wasm-pack installer \| sh | CI-only Pages deploy job, official wasm-pack installer; never run locally | Benign |
| npm hooks / committed binaries | none | — |

Verdict: no malicious code found; safe to `cargo build/test` the `hayro-syntax` crate.
