# Audit — LargeModGames/spotatui @ 9c46bc0 (main, 2026-09-24)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/spotatui` + manual review.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface: none (no `build.rs`, no `.cargo/config`, no npm hooks) | `find -name build.rs`, `ls .cargo` | benign — nothing runs at build time beyond crates.io deps from `Cargo.lock` |
| `Cargo.toml` git dependencies | `grep 'git =' Cargo.toml` → none | benign |
| Committed binaries | none | benign |
| pipe-to-shell: `install.sh:4`, `.github/workflows/cd.yml:196` | both are comments / release-note text documenting the official `curl … \| bash` installer | benign, not executed by build/test |
| powershell-download: `install.ps1:51,59` | Windows installer downloads the release zip + `.sha256` from the project's GitHub releases and verifies it | benign, not executed by build/test |
| secret-paths: `playback.rs:1027`, `local/dispatch.rs:28` | code comments containing the word "local state" | false positive |
| `std::process::Command` in `src/runtime/cli.rs:267` | self-update re-exec of the installed binary (CLI subcommand only) | benign, not reached by tests |
| `ProcessCommand::new("git")` in `src/cli/plugin.rs:590,602` | `spotatui plugin add/update` clones plugin repos with git | benign, not reached by tests touched here |
| `src/gates.rs` (runs in `cargo test`) | only reads `src/**/*.rs` and `tools/gates.count` from the repo root and counts patterns | benign |
| Git submodule `spotatui.wiki` | not initialised (shallow clone), docs only | benign |

**Verdict: no malicious code found. Safe to build and run the test suite.**
