# AUDIT — lacs-project/sysknife @ 603ca81

`python3 tools/audit_repo.py` (505 text files). Verdict: **no malicious code found; safe to build/test.**

| Hit | Reviewed | Verdict |
|---|---|---|
| crates/sysknife-proto/build.rs | read in full | benign: prost_build with vendored protoc compiling the repo's own .proto |
| apps/sysknife-shell/src-tauri/build.rs | read | benign: `tauri_build::build()` only (GUI crate, not built here) |
| .pre-commit-config.yaml / .githooks/* | not installed (we never run `--install-hooks`) | n/a, not executed |
| packaging/sysknife-action-steps:271 `os.execve(..., os.environ)` | read context | benign: privileged helper exec of flatpak/podman/toolbox after dropping to user; not run by tests here |
| pipe-to-shell (fnm/ollama/rustup install hints in setup/e2e scripts) | read | benign: documented upstream installers in e2e provisioning/messages; not executed |
| secret-paths (.codexignore comment, atomic-vm.sh comment) | read | benign: comments only |
| npm hooks / committed binaries | none | — |

Only `cargo test -p <crate>` / clippy / fmt on the touched crates were run.
