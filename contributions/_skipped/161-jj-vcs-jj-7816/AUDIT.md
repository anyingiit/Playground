# Malicious-code audit — jj-vcs/jj @ 0cb02a8 (main, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/s2-1250/jj` (564 text files), then manual review. Written before any build/test.

| Hit | Reviewed | Verdict |
|---|---|---|
| `cli/build.rs` (auto-run on build/test) | Read in full (≈95 lines): runs `jj --ignore-working-copy log -r=@- -T commit_id` or `git rev-parse HEAD` only to embed a version hash; checks for a `docs` symlink to set `JJ_DOCS_DIR`. No network, no file writes outside cargo env vars. | benign |
| `Command::new("jj")` / `Command::new("git")` in build.rs | same as above, read-only version lookup | benign |
| "secret-paths" hits in `operation/revert.rs`, `operation/restore.rs`, `core/src/op_store.rs` | doc comments mentioning "local state" | false positive |
| npm lifecycle hooks / committed binaries | none | — |
| `lib/gen-protos` | separate binary to regenerate protobuf `.rs`; not run by build/test | benign |
| Test harness (`cli/tests/runner.rs`, `lib/testutils`) | runs the built `jj` binary in temp dirs with isolated config/env | benign |

Verdict: **no malicious code found**; safe to build and run targeted tests with `CARGO_TARGET_DIR` under /home/user/work/s2-1250.
