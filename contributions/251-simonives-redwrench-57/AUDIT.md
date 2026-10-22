# AUDIT: simonives/redwrench @ ed406f2 (main, 2026-10-22)

`python3 tools/audit_repo.py`:

| Surface | Result |
|---|---|
| build.rs | `include!("src/cli.rs")` + clap_mangen writes a man page to OUT_DIR. Harmless |
| npm lifecycle hooks | none |
| Committed binaries | none |
| Pattern findings | none |

Ran locally: `cargo test`, `cargo clippy --all-targets -- -D warnings`, `cargo fmt --check`. Dependencies from crates.io via Cargo.lock.

Verdict: nothing suspicious.
