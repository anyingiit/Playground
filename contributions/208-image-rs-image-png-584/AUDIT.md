# AUDIT: image-rs/image-png @ b2f10c6 (master, 2026-09-23)

`python3 -I tools/audit_repo.py image-png` (1267 text files):

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (build.rs etc.) | none in the crate (no build.rs, no proc-macros) | benign |
| npm lifecycle hooks | none | benign |
| Committed binaries | none flagged (test PNG fixtures only) | benign |
| Pattern findings | none | benign |
| `.cargo/config.toml` | only sets `wasmtime` runner for wasm32-wasip1 target, not used on host | benign |
| Dependencies | crc32fast, fdeflate, flate2, bitflags, no other runtime deps from crates.io (well-known image-rs deps) | benign |

Verdict: nothing suspicious; safe to build and run `cargo test` locally.
