# Audit — Enter-tainer/typstyle (shallow clone, default branch, 2026-10-01)

Tool: `python3 tools/audit_repo.py /home/user/work/typstyle` (169 text files).

| Hit | Reviewed | Verdict |
|---|---|---|
| crates/typstyle/build.rs | read fully | benign — `vergen` build metadata (timestamp/rustc/git describe) only |
| crates/typstyle-wasm/build.rs | read | benign — parses `../typstyle-core/src/config.rs` with `syn` to generate TS types; no network/exec (not built here) |
| npm lifecycle hooks | none | n/a |
| committed binaries | none | n/a |
| .github/workflows/build-docs.yml:38 `curl ... shiroa-installer.sh \| sh` | read | CI-only docs build from the official shiroa release; never run here |

Verdict: no malicious code. Only `typstyle-core` + `typstyle-tests` built/tested locally.
