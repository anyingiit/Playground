## Description

`Linkifier._removeIntersectingLinks` kept the occupied cells as a set of x values only. When a link started or ended on a row other than the hovered row `y`, its range was widened to `0..cols` on that row. On a wrapped line, links on different rows could therefore collide on x alone, and the lower priority one was dropped. For example, with link A at `(5,1)..(10,2)` and link B at `(20,2)..(30,2)`, hovering row 1 made A occupy x `5..cols`, so B was removed although the two links share no cell.

This PR keys the occupied cells by their absolute offset `y * cols + x` over the whole link range, which is what the issue suggests. Links are still only removed when they really share a cell, with the end position inclusive as before. Since the hovered row is no longer needed, the `y` parameter is dropped.

A regression test in `Linkifier.test.ts` registers two link providers and goes through `_askForLink`: one link wraps over two rows and the other provider returns two links on its second row; the one that shares x with the first row only is kept, and the one that really overlaps is still removed.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Fixes #4296

## Checklist

- [x] Tests pass locally
  - `npm run build && npm run esbuild && npm run test-unit -- out-esbuild/browser/Linkifier.test.js`: 5 passing. The new test fails without the fix (`4 passing, 1 failing`: the link on the second row is removed).
  - `npm run test-unit` (all unit tests): 2408 passing
  - `npm run lint-changes`: clean
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (the repo has no changelog)
- [ ] Documentation is updated (if applicable) — n/a (internal behavior only)
