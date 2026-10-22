## Problem

`tools/nxs-pack` had no tests; its header said `TEST_COVERAGE: No tests` (#47).

## Scope

- Touched: `tools/nxs-pack/src/tests.rs` (new), `tools/nxs-pack/src/main.rs`, `tools/nxs-pack/Cargo.toml`, `Cargo.lock` (one line: `tempfile` under `nxs-pack`).
- Out of scope: the archive format and every packing path (`build_system_index`, `write_archive`, signing) are unchanged.

## ADR link(s)

- n/a (tests only). The tool is RFC-0012 Phase 1.

## Affected crates/modules

`nxs-pack` only.

- 17 unit tests in a `#[cfg(test)] mod tests;` file, covering the helpers listed in the issue:
  - `parse_args`: every flag in any order, each missing flag, a flag without a value, an unknown argument.
  - `parse_meta` / `req_str` / `opt_u64`: the version is trimmed and a missing timestamp defaults to 0. Errors for a missing or non-string `system_version`, a blank one, a negative or non-integer timestamp, invalid TOML, and a missing file.
  - `parse_manifest`: name and semver are read and trimmed. Errors for a blank name or semver, and for bytes that are not a Cap'n Proto message.
  - `read_file_with_limit`: a file at the limit is read, one byte over is refused, and a missing file is an error.
  - `sha256`: the known digests of `""` and `"abc"` (the FIPS 180-2 example).
- Rejection cases use the `test_reject_*` naming. Temp files go through `tempfile`, as in `nxb-pack`.
- The tests live in `src/tests.rs` rather than inline so `main.rs` stays well under the structure-gate's 600-line limit. The same `mod tests;` layout is used in `tools/nx/src/chain`.
- `parse_args` now delegates to `parse_args_from(impl Iterator<Item = String>)` so a test can pass an argument list. The binary still reads `env::args().skip(1)`, so there is no behaviour change.
- The header's `TEST_COVERAGE` line now points at the tests.

## Public API changes

None (binary crate; CLI unchanged).

## Invariants preserved

- [x] Host path byte-compatible (no change to what `nxs-pack` writes)
- [x] UART markers contract intact (not touched)
- [x] OS-lite code behind feature flag (not touched; host tool)

## Test plan

- `cargo test -p nxs-pack` → 17 passed (was 0).
- The tests catch regressions. I mutated the helpers one at a time and each mutation failed at least one test:
  - `>` → `>=` in the size bound.
  - Dropping the name `trim()`.
  - `n < 0` → `n < -1`.
  - Renaming the `--meta` flag.
- `cargo +nightly-2025-01-15 clippy -p nxs-pack --all-targets -- -D warnings`: clean.
- `cargo +nightly-2025-01-15 fmt --all -- --config-path config/rustfmt.toml --check`: clean.
- `scripts/check-structure.sh`: PASS.
- Not run: the full `just check` (I don't have `just`/`cargo-deny` set up here; `tempfile` is already in `Cargo.lock` and only a dev-dependency, so it is not in the OS graph), `just diag-os` and the QEMU lanes, which this host-only test change doesn't affect. No CHANGELOG entry, since the Unreleased section records closed tasks and this only adds tests. Happy to add one if you'd like.

## Rollback plan

Revert the single commit; it only adds tests plus the `parse_args_from` split.

Closes #47

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂
