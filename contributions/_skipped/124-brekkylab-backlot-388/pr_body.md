## What changed

`_flag` in `backlot/routers/hubspot.py`, which reads the `archived` query parameter of `GET /crm/v3/objects/{objectType}`, now treats only `true` (in any case) as true. `archived=1` and `archived=yes` serve the active records instead of the archived view; `true`, `TRUE`, `abc`, an empty value and an absent parameter answer as before. The docstring now records the measurement instead of the old "plausible spellings" rationale. A parametrized test in `tests/test_hubspot.py` pins all seven cases.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Closes #388

## Why this is what the real API does

The measurement is the one in #388 (split from #379, block 2), taken against api.hubapi.com on 2026-10-01 with `GET /crm/v3/objects/contacts?archived=<value>`: `true` and `TRUE` served the archived contact; `1`, `yes`, `abc`, an empty value and an absent parameter all served the five active contacts. I did not take a new live measurement myself. Mixed case such as `True` and surrounding whitespace were not part of that measurement; the change keeps the existing case-folding and `strip()` for those.

## Verification

- **Tests** — `pytest` on a `.[dev]` install (`uv sync --extra dev --locked`, Python 3.11): 3771 passed, 38 skipped. With only the router change reverted, `pytest tests/test_hubspot.py` fails `test_hubspot_archived_reads_only_true_as_true[1-False]` and `[yes-False]` (2 failed, 39 passed); with it, 41 passed.
- **Optional surfaces that ran rather than skipped** — none; the 38 skips are the extras-gated files (`official-sdk`, `llamaindex`, `mcp`, `mirage`, `fsspec`). The change is in the HTTP route, which the `.[dev]` endpoint tests cover.
- **Lint** — `ruff check . && ruff format --check .`: All checks passed! / 143 files already formatted

- [x] A test fails without this change
- [ ] A new endpoint serving corpus content is ACL-scoped, proved for both an admin and a scoped token — n/a, no new endpoint
- [x] Comments state what was measured, not the history of the fix
