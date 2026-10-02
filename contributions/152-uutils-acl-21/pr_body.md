## Description

`getfacl` already accepted `-p` / `--absolute-names`, but the flag was ignored and the `# file:` header always echoed the path verbatim.

This implements the GNU getfacl behaviour:

- By default, leading `/` characters are stripped from the name shown in the `# file:` header, and a one-time warning is printed to stderr: `getfacl: Removing leading '/' from absolute path names`. A leading `./` is also dropped, and an empty result (e.g. `getfacl /`) is shown as `.`.
- With `-p` / `--absolute-names`, the name is printed exactly as given and no warning is emitted.

Only the displayed name changes; the file is still looked up with the original path. The logic lives in a small `display_name` helper, with a new `absolute_names` field on `Config`.

Tests added in `tests/by-util/test_getfacl.rs`: stripping plus warning, the warning printed only once for several files, `/` shown as `.`, `-p`/`--absolute-names` keeping the slash, and `./file` shown as `file`. Four of these failed before the change and all pass after it.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #21

## Checklist

- [x] Tests pass locally (`cargo test`: 13 passed, 0 failed; `cargo fmt --all -- --check`: clean; `cargo clippy -- -D warnings` and `cargo clippy --all-targets -- -D warnings`: no warnings)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, the `--help` text for `-p` already describes this behaviour
