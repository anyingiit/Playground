## What does this change?

`no_tier_rule_has_an_empty_description` predates `TierName::Developer` and only iterated Safe, Standard and Unrestricted, so the Developer tier's rules (including the nine `DEVELOPER_TOOLS` allows) were never checked for an empty description. This adds `TierName::Developer` to the iterated array, as the issue describes. No production code changes.

Closes #57

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Testing checklist

- [ ] `cargo test` passes (this crate targets Fedora specifically, `systemctl`/`dnf`/`journalctl` integration tests need a real Fedora host, see `CONTRIBUTING.md`'s development-environment section). I ran it in a Linux container that isn't Fedora: the lib suite gives 158 passed, 5 failed and 1 ignored, and the same 5 fail on unpatched `main`. They are the `run_as_*` and `dispatch_drops_privilege_*` privilege-drop tests, which can't spawn in this environment. `no_tier_rule_has_an_empty_description` passes.

- [x] `cargo clippy --all-targets -- -D warnings` is clean
- [x] `cargo fmt --check` is clean
- [ ] If this touches `src/policy/`: a test covers the specific behaviour changed, including at least one test attempting to smuggle a second command or flag-injection payload past a deny rule (see `CONTRIBUTING.md`'s testing expectations). N/A: this only widens an existing test in `src/policy/tiers.rs` and changes no rule, so there is no deny rule to smuggle past.
- [ ] If this adds or changes a tool in `src/tools/`: not applicable.

The test still passes with Developer included, because every Developer rule already has a real description. To check that it now covers that tier, I temporarily blanked the `DEVELOPER_TOOLS` allow description in `developer_rules()`. The updated test then failed (`rule for command 'bash' under Developer has an empty description`), and the original test still passed. The other `[Safe, Standard]` loops in this file are tier-specific regression tests, not "every tier" checks, so I left them alone.

## Security considerations

None: this is a test-only change and doesn't alter any rule or code path.
