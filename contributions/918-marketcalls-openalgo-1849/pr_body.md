## Description

`useAuthStore` (`frontend/src/stores/authStore.ts`) wrapped its whole state in Zustand `persist`, so the OpenAlgo API key was written to `localStorage['openalgo-auth']` on every session sync. Any script running on the origin can read it there, and it survives browser restarts.

This PR keeps the key in memory only:

- **`partialize`** persists just `user` and `isAuthenticated`. New writes never contain `apiKey`.
- **`version: 1` + `migrate`** drops `apiKey` from existing v0 snapshots. Zustand rewrites storage after a migration, so the legacy key is also removed from `localStorage` on the first load after upgrade.
- **`merge`** strips `apiKey` from whatever is in storage, so a stored key (legacy or hand-edited) can never overwrite the in-memory one during hydration.
- `logout()` still sets `apiKey: null`, which clears it from memory.

The key stays usable during an active session: `AuthSync` already fetches it from `/auth/session-status` on every page load before rendering the app, so it never relied on the persisted copy. (This follows up the `partialize` suggestion in the review of #1865.)

Tests: `frontend/src/stores/authStore.persist.test.ts` uses jsdom `localStorage` with obvious dummy values and covers new writes, legacy hydration and cleanup, merge precedence and logout.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1849

## Checklist

- [x] Tests pass locally
  - `npx vitest run src/stores/authStore.persist.test.ts`: 2 of 4 tests fail without the fix (the key ends up in `localStorage`, and a legacy key is restored on hydration). All 4 pass with it.
  - `npx vitest run`: 245 files, 3457 tests passed
  - `npm run lint` (biome): no errors. The 4 warnings and 2 infos it reports are already on `main`; none are in the changed files.
  - `npx biome check ./src/stores`: clean
  - `npx tsc -p tsconfig.app.json --noEmit`: clean
  - `frontend/dist/` was not built or committed.
- [ ] `CHANGELOG.md` is updated (if applicable): n/a
- [ ] Documentation is updated (if applicable): n/a (internal store behaviour)
