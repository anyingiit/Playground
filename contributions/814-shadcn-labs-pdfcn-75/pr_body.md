## Description

### Summary

Closes #75

Adds a `Timeline` PDF component for **both** the `takumi` and `forme` bases (same pattern as `key-value`):

- `registry/bases/{takumi,forme}/components/timeline/timeline.tsx`: typed `TimelineProps` / `TimelineItem` (`items: { date; title; body? }[]`, `accentColor?` (theme token or CSS color, default `primary`), `dateWidth?` (default `72`), `style?`). It uses `usePdfcnTheme`, `useSafeMemo`, `resolveColor` and the base `pdf-primitives`.
- Layout: a fixed-width muted date column, then a rail with the accent spine and a dot, then a semibold title and an optional muted body. The dot and the date are vertically centred on the first line of the title.
- Page splitting: each item is its own `wrap={false}` row, with its own spine segment above the dot (left blank on the first item) and below the dot (not drawn on the last item). The spine stretches with the row, so the dots stay aligned with items of any height. A page break can only fall between rows, so a marker is never left behind without its item, and the spine continues on the next page.
- I did not add the `renderingBase` prop from the issue sketch. Like every other component, the base is chosen by the registry entry (`@pdfcn/takumi/timeline` / `@pdfcn/forme/timeline`).
- Docs: `content/docs/components/{takumi,forme}/timeline.mdx` (copied from `key-value.mdx`, with a live `ComponentPreview`), `meta.json` page entries, examples in `examples/{takumi,forme}/timeline.tsx`, and `examples/__index__.ts` entries. All new entries are in alphabetical order.
- `registry.json` gets `takumi/timeline` and `forme/timeline`. `public/r/**` was regenerated with `pnpm registry:build` and not edited by hand.

Existing blocks (event-agenda, meeting-minutes) are untouched.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

### Validation

```bash
pnpm install --frozen-lockfile
pnpm registry:build   # Validated isolated install closure for 103 items (was 101); public/r/{takumi,forme}/timeline.json generated
pnpm fix
pnpm check            # 0 warnings, 0 errors; all files formatted
pnpm typecheck        # tsc --noEmit: OK
```

I also rendered the examples locally to PDF with `takumi-pdf` `render()` and `@formepdf/core` `renderPdf(serialize(...))`, the same calls the `/api/pdf/*` routes make. I rendered the docs demo plus a 24-item timeline with rows of mixed heights. On both engines the dots and spine line up, and the 24-item timeline breaks between rows onto page 2 with no orphaned dot. I did not run the full `next build`; CI runs it.

## Related issue

Closes #75

## Checklist

- [ ] I linked an issue with prior discussion confirming this change is wanted. (#75 is a `good first issue` / `help wanted` request with the spec; I commented on it before opening this PR.)
- [x] I ran the relevant checks from CONTRIBUTING.md (`pnpm check`, `pnpm typecheck`, `pnpm registry:build`)
- [x] I added tests and documentation where relevant. The repo has no unit tests; I added docs pages with live previews and examples for both bases.
- [x] I ran `pnpm check` and `pnpm typecheck` successfully
- [ ] `CHANGELOG.md` is updated (if applicable): n/a, the repo has no changelog
- [x] Documentation is updated (if applicable): new takumi and forme docs pages
