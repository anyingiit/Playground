## Description

Adds `apps/server/tests/rulesById.test.ts`, a supertest suite for the by-id routes of `/api/v1/mute-policies/:id` and `/api/v1/enrichments/:id`, modeled on `tests/tags.test.ts`. No production code changes.

**What was changed:** one table-driven `describe.each` runs the same cases against both resources. Each test creates its row through the API in `beforeEach`, after clearing the table:

- `GET` of an existing row returns 200 with that row
- `GET`, `PUT` and `DELETE` with an unknown id return 404 with the resource's `... not found` error, and the existing row is left as it was
- `GET`, `PUT` and `DELETE` with a non-numeric id (`abc`) return 400 `Validation error` (zod)
- `GET`, `PUT` and `DELETE` without an `Authorization` header return 401, and nothing is changed
- `PUT` with `{}` returns 200 and the resource unchanged (`updatedAt` is ignored in the comparison)
- the normal `PUT` and `DELETE` paths (`DELETE` followed by a 404 on `GET`)

The mute-policy evaluator is out of scope, as the issue says.

**Why was it changed:** these error paths had no direct tests. To check that the new tests catch real regressions, I broke the handlers one at a time and confirmed that the matching test failed each time (all mutations were reverted afterwards):

| Mutation | Failing test(s) |
|---|---|
| mute-policy controller skips the `!mutePolicy` 404 check | `404 for an unknown id`, `DELETE removes the resource` |
| enrichment `deleteHandler` skips the `!existing` check | `404 for an unknown id` (enrichments) |
| mute-policy controller stops mapping zod errors to 400 | `400 for a non-numeric id` |
| mute-policy `updateHandler` writes `reason: null` when it is omitted | `PUT with an empty body returns the resource unchanged` |
| `/enrichments` router mounted before `authenticateJWT` | `401 without an Authorization header` |

**Screenshots:** n/a (tests only).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1041

## Checklist

- [x] Tests pass locally
  - `pnpm --filter @OpsiMate/server exec vitest run tests/rulesById.test.ts`: 14 passed
  - `pnpm --filter @OpsiMate/server test` (after building `@OpsiMate/shared`, as CI does): 46 files / 610 tests passed
  - `pnpm --filter @OpsiMate/server format` (Prettier check): clean; `pnpm --filter @OpsiMate/server lint`: clean
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (tests only)
- [ ] Documentation is updated (if applicable) — n/a (tests only)
