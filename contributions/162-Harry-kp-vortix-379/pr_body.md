## What does this PR do?

`vortix list` shows when each profile was last used via `format_elapsed` in
`crates/vortix/src/cli/profiles.rs`. The hour and day branches always used the plural, so a profile
used an hour or a day ago showed "1 hours ago" / "1 days ago". A small helper now picks the singular
when the count is 1 and keeps the plural otherwise ("2 hours ago", "2 days ago"). The "min" branch is
unchanged since it already reads fine for 1 and 2+.

`test_format_elapsed` gains the boundaries listed in the issue: 3600 and 7199 s ("1 hour ago"),
86400 and 172799 s ("1 day ago"). Without the fix the test fails with
`left: "1 hours ago"`, `right: "1 hour ago"`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related Issue

Fixes #379

## Type of Change

- [x] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 📖 Documentation
- [ ] 🔧 Refactor
- [ ] 🧪 Tests

## Checklist

- [x] `scripts/ci-local.sh` passes (see `docs/ci-parity.md`) — run on Linux, the parts touching this change: `cargo fmt --all -- --check` (clean), `cargo clippy -p vortix --all-targets -- -D warnings` (clean), `cargo test -p vortix` (all pass: 972 lib + 5 bin + integration/suite tests), `cargo test -p vortix format_elapsed` fails on `main` and passes with the change. Release build / size smoke and the xtask checks were not run (no docs or build changes).
- [x] I updated documentation if needed — n/a (no doc mentions this output; `CHANGELOG.md` is written at release time)
