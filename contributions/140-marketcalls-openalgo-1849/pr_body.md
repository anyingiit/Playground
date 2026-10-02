## Description

`useAuthStore` wrapped its whole state in Zustand `persist` with no `partialize`, so the OpenAlgo API key was written to `localStorage["openalgo-auth"]`. Any script on the origin can read that, and it survives browser restarts.

This change keeps the key in memory only:

- `partialize` persists just `user` and `isAuthenticated`, so new writes never contain `apiKey`.
- The persist `version` goes from 0 to 1 with a `migrate` that rewrites an existing entry without the key on first load, so keys stored by older builds are removed from localStorage.
- A `merge` that never takes `apiKey` from storage, whatever version wrote it.
- In-session behaviour is unchanged: `AuthSync` already fetches the key from `/auth/session-status` on every page load and renders children only after that check, and `logout()` still sets `apiKey` to `null`.

One behavioural note for reviewers: if `/auth/session-status` throws a network error on load, `AuthSync` leaves auth state as it is. Before this change the stale key from localStorage would then still be in memory; now `apiKey` stays `null` until the next successful sync. That seemed like the right trade-off for a credential, but say so if you would rather handle it differently.

New test `frontend/src/stores/authStore.persist.test.ts` (jsdom localStorage, dummy key value) covers: no key in new writes, key usable in memory, legacy version 0 entry with a key is hydrated without it and rewritten, and logout clears the key. The first and third tests fail without the fix.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all.

## Related issue

Closes #1849

## Checklist

- [x] Tests pass locally (`cd frontend && npm run test:run`: 245 files, 3457 tests passed; new test fails 2/4 without the fix, 4/4 with it)
- [x] Lint and types (`npm run lint`: no errors, same pre-existing warnings; `npx tsc -b`: clean)
- [ ] `CHANGELOG.md` is updated (if applicable) - n/a, `docs/CHANGELOG.md` is written at release time
- [ ] Documentation is updated (if applicable) - n/a, no user-facing docs describe this storage
