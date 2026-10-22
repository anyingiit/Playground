## What & why

`WIGOLO_AUTH_STATE_PATH` reached `fetchWithBrowser` as `storageStatePath`, but none of the places that create a browser context used it, so `use_auth: true` fetches ran as a logged-out visitor.

Fixes #526

## Changes

- **Pooled path** (`acquireForType`): I didn't add `storageState` to the pooled `newContext`, because pooled contexts are reused. The first authenticated fetch would seed the session into a context that the next anonymous fetch picks up. Instead, a fetch with a storage state gets its own context on the shared browser, created with `{ acceptDownloads: true, storageState }`, and closed in the existing `dedicated` cleanup in the `finally`. The shared browser stays up, no extra browser is launched, and the stealth slot is not taken.
- **Stealth path**: the dedicated context is created with `storageState` alongside the stealth options. It was already per-fetch, so there is no leak risk.
- **CDP / hosted scraping browser**: a new context is created with `storageState`. An existing remote context (`contexts[0]`) can't take one after creation, so it is driven as before, and a `warn` log says the state wasn't applied rather than failing silently. This is a small `cdpContext()` helper shared by both call sites. With a hosted scraping browser (`WIGOLO_SCRAPING_BROWSER_WSS`) that has no context yet, this means the saved session is loaded into the remote browser.
- `docs/configuration.md`: one sentence on the above.

Not included: `userDataDir` / `WIGOLO_CHROME_PROFILE_PATH` (#161) has the same gap, but fixing it needs `launchPersistentContext`, which is a different shape, so I kept this PR to the storage state. Credit to @MeRezaRezaei (who reported this issue) for #527: after review pointed out the pooled-context leak, it moved to a dedicated context that never returns to the pool. This PR takes the same approach, and the unit test file follows #527's layout, but it opens the context on the shared browser instead of launching a browser per fetch.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Testing

- [ ] `npm test`: I ran `npx vitest run tests/unit` and the whole `tests/integration/fetch/browser-pool.test.ts` file, not the full suite. Results below.
- [x] `npm run lint` passes
- [x] Added/updated tests for the new behavior:
  - `tests/unit/fetch/browser-pool.storage-state.test.ts`, 6 tests:
    - The pooled path creates the context with the storage state and closes it.
    - A later anonymous fetch gets a clean context.
    - The pooled path is unchanged without a storage state.
    - The stealth context is seeded.
    - A CDP browser with no context gets a seeded one.
    - An existing CDP context is driven as before.
  - With only `browser-pool.ts` reverted, the 4 behaviour tests fail and the 2 unchanged-behaviour guards pass.
  - `tests/integration/fetch/browser-pool.test.ts`: a real headless Chromium fetches a local page that echoes the `Cookie` header. With a storage-state file it sends `session=abc123`, and the anonymous fetch right after sends no cookie. This test fails without the fix. The whole file passes 20/20.

Note on the full unit run (`vitest run tests/unit`): 7926 passed, 3 failed. The 3 are the `PERMISSION_DENIED` cases in `tests/unit/cli/tui/config-writer-json.test.ts`, which fail identically on unpatched `main` here because my sandbox runs as root, which ignores file modes. The touched suites (`tests/unit/fetch`, `tests/integration/fetch/browser-pool.test.ts`) pass in full.

## Checklist

- [x] Follows [Conventional Commits](https://www.conventionalcommits.org/)
- [x] Focused change (no unrelated refactoring)
- [x] I have read `CONTRIBUTING.md` and agree to its contribution terms
