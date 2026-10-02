# Audit — Harry-kp/vortix @ 51b2eb0 (main, 2026-10-02 02:35 +0530)

Tool: `python3 /home/user/Playground/tools/audit_repo.py vortix` (165 text files) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-exec surface: no `build.rs` in any workspace crate, no npm hooks, 0 committed binaries | `find -name build.rs`, `grep build= Cargo.toml` | benign — nothing runs at build time from the repo itself |
| `.cargo/config.toml` | only alias `xtask = "run --package xtask --quiet --"` | benign (not invoked by us) |
| `rust-toolchain.toml` | pins 1.91.0 + rustfmt/clippy (rustup downloaded official toolchain) | benign |
| pipe-to-shell in `.github/workflows/install-sanity.yml`, `release.yml`, `scripts/p0-journey.sh`, `tests/integration/Dockerfile` | official rustup / cargo-dist / project's own release installer, CI/release only | benign; not executed by `cargo test` |
| raw IP `169.254.169.254` in `scripts/vpn-lab.sh` | DigitalOcean metadata endpoint for a VPN test lab script | benign; not executed |
| secret-paths in `scripts/vpn-lab.sh` | comment about local SSH key override for the lab; a warn message | benign; not executed |
| `.claude/settings.json` + `.claude/hooks/guard-merge.sh` | maintainer's agent permissions; hook only blocks `gh pr merge --auto/--admin`; PostToolUse rustfmt | benign; not used here |
| `scripts/install-hooks.sh` / `pre-commit.sh` | symlinks pre-commit hook (fmt/clippy/gitleaks/tests) | not installed here |
| Test under change (`cli/profiles.rs` `mod tests::test_format_elapsed`) | pure unit test, no fs/network | benign |

Verdict: **no malicious code found**. Only ran `cargo fmt`, `cargo clippy`, `cargo test -p vortix` (third-party crates from crates.io via `Cargo.lock`).
