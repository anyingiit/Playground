# MakazhanAlpamys/Soup #1221

| 项 | 值 |
|---|---|
| Issue | https://github.com/MakazhanAlpamys/Soup/issues/1221 |
| Tier | 高活跃高Star |
| Labels | bug, help wanted |
| Status | 🚧 in progress — issue chosen, cloning/auditing |
| Duplicate-PR check | `1221 repo:MakazhanAlpamys/Soup` → 0 PRs; keyword `forge judge empty answer` open → 0; issue has 0 comments, unassigned (checked 2026-09-24) |

## Notes
- `make_judge_provider_fn` returns `{"text": ""}` on failure unless `raise_on_error=True`; `soup data forge` builds judge without it → empty-answer rows, exit 0.
- Fix path per issue: raise_on_error=True, count failures, prune empty replies regardless of threshold, report `N of M judge calls failed` + first error, exit non-zero when no usable row.
