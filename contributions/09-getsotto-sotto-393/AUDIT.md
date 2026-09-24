# Malicious-code audit — getsotto/sotto @ 452c390

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/sotto-393` (256 text files scanned), plus manual review of everything that runs on `cargo build/test -p sotto-cli`.

Only the Rust CLI crate was built/tested here (`cargo test -p sotto-cli`, clippy, fmt). No npm install, no web/e2e, no Python scripts, no install scripts were executed.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-exec: `web/vitest.config.ts`, `web/playwright.config.ts` | not executed (web not built) | benign (standard test configs) |
| Auto-exec: `web/e2e/global-setup.ts` (`execFileSync`) | read | benign: runs the repo's own `target/debug/examples/e2e_seed` against 127.0.0.1:8099; not executed here |
| npm lifecycle hooks | none | n/a |
| Committed binaries | none | n/a |
| env-dump: `scripts/check-restore`, `scripts/tests/test_cloud_coverage_races.py` | read | benign: copies `os.environ` to pass to child processes in tests; no network exfiltration; not executed |
| pipe-to-shell: `install.sh`/`install.ps1` comments, landing copy | read | benign: documented install instructions for the project's own GitHub releases |
| powershell-download: `install.ps1` | read | benign: downloads release asset + SHA256SUMS + sigstore bundle from the project's own releases and verifies them; not executed |
| raw-ip-url: `crates/server/src/auth/routes.rs:341` | read | benign: test asserting the metadata IP is *rejected* as a redirect |
| secret-paths: comments in server/cli | read | benign: prose containing "local state" |
| `build.rs` files | none in workspace | n/a |
| `.cargo/` | only `audit.toml` (cargo-audit policy) | benign, no `config.toml`, no custom runners/linkers |
| Git/path deps in Cargo.toml | none (crates.io + workspace paths only; Cargo.lock committed) | benign |

**Verdict: no malicious code found. Safe to build and test the `sotto-cli` crate.**
