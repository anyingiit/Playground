## What and why

On first use the emoji data is still loading when the picker opens, so typing "rocket" in the search box and pressing Enter right away did nothing: `results` was still `null`, so the Enter handler had nothing to pick.

This records an Enter pressed in that state and picks the first result once the data arrives. Typing again before the data loads drops the pending pick, so it never applies to a query the user has moved past. Once the data is loaded, Enter behaves exactly as before.

Fixes #38

Implementation notes (`packages/ui/src/components/emoji-picker.tsx`):

- The pending Enter is a ref, so it causes no extra render. An effect on `results` picks `results[0]` and clears the ref.
- `pick` is now wrapped in `useCallback([onSelect])` so the effect can depend on it under `react-hooks/exhaustive-deps`.
- Enter only becomes pending when the data hasn't loaded, the load hasn't failed and the query isn't blank. If nothing matches when the data arrives, nothing is picked, the same as pressing Enter on "No emoji found" today.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## How to test it

1. Open the emoji picker for the first time in a fresh tab (for example, a page icon), so the emoji data has not loaded yet.
2. Type `rocket` and press Enter immediately. 🚀 is selected as soon as the data arrives. (Throttling the network in DevTools makes the loading window easier to hit.)

Two tests were added to `packages/ui/src/components/components.test.tsx`:

- `picks the first result of an Enter pressed while the emoji are still loading`: types "rocket" and presses Enter while the spinner is showing, then expects `onSelect('🚀')` exactly once. It fails without the fix.
- `drops a pending Enter when the query changes before the emoji load`: Enter on "rocket", then the query changes to "pizza" before the data loads, so nothing is picked. This one passes without the fix too (Enter did nothing before), but it fails if the pending pick isn't cleared on typing.

## Checklist

- [x] The PR does one thing, and its title follows [Conventional Commits](https://www.conventionalcommits.org) (`feat(editor): …`).
- [x] `pnpm typecheck`, `pnpm lint` and `pnpm test` pass locally (`pnpm test`: 184 files, 1590 tests).
- [x] New behavior has tests; a bug fix has a test that failed before the fix.
- [x] UI works in light and dark themes, at phone width, and with the keyboard alone. No visual change; the fix is keyboard-only and is covered by the jsdom tests above.
- [x] User-facing strings go through `t()`. No new strings.
- [x] Docs are updated if behavior changed. Not needed; this makes the picker do what it already promises.
