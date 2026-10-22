## What does this pull request do?

- Resolves: #980
- Description: in copy mode, `^` now moves to the first nonblank character of the row and `$` (and the `copy_mode_line_end` action, `End` by default) to the last nonblank one, instead of column zero and the pane's last column. A new `copy_mode_first_nonblank` action does what `^` does, so it can be bound in `[keybindings.copy_mode]`.

---

## Motivation / Context

As #980 describes, `$`/`L`-bound line end landed on the blank padding at the pane edge, and `^` behaved like `0` (the handler even had a "could be enhanced to skip leading whitespace" note). tmux's `back-to-indentation` and `end-of-line` stop on the text, and so does vim. Column zero stays reachable through `0` and `copy_mode_line_start` (`Home`), for selecting indentation, as the issue asks.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

---

## What has been changed

- `internal/input/copymode_helpers.go`: `getCellAtCol` (what `getCellAtCursor` now calls), plus `firstNonBlankCol` / `lastTextCol`, which scan the cursor's row (screen or scrollback). A wide character answers with its first cell; tabs and spaces count as blank; a blank row gives column 0.
- `internal/input/copymode_handlers.go`: `^` and `$` in normal and visual mode, and the `copy_mode_line_end` / new `copy_mode_first_nonblank` actions, use them. `0` and `copy_mode_line_start` are unchanged.
- `internal/config/copy_mode_actions.go`, `registry.go`, `internal/app/help.go`: the new action, its description and its help row. Like `hold_window_mode`, it ships without a default key (`^` already does it), so it is absent from the defaults rather than present and empty; `TestEveryDescribedActionIsHandled` counts it through its constant.
- Tests: new `internal/input/copymode_line_motion_test.go` (screen rows, a selection, a blank row, wide characters, a scrollback row, and the three bound actions). `TestCopyModeBorderlessMotionReachesLastRow` asserted that `$` reaches the last column on a row holding just `$`; it now proves the last column is reachable with `l`, since `$` stops on the text by design.
- `docs/KEYBINDINGS.md`: the "Line start and line end" section describes the new targets and the new action.

---

## How to verify this change

1. `go build ./cmd/tuios`
2. `go test ./internal/input/ ./internal/config/ ./internal/app/ ./cmd/tuios/ -count=1` — all pass. The new tests fail on `main` (`^` → 0, `$` → 77) and pass with the change.
3. Manually: `printf '    alpha beta\n'`, `Ctrl+B [`, move onto the line: `^` lands on `a`, `$` and `End` on the final `a`, `0` and `Home` on column 0.

I did not run the e2e suite (`e2e/tui`) or the ghostty-backend tests; `e2e/tui/copy_mode_home_end_test.go` compares `End` with `$` on a line with no trailing blanks, which this keeps equal.

---

## Notes on compatibility / installation method

- Platform(s) tested: Linux x86_64 (unit tests only)
- Installation method tested: built from source
- Version/commit used: `9c8f0df`
- Behaviour change: anyone relying on `$`/`End` to select up to the pane edge (trailing blanks) now stops on the last character; `l` still walks to the edge.
