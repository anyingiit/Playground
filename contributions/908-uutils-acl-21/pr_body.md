## Description

`getfacl` accepted `-p/--absolute-names` but ignored it, and absolute paths were always printed as-is in the `# file:` header.

This matches GNU getfacl: by default, leading `/` characters (and a leading `./`) are stripped from the name in the `# file:` header, and `getfacl: Removing leading '/' from absolute path names` is printed to stderr once per run. If nothing is left after stripping, `.` is used. With `-p`/`--absolute-names`, the name is printed as given.

Tests: a unit test for the stripping helper, plus integration tests for absolute paths (one warning for two files), `-p`/`--absolute-names`, and `./file`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #21

## Checklist

- [x] Tests pass locally (`cargo test`: 11 passed; `cargo test -p uu_getfacl`: 1 passed; `cargo fmt --all -- --check` and `cargo clippy --all-targets -- -D warnings` are clean). Without the fix, the new absolute-path and `./` tests fail.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, the `-p` help text already describes the behaviour
