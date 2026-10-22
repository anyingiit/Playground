# AUDIT — pydantic/monty @ 9ccbaff

`python3 tools/audit_repo.py` (1401 text files). Built/ran only `cargo build/test -p monty-runtime` and `cargo clippy -p monty-runtime`.

| Hit | Reviewed | Verdict |
|---|---|---|
| `.pre-commit-config.yaml` | not run | n/a |
| `crates/monty-typeshed/build.rs` | zips vendored `vendor/typeshed` into OUT_DIR; walkdir + zip only, no network/exec | benign |
| `crates/monty-js/build.rs` (`Command::new("npm")`) | JS crate, not in the monty-runtime dependency graph; never built | not run |
| `crates/monty-python/build.rs`, `monty-bench/build.rs`, `monty-datatest/build.rs`, `monty-python/tests/conftest.py`, `monty-js/vitest.config.ts` | not part of `-p monty-runtime` build/test | not run |
| `.devcontainer/setup.sh` curl \| sh (astral uv installer) | devcontainer only, not run | benign |
| long hex strings in `hashlib_module.rs` | sha2 state snapshots in tests | benign |
| `secret-paths` hits (`prepare.rs` "nonlocal") | false positive | benign |
| `dump_v13.bin` fixture | serialized snapshot test fixture, not executed | benign |

Verdict: no malicious code found.
