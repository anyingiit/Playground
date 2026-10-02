## Purpose

Vim mode in the TUI supports `dw` and `dd`, but not the matching change commands `cw` and `cc`. This adds them, as described in #425.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Fixes

Fixes #425

## Approach

- `packages/tui/src/vim-mode.ts`: `c` is now a pending key, like `d` and `f`.
  - `cw` calls `editor.deleteWordForward()` (the same edit as `dw`) and enters insert mode.
  - `cc` calls a new `editor.clearCurrentLine()` and enters insert mode.
  - `c` followed by any other character clears the pending key, changes nothing, and stays in normal mode. `Escape` already clears a pending key.
- `packages/tui/src/editor.ts`: new `LineEditor.clearCurrentLine()`. It kills the text between the start and end of the current line and leaves the newline in place, so other lines are kept. It goes through the existing `kill()` path, so undo and the kill ring work as they do for `dd`. This differs from `deleteCurrentLine()`, which removes the line itself.
- SPDX copyright lines added to the three touched files, per CONTRIBUTING.

Notes for review:
- As the issue asks, `cw` uses `deleteWordForward()`, so it also removes the whitespace after the word (same as `dw`). Real Vim treats `cw` on a word like `ce` and keeps that space. I followed the issue text. I can switch to an end-of-word delete if you prefer.
- No compatibility or security impact. Only the opt-in `/vim` normal mode changes.
- This touches the same `handle()` method as #463 (`D` / `C`), but a different part of it. A rebase of either PR should be trivial.

## How was this tested?

Node v22.22.0, `pnpm install --frozen-lockfile`.

- New test `Vim cw and cc change text and enter insert mode` in `packages/tui/test/productivity.test.ts`. It covers `cw`, `cc` on the middle of three lines (other lines kept, insert mode, typed text lands on the cleared line), and `c` + another key cancelling.
- Red before the fix: `node --test --test-name-pattern=Vim test/productivity.test.ts` in `packages/tui` fails (`expected: 'two'`, `actual: 'one two'`). Green after the fix: 2/2 pass.
- `node --test test/*.test.ts` in `packages/tui`: 228 pass, 0 fail.
- `pnpm format:check`, `pnpm lint`, `pnpm typecheck`, `pnpm check:boundaries`, `pnpm check:generated`: all pass.
- `reuse lint` (6.2.0): compliant, 632/632 files.
- Full root test run (`node --test --test-concurrency=1 --test-timeout=30000 packages/*/test/*.test.ts packages/extensions/*/test/*.test.ts scripts/*.test.ts`, after `tsc -b` of all packages): 1073 tests: 1050 pass, 0 fail, 21 skipped, 2 cancelled by the 30 s file timeout on a loaded shared 4-core machine. The two were `packages/cli/test/unsafe-cli.test.ts` (passes 14/14 when run alone, with and without this change) and `scripts/build-release-package.test.ts` (runs the full `pnpm build` including the `@axl/web` build; not re-run here). Neither touches the TUI.
- Not run: the `@axl/web` production build (`pnpm build` runs it before `pnpm test`). This change does not touch the web package.

## Learning

N/A

## Checklist

- [ ] I reviewed the complete diff.
- [x] I added or updated the smallest relevant test for behavior changes.
- [x] I ran the relevant formatting, lint, type-check, test, boundary, and license checks.
- [x] Every new file has SPDX metadata, directly or through `REUSE.toml`. (No new files. Existing headers updated.)
- [x] Every commit has a matching DCO `Signed-off-by` trailer.
- [ ] UI changes include screenshots attached to the pull request, not committed to the repository. (Keybinding-only change with no visual change. Screenshot to be added if wanted.)

## AI assistance

- [x] Generative AI materially assisted this change. Tool and model/version: Claude Code (Claude Opus 5.5)
- [ ] I manually reviewed, understood, and tested the generated work.
