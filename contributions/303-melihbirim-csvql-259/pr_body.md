## Description

Follow-ups from the review of #250 / #251, as listed in #259:

- **zsh exclusion groups match the binary.** `--json`/`--jsonl` and `--table`/`--no-table` can be combined (the last one wins), so they no longer exclude each other. The only real conflicts are `--markdown` with `--json`, `--jsonl` and `--no-header` (the ones `main.zig` rejects), so those are the only exclusion groups left.
- **zsh `--root` completes a comma-separated list**, like the bash script, using zsh's own `_dir_list -s ,`. The action is written as `{_dir_list -s ,}` because in the plain word form `_arguments` didn't complete after the comma.
- **Drift test only counts spec lines.** `tests/completions_test.zig` now looks for each flag on completion spec lines only: the `compgen -W` word lists in bash, and the quoted `_arguments` specs plus the `compadd` line in zsh. For a zsh spec it only reads the option names: the leading exclusion group and the `[description]` are dropped. So a flag mentioned only in a comment, in another option's exclusion group (e.g. `(--markdown)--json`) or in a description no longer satisfies the test. There are two new unit tests for this.
- **README:** a note that macOS Terminal reads `~/.bash_profile`, plus `mkdir -p` and the `fpath=(...)` line before `compinit` for zsh.

**Not included: `--root=dir` in bash.** I left this one out on purpose. The binary only accepts `--root <dir>` today; it never parses `--root=<dir>`. `--root=<dir>` is passed through with the query arguments, so the root restriction is not applied. For example, `csvql "SELECT * FROM '/tmp/x.csv'" --root=/home` reads the file outside `/home` and exits 0. With `--root /home` it fails with `PathOutsideAllowedRoot`. Completing the `=` form would point people at a spelling that silently drops the sandbox, which matters most with `--mcp`. Two possible follow-ups: accept `--root=<dirs>` in `main.zig` (both parse loops), or reject unknown `--flags`. I'm happy to do either in a separate PR if you'd like.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Part of #259. Everything except the `--root=dir` item; see the note above.

## Checklist

- [x] Tests pass locally (`zig build test` with Zig 0.15.2: 35/35 steps, 1066/1066 tests passed; `zig fmt --check src tests build.zig` is clean)
- [x] Red → green, with the old drift test still passing in each case and the new one failing:
  - Moving `--strict` from the bash `compgen -W` list into a comment: the old test passed (1064/1064); the new one fails with `completions/csvql.bash is missing --strict`.
  - Deleting the zsh `--markdown` spec line, which is still listed in other options' exclusion groups: the new test fails with `completions/_csvql is missing --markdown`.
  - Deleting the zsh `--no-header` spec line: the new test fails with `completions/_csvql is missing --no-header`.
- [x] zsh 5.9, checked by capturing completions in a pty:
  - `csvql --json --` now offers `--jsonl --table --no-table` (and no longer `--markdown`).
  - `csvql --markdown --` hides `--json --jsonl --no-header`.
  - `csvql --root da,d` offers `da,da da,db` (before: nothing).
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [x] Documentation is updated (if applicable) — README completion install steps
