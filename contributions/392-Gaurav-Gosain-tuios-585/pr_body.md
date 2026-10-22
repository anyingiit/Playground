## What does this pull request do?

- Resolves: #585
- Description: the review overlay's hunk and file motions (`]` `[` `}` `{`) become bindings in a new `[keybindings.review]` section, with the same keys as defaults, so a layout where those keys need Option (AZERTY on macOS, see #575) can move them.

---

## Motivation / Context

As #575 (point 2) and #585 describe, the four keys were hardcoded in `review_input.go`. On a French AZERTY Mac they need Option, which clashes with tuios when Option is Esc+. #585 asks for them to be bindable like the other keybindings and to show in `tuios keybinds` / `tuios keybinds explain`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

---

## What has been changed

- `internal/config/review_actions.go` (new): `review_next_hunk`, `review_prev_hunk`, `review_next_file`, `review_prev_file` and their defaults (`]`, `[`, `}`, `{`).
- `internal/config`: the `Review` section on `KeybindingsConfig` (`toml:"review"`), wired the way `transfers` and `copy_mode` are: defaults, nil-map init, `fillMapDefaults` for older configs, the section list, validation, `SectionReview` / `ScopeReview` (a modal "Review" scope, so `tuios keybinds` lists it), and `GetReviewAction` / `GetReviewKeys` on the registry.
- `internal/input/review_input.go`: the overlay looks the key up in the review section first (through `lookupAction`, so the layout-aware base code applies), runs the motion and notes the action; the four hardcoded cases are gone. The other overlay keys stay its own.
- `internal/app/render_review.go`: the footer hints name the bound key, and drop a hint whose action is bound to nothing.
- `internal/app/help.go`: the help overlay's review rows read the bound keys.
- Tests: the review section joins the reachability table (`reachReviewOS`), so every default key is pressed through the real entry point in both modes; `TestReviewMotionsFollowTheirBindings` rebinds the next-hunk/next-file actions and checks the new keys move and the old ones no longer do; `TestReviewMotionKeysAreTextInANote` checks `]` typed into a note stays text. The reachability rows and the rebinding test fail without the input change.
- `docs/KEYBINDINGS.md`: the review overlay table names the actions, plus a short `[keybindings.review]` example for AZERTY.

---

## How to verify this change

1. `go build ./cmd/tuios`
2. `go test ./internal/input/ ./internal/config/ ./internal/app/ ./cmd/tuios/ -count=1` — all pass.
3. Manually: add `[keybindings.review]` with `review_next_hunk = ["n"]`, open a review with `ctrl+b v`: `n` moves to the next hunk, `]` does nothing, and the footer shows `n next hunk`.

I did not run the e2e suite (`e2e/tui`).

---

## Notes on compatibility / installation method

- Platform(s) tested: Linux x86_64 (unit tests only)
- Installation method tested: built from source
- Version/commit used: `9c8f0df`
- Configs without the section get the old keys, as before. A key bound in `review` wins over the overlay's own key of the same name, which the docs point out. Unlike `copy_mode`, there is no doctor warning for such a clash yet; happy to add one (like `CopyModeProblems`) if you want it.
- `tuios keybinds list` prints a Review table and `tuios keybinds explain ']'` names `review_next_hunk` (checked with a built binary).
