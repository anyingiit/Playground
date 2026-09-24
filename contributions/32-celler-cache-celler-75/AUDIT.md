# Malicious-code audit — celler-cache/celler @ 8d1ea58

Tool: `python3 /home/user/Playground/tools/audit_repo.py celler` (167 tracked files).

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (setup.py, package.json, Makefile, conftest) | tool: none; manual `find -name build.rs` in repo: none | benign |
| npm lifecycle hooks | none (no JS) | benign |
| Committed binaries | none | benign |
| Pattern findings | none | benign |
| `.cargo/config.toml` | only `rustflags = ["--cfg", "tokio_unstable"]` | benign |
| `.envrc` | nix-direnv `source_url` with pinned sha256 — only used by direnv, not run here | benign (not executed) |
| Git dependency `nix-daemon` from `codeberg.org/blitz/gorgon` (maintainer's own repo, pinned rev f42f79a) | inspected checkout: no Cargo build script (`nix-supervisor/src/entity/build.rs` is a normal module, and not a `build =` target) | benign |
| crates.io dependencies | standard, pinned by Cargo.lock; fetched with `cargo fetch` into work-dir CARGO_HOME | accepted (normal ecosystem risk) |
| CI (`.github/workflows/book.yml`, hercules-ci via flake) | nix builds of book / `cargo test`; nothing downloaded by tests | benign |

Verdict: **no malicious code found**; safe to build and run `cargo test -p attic-client`.
