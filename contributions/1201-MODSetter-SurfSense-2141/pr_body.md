## Description

**What.** `wait()` in `surfsense_local/frontend/src/features/workspaces/workspace-changes.ts` now:

- removes its `abort` listener when the retry timer fires (the same pattern `wait()` in `features/studio/use-studio.ts` already uses), and
- resolves at once when the signal is already aborted.

The "Known gaps" entry for this in `docs/architecture/overview.md` (added in #2140) is removed.

**Why.** The workspace signal lives as long as any list listens, and `wait()` runs once per retry. Before this change each wait added an `abort` listener and never removed it when the timer fired first. A stream that kept dropping (for example while the API is down) therefore collected about 360 listeners an hour. An aborted signal never fires `abort` again, so a stream torn down between attempts also sat out its full backoff (up to 10 s) before the loop exited.

**Tests.** I added two regression tests to `workspace-changes.test.ts`. They use fake timers and `addEventListener`/`removeEventListener` spies on the workspace's signal:

- *removes each retry's abort listener once its wait is over*: the API is down for 60 s (about 9 attempts). Every wait except the one still running has removed its listener.
- *stops at once when the stream is closed between attempts*: the last list leaves while a request is in flight. The loop adds no listener to the aborted signal and leaves no timer pending.

**How to test** (repo template). In `surfsense_local/frontend`, run `pnpm install --frozen-lockfile`, then `pnpm exec vitest run --environment jsdom src/features/workspaces/workspace-changes.test.ts`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #2141

## Checklist

- [x] Tests pass locally:
  - `pnpm exec vitest run --environment jsdom src/features/workspaces/workspace-changes.test.ts`: 5 passed. When only `workspace-changes.ts` is reverted, both new tests fail. `removeEventListener` was expected 8 times and was called 0 times. `addEventListener` was called once on the aborted signal.
  - `pnpm test`: 63 files and 384 tests passed.
  - `pnpm typecheck` and `pnpm lint` pass. `prettier --check` passes on the changed files.
  - `pnpm translations:extract` leaves `en.json` unchanged, `pnpm translations:verify` passes, and `node scripts/check_translations.mjs` reports 0 problems.
  - `python scripts/check_docs.py`: 111 doc files, 0 problems.
- [ ] `CHANGELOG.md` is updated (if applicable): n/a, the repo has no changelog
- [x] Documentation is updated (if applicable): the known-gap entry in `docs/architecture/overview.md` is removed
