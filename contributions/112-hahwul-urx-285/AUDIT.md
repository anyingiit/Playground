# Audit — hahwul/urx @ 9e11bf629a97 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/urx` + manual review of Cargo.toml, justfile, scripts/.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (build.rs / npm hooks) | none reported; confirmed there is no `build.rs`, no `[patch]`, no git dependencies in Cargo.toml (all deps from crates.io, locked by Cargo.lock) | benign |
| Committed binaries | none | benign |
| src/filters/url_filter.rs:785 `/.ssh/id_rsa` | string literal in a URL-filter unit test (matches a URL path, never touches the filesystem) | benign |
| src/filters/preset.rs:142-230 `/.npmrc`, `/.pypirc`, `/.docker/config.json`, `/.kube/config` | URL path patterns for the `only-secrets` / `only-config` presets (filter lists for scanned URLs) | benign |
| scripts/version_check.cr, version_update.cr | Crystal release helpers invoked only via `just version-*`; not run here | not executed |
| justfile `test` recipe | `cargo test`, `cargo clippy`, `cargo fmt --check` only | benign |

Verdict: nothing malicious; safe to run `cargo build` / `cargo test` / `cargo clippy` / `cargo fmt`.
Note: some integration/provider tests hit the network (expected per AGENTS.md); only the targeted unit test plus the full suite were run.
