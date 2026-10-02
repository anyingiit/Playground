- [x] I have run all relevant linters for this PR.
- [x] I have read and will follow the contributing guidelines.

#

- [x] AI was used in this PR to generate code, documentation, or other changes, and I have explained _how_ it was used below. I understand that if I do not adhere to disclosing AI usage, my PR can be closed, even without explanation.
- [ ] I have not used AI for _any_ portion of this PR.

## Description

`zb` already gets `arg_required_else_help` from clap's derive, since the subcommand is required. A bare `zb` shows the help in a clean environment. It breaks once `ZEROBREW_ROOT` or `ZEROBREW_AUTO_INIT` is set, because clap treats options filled from the environment as given. `zb init` (and `install.sh`) export `ZEROBREW_ROOT`, so most installed users see the error from the issue instead of the help:

```
$ ZEROBREW_ROOT=/tmp/x zb
error: 'zb' requires a subcommand but one was not provided
```

The fix adds `Cli::try_parse_args`. When there are no arguments at all, it clears the `env` sources on the command before parsing, so clap's own help-on-missing-subcommand path runs. Output, stderr and exit code (2) are the same as a bare `zb` without those variables. `zb.rs` now calls it instead of `Cli::parse()`. Any invocation with arguments parses as before, with env values applied.

One trade-off: the help printed for a bare `zb` leaves out the `[env: ZEROBREW_ROOT=]` and `[env: ZEROBREW_AUTO_INIT=]` hints, since those come from the stripped `env` settings. `zb --help` still shows them.

Tests in `zb_cli/src/cli.rs`:
- `shows_help_without_arguments`: bare `zb` returns `DisplayHelpOnMissingArgumentOrSubcommand`.
- `shows_help_without_arguments_when_env_options_are_set`: the regression test. It sets `ZEROBREW_AUTO_INIT=true`. Without the fix it fails with `MissingSubcommand`.
- `parses_subcommand_through_try_parse_args`: normal parsing through the new entry point still works.

Also added a `CHANGELOG.md` entry under Unreleased / Fixed.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. That covers the root-cause analysis, the code, the tests and this description. I reviewed it and checked the binary by hand. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #357

## Checklist

- [x] Tests pass locally: `cargo fmt --all -- --check` passes. `cargo clippy --workspace --all-targets -- -D warnings` passes. `cargo test --workspace` passes everything except `init::tests::is_writable_returns_false_for_readonly_dir` and `init::tests::needs_init_when_not_writable`. Those two fail the same way on `main` in my environment, because it runs as root and root can write to read-only directories. Manual check: `zb`, `ZEROBREW_ROOT=/tmp/x zb` and `ZEROBREW_AUTO_INIT=true zb` all print the help and exit 2. `zb -v` still reports the missing subcommand.
- [x] `CHANGELOG.md` is updated: added an entry under Unreleased / Fixed.
- [ ] Documentation is updated (if applicable): n/a
