## Description

Global options were parsed with `GlobalArgs::command()`, which has no subcommands, so with `ignore_errors(true)` parsing stopped at the subcommand name and `--color`/`-C` given after it (e.g. `git sl --color always`, `git branchless smartlog --color always`) were silently ignored.

When the parsed command already defines the global options (the main `git-branchless` executable, whose `Opts` flattens `GlobalArgs` with `global = true`), they are now read from matches of the full command, so clap propagates the values from the subcommand. Standalone `git-branchless-<subcommand>` binaries keep the previous behavior. Added a unit test in `git-branchless-invoke` and a CHANGELOG entry.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1308

## Checklist

- [x] Tests pass locally: `cargo test -p git-branchless-invoke` (new `test_global_args_position` fails without the fix: `smartlog --color always` parsed as `color: None`). Manually checked with a built binary that `git-branchless smartlog --color always | cat`, `--color=always`, and a `git sl --color always` alias emit colors, and `--color never` does not. `cargo fmt --all -- --check` and `cargo clippy -p git-branchless-invoke --no-deps --all-targets -- --deny warnings` are clean.
- [x] `CHANGELOG.md` is updated (if applicable) — entry under Unreleased → Fixed
- [ ] Documentation is updated (if applicable) — n/a
