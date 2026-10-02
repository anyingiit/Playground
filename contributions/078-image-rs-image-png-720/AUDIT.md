# AUDIT — image-rs/image-png @ b2f10c6

`python3 tools/audit_repo.py /home/user/work/image-png` (1267 text files):

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (build.rs, npm lifecycle, etc.) | none found; no build.rs in crate root | benign |
| Committed binaries | 0 bytes flagged (test PNGs are data files read by tests) | benign |
| Pattern findings | none | benign |
| `.cargo/config` | only sets `wasmtime` runner for `wasm32-wasip1` target (not used here) | benign |
| `.github/workflows/rust.yml` | standard cargo build/test/fmt/clippy steps | benign |

Verdict: nothing suspicious; safe to build and test (`cargo test`, deps from crates.io).
