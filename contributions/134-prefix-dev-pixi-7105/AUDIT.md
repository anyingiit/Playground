# Malicious-code audit — prefix-dev/pixi @ 6f71156de33ac6420522a77f21437ff0a331cb09

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/pixi` (1783 text files scanned), every hit reviewed manually before building/testing.

| Hit | Reviewed | Verdict |
|---|---|---|
| `crates/pixi_cli/src/build.rs` flagged as "cargo build script" | It is the `pixi build` CLI subcommand module (clap `Args` struct), not a Cargo build script (it is under `src/`, not referenced by `build =`). No `build.rs` build scripts exist in the workspace. | benign |
| `tests/**/conftest.py` (5 files) | Python integration-test fixtures (copy fixture repos, run `git` in temp dirs). Only a few selected `pixi info` / inline-environment integration tests were run (after this review), which do not use these git fixtures. | benign |
| `tests/data/**/setup.py`, `docs/source_files/**/setup.py` (5) | Minimal setuptools fixture packages used as test data. Not executed. | benign |
| `tests/data/git-fixtures/lfs-sample/001_v0.1.0/data.bin` | 1326-byte ASCII text fixture (LFS sample data). | benign |
| env-dump in `tests/integration_python/common.py`, `test_richer_platform_bugs.py`, `test_trampoline.py` | Copy `os.environ` to pass to child `pixi` processes in tests; nothing is sent anywhere. | benign |
| powershell-download in `install/install.ps1:194` | Official Windows installer downloading the pixi release binary from GitHub releases. Not executed. | benign |
| process-spawn `test_specified_build_source/conftest.py:29` | `subprocess.run(["git", ...])` in a temp fixture repo. | benign |

Additional manual checks: no `build.rs` / proc-macro crates inside the workspace that run custom code at build time beyond normal crates.io dependencies (from `Cargo.lock`); `lefthook.yaml` only runs formatters/linters (not installed here).

**Verdict: no malicious code found.** Executed only after this audit: `cargo build/test/clippy/fmt` on the Rust crates, a `uv`-based run of `schema/model.py` + schema pytest, and a handful of selected Python integration tests (`pytest --pixi-build=debug`) against the locally built `pixi` binary.
