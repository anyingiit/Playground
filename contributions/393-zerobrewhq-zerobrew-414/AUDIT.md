# AUDIT — zerobrewhq/zerobrew @ c24141a

`python3 tools/audit_repo.py` (128 text files): no build scripts, no npm hooks, no committed binaries.

| Hit | Reviewed | Verdict |
|---|---|---|
| `install.sh:450` `curl https://sh.rustup.rs \| sh` | the end-user installer bootstraps rustup when building from source; not run | benign, not run |
| `site/src/_data/install.json` `curl … \| bash` | install command shown on the website | benign |

Tests run: `cargo test` / `cargo clippy` for the workspace (unit tests only; `--ignored` integration tests need network and were not run). Tests use `tempfile` and touch only temp dirs.

Verdict: no malicious code found.
