# inokawa/remark-pdf#61 — Table cells in a row are not stretched to the row height

| | |
|---|---|
| Issue | https://github.com/inokawa/remark-pdf/issues/61 |
| Tier | 自由 |
| Labels | `good first issue` |
| Status | 🚧 in progress — audit |

## Notes
- Root cause in `src/layout.ts` (`case "table"`): `rowHeight` computed but each cell BlockBox keeps its own height; `border: true` cells draw their own border.
- Issue open since 2026-06-03, no assignee/comments/linked PR (WebFetch).
- Outside contributors merged historically (James Zetlen, Georgios Petasis, Alan007BR).
