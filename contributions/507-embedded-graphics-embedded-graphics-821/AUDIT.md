# AUDIT — embedded-graphics/embedded-graphics @ 9c5bbcb (shallow clone, 2026-10-01)

`python3 tools/audit_repo.py /home/user/work/embedded-graphics` — 159 text files scanned.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (build.rs, install hooks) | `find -name build.rs` → none; workspace = root crate + `core` | benign — no build scripts |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none (0 bytes) | n/a |
| Pattern findings | none | n/a |
| `justfile` | test = `cargo test --workspace`, fmt = `cargo fmt --all -- --check`; link check / example generation not run here | benign |
| dev-dependencies (crates.io) | standard crates only (arrayvec, criterion etc. per Cargo.toml) | benign |

Verdict: nothing suspicious; safe to build/test.
