# thebanri/limoni #59 — Sixel encoder allocates per pixel when building its palette

Status: 🚧 in progress — audit done, implementing

| Item | Value |
| --- | --- |
| Issue | https://github.com/thebanri/limoni/issues/59 |
| Tier | 新锐 |
| Labels | good first issue, graphics, performance |
| Status | open, unassigned, no comments (opened 2026-09-24) |
| Duplicate-PR check | none (all 21 PRs closed; none mention sixel/palette/#59) |

Baseline: `go test ./graphics -run '^$' -bench EncodeSixel -benchmem` → 51211 allocs/op, 371 KB/op, ~2.0 ms/op.
