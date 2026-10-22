# AUDIT: vyncint/termlens @ 06cd15d (main, 2026-10-22; same tree as 245)

`python3 tools/audit_repo.py termlens` (172 text files):

| Surface | Result |
|---|---|
| build.rs / proc-macro / install hooks | none |
| npm lifecycle hooks | none |
| Committed binaries | none |
| Pattern findings (pipe-to-shell, env dump, raw IP, secret paths…) | none |

Ran locally: `cargo build`/`test --workspace`, `cargo clippy`, `cargo fmt`, `tools/preflight.sh` (the repo's own gate runner: shell scripts that build fixtures in temp git repos, no network). Dependencies come from crates.io via Cargo.lock.

Verdict: nothing suspicious.
