# Malicious-code audit — zerobrewhq/zerobrew @ d9c8b0a

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/zerobrew` (102 text files scanned)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | tool reported none; `find . -name build.rs` → none; no `.cargo/config*`; no `[build-dependencies]` in workspace crates | benign — nothing runs at build time from the repo itself |
| `install.sh:424` `curl https://sh.rustup.rs \| sh -s -- -y` | user-facing installer that installs rustup if cargo is missing; only runs when a user invokes `install.sh` manually; not used by cargo build/test | benign (official rustup URL), not executed here |
| `site/src/_data/install.json:4` `curl -fsSL https://zerobrew.rs/install \| bash` | static website data (install instructions shown on the docs site) | benign, not executed |
| `Justfile` | wrapper recipes (`fmt`, `lint`, `test`, `install` → `cargo build` + copy binary, `reset`/`uninstall` use sudo/rm on zerobrew dirs) | benign; not used — cargo invoked directly |
| `install-completions.sh` | writes shell completion scripts from `zb completion <shell>` to user shell dirs | benign; not executed |
| `.github/workflows/{ci,test,homebrew-compat,release}.yml` | standard fmt/clippy/cargo-audit/build/test/release steps, no fetch-and-exec of unknown scripts | benign |
| `zb_cli/tests/integration.rs` | integration tests run the built `zb` binary against real Homebrew bottles; all network tests are `#[ignore]` | benign; ignored tests not run here |
| `Cargo.lock` dependencies | 323 crates, all from crates.io registry, no git sources | standard ecosystem crates |
| Committed binaries | none | — |

Conclusion: nothing suspicious; safe to build and run `cargo fmt/clippy/test` (non-ignored tests).
