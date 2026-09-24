# LargeModGames/spotatui #554 — `ctrl--` / `alt--` key bindings fail to parse

| Item | Value |
|---|---|
| Issue | https://github.com/LargeModGames/spotatui/issues/554 |
| Tier | 自由 |
| Labels | bug, good first issue |
| Status | ✅ ready |
| Duplicate-PR check | 4 open PRs (#574 debug logging, #524 native-queue downloads, #391 Sonos, #358 audio device) — none touches key parsing; PR search `554` → only the unrelated #534. Issue: no assignee, opened by the maintainer 2026-09-23 (checked 2026-09-24, re-checked before finishing). ⚠️ The API reports **1 comment** that could not be read from here (the GitHub HTML/API is blocked for this environment and WebFetch shows none) — please glance at the issue before opening the PR in case someone claimed it. |
| Base | `main` @ 9c46bc0 (2026-09-24) |

## 为什么选这个

- spotatui: a Rust Spotify TUI (successor of spotify-tui), very active (commits daily, release v0.43.0 on 2026-09-23).
- Outside PRs are merged routinely: #569/#555 (Hi-1mYara), #560/#561 (yvoolab), #551 (TongTong0828), #550 (Oud-Idk), #536 (nohint404), #531 (shilicioo); all-contributors bot adds them.
- The issue is written by the maintainer with an exact suggested fix and "done when" criteria.

## 需要提交者注意

- **AI policy**: the repo ships `AGENTS.md` / `CLAUDE.md` / `.github/copilot-instructions.md` for coding agents — AI-assisted contributions are explicitly expected; no disclosure/ban rules found (`CONTRIBUTING.md`, `.github/`). No DCO / sign-off.
- PR template (`.github/PULL_REQUEST_TEMPLATE.md`) has sections **Summary / Testing / Additional notes** — the PR body below uses those headings (plus the disclosure paragraph and `Closes #554`).
- CI has a PR-only **Gates ratchet** job: `tools/gates.count` `test_attribute_total` was raised 2123 → 2125 for the two new tests. If `main` gains tests before this merges, rebase and set it to the value `cargo test` (in `src/gates.rs`) prints.
- `CHANGELOG.md`: entry added under `[Unreleased]` → new `### Fixed` section, in the repo's bold-headline style, linking the issue.
- Commit message is Conventional Commits (`fix(config): …`), matching the repo history.

## 问题理解

`parse_key` did `key.split('-')` and rejected anything with more than 2 sections. `ctrl--` → `["ctrl", "", ""]` → "Shortcut can only have 2 keys". Consequences: `config.yml` skipped such a binding with a warning; in Settings, pressing Alt+- stored `alt--` (via `key_to_config_string`), `settings_apply.rs` silently ignored the parse error (`if let Ok(...)`), and the row showed `alt--` while the binding didn't change.

## 合理性判断

Clear bug, maintainer-filed, fix spelled out in the issue (`splitn(2, '-')`, drop the `> 2` check, keep `modifier_char` as is, `ctrl-a-b` must stay an error, `-` alone must still be `Key::Char('-')`, existing malformed-binding cases must still fail).

## 改动

- `src/core/user_config.rs`: `parse_key` splits on the first dash only (`splitn(2, '-')`); the "only 2 keys" check is removed. `ctrl-a-b` → `["ctrl", "a-b"]` → rejected by `modifier_char` ("must combine the modifier with exactly one key"), naming the binding.
- Test `a_dash_after_a_modifier_parses_as_the_key` (`ctrl--` → `Ctrl('-')`, `alt--` → `Alt('-')`, `-` → `Char('-')`, `ctrl-a-b` error names the binding).
- `src/tui/handlers/settings.rs`: test `a_dash_keybinding_round_trips_through_the_config_string` (`parse_key_public(key_to_config_string(k)) == k` for `Alt('-')`, `Ctrl('-')`, `Char('-')`) — the optional test from the issue.
- `tools/gates.count`: `test_attribute_total` 2123 → 2125.
- `CHANGELOG.md`: Fixed entry.

## 验证

Toolchain rustc/cargo 1.98.1, `CARGO_TARGET_DIR` outside the repo.

- **Red** (tests + gates bump, without the `parse_key` change):
  `cargo test --locked --no-default-features --features telemetry,tui dash_` → `0 passed; 2 failed` (both new tests; `ctrl--` unwrap on `Err("Shortcut can only have 2 keys …")`).
- **Green**: same command → `2 passed; 0 failed`. The issue's check `cargo test --no-default-features --features telemetry,tui dash_after_a_modifier` → `1 passed; 1134 filtered out`.
- **Full slim gate** (CONTRIBUTING / AGENTS.md):
  - `cargo fmt --all -- --check` → clean
  - `cargo clippy --locked --no-default-features --features telemetry,tui -- -D warnings` → clean
  - `cargo test --locked --no-default-features --features telemetry,tui` → **1135 passed, 0 failed** (includes `src/gates.rs` ratchet pin test)
  - `bash tools/check_gates_ratchet.sh 9c46bc0` → `ok`
- Not run: the other CI legs (default / all-sources / mcp-only / ai-dj-only / headless / macOS) — they need librespot/audio system libs and a lot of disk. The change is in feature-independent `core/user_config.rs` code plus a test in the `tui` settings handler, so no leg-specific code is touched.

## 如何提交

```bash
git clone https://github.com/<you>/spotatui && cd spotatui
git checkout -b fix/dash-after-modifier-keybinding origin/main
git am /path/to/0001-fix-config-parse-ctrl-and-alt-keybindings.patch
git push -u origin fix/dash-after-modifier-keybinding   # then open PR against LargeModGames/spotatui:main
```

## PR title

`fix(config): parse ctrl-- and alt-- keybindings`

## PR body

```markdown
# Summary

`parse_key` split a binding on every `-`, so a dash after a modifier (`ctrl--`, `alt--`) became three sections and was rejected with "Shortcut can only have 2 keys". In `config.yml` the binding was skipped with a warning; in Settings, pressing Alt+- stored `alt--` while the old binding stayed active.

It now splits on the first dash only (`splitn(2, '-')`) and the "only 2 keys" check is gone, as suggested in the issue. `ctrl-a-b` still fails, now in `modifier_char`, whose message names the binding; `-` alone still parses as `Key::Char('-')`, and every case in `malformed_modifier_bindings_error_instead_of_panicking` still fails.

- New test `a_dash_after_a_modifier_parses_as_the_key` (`src/core/user_config.rs`).
- New round-trip test `a_dash_keybinding_round_trips_through_the_config_string` in the settings handler (`parse_key_public(key_to_config_string(&key)) == key` for `Alt('-')`, `Ctrl('-')`, `Char('-')`).
- `tools/gates.count`: `test_attribute_total` 2123 → 2125.
- `CHANGELOG.md`: entry under `[Unreleased]` → Fixed.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Closes #554

# Testing

- Without the fix, `cargo test --locked --no-default-features --features telemetry,tui dash_` → 2 failed (both new tests); with it → 2 passed
- `cargo test --no-default-features --features telemetry,tui dash_after_a_modifier` → 1 passed
- `cargo fmt --all -- --check` → clean
- `cargo clippy --locked --no-default-features --features telemetry,tui -- -D warnings` → clean
- `cargo test --locked --no-default-features --features telemetry,tui` → 1135 passed, 0 failed
- `tools/check_gates_ratchet.sh origin/main` → ok

# Additional notes

Only the slim leg was run locally; the change is in feature-independent config parsing, so the other CI legs should behave the same.
```
