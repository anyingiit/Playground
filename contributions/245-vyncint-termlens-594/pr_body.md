## What & why

The CLI promises exit codes 0, 1 and 2, but the three inputs in #594 ended in a panic and exit 101. This fixes all three plus the `--out ""` message the issue mentions:

- **Closed or full stderr** (`2>&1 | true`, `2>/dev/full`): diagnostics and the `inspect` trailer went through `eprintln!`, which panics on a failed write. They now go through a small checked helper. A lost diagnostic keeps its exit 2, and a trailer that cannot be written is exit 2, since the run's result never reached the caller.
- **Non-UTF-8 argument**: arguments are read with `args_os`. termlens's own options and operands must be UTF-8 and are refused with exit 2 (`"\xff" is not valid UTF-8; termlens's own arguments must be`), while the program `inspect` runs gets its arguments untouched, so `termlens inspect -- prog $'\xff'` works.
- **Huge `--timeout`**: the deadline is computed with `checked_add` before the program is spawned, so a timeout the clock cannot represent is refused by name instead of panicking after the spawn.
- **`render --out ""`** now says `--out needs a PATH argument`, as `--out=` already did (#451).

The `inspect` example gets the same fixes, including its `--help`/`--version` under `| true`.

Closes #594

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below; per CONTRIBUTING §6 the commit carries no AI attribution and I'm the author of record under the DCO. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all.

## Checklist

- [x] Linked an issue (#594)
- [x] Tests added/updated for the change: five new tests in `crates/termlens-cli/tests/cli.rs` (closed stderr, `/dev/full` on Linux, non-UTF-8 arguments on Unix, an unrepresentable `--timeout`, `render --out ""`). All five fail on `main` and pass with the change.
- [x] `cargo fmt --all` and `cargo clippy --workspace --all-targets --all-features` are clean; `cargo test --workspace` passes
- [x] **All commits are signed off** (`check-dco.sh main..HEAD`: OK)
- [x] **No AI attribution trailers** (`check-no-ai-attribution.sh main..HEAD`: OK)
- [x] `CHANGELOG.md` updated under `[Unreleased]` → `Fixed`
- [x] Snapshot changes (if any) were reviewed with `cargo insta review`, not blind-accepted (none in this PR)

Not done: I didn't run `cargo-semver-checks` (not installed here); the change is binary-only plus an example, with no library API change. I haven't run the stress workflow (`stress.yml`); four of the new tests spawn `inspect`, so they add PTY spawns, which CONTRIBUTING §3 says must pass it. I can trigger it on my fork, or a maintainer can. I also didn't run the Windows clippy target.

One behaviour to flag: termlens's own path arguments (`--cwd`, and the `diff`/`render` file operands) must now be UTF-8, so a non-UTF-8 path is refused with exit 2 rather than accepted. Before this it panicked. The issue asks for that for termlens's own options; if you'd rather accept non-UTF-8 paths, I can carry those as `OsString`. In `tools/preflight.sh` the attribution-gate selftest's "bot author identity" case fails on an untouched `main` in my environment too, so I don't think it relates to this change.
