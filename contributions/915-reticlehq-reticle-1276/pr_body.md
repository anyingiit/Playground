## What & why

A Vinext app depends on `next` (for the API surface) and usually keeps a `next.config.*`, but it builds through Vite and never evaluates the Next config. `detect.ts` tries `Framework.NEXT` before `Framework.VITE`, so `init` classified it as Next, wired `withReticle` into a file Vinext never reads, and the app never connected.

Change (in `init/src/detect/detect.ts`): `FrameworkSignals` gains an optional `depsUnless` — dependency names whose presence disproves *both* the dependency and the config-file signal of that framework. `Framework.NEXT` declares `depsUnless: ['vinext']`, so a `{ next, vinext, vite }` project falls through the precedence chain to the Vite branch, which wires the Vite plugin into `vite.config.*` (the config Vinext actually runs). I went with this rather than reordering `DETECTION_ORDER`, since "next before vite" is still correct for every other project carrying both. It also covers a Vinext app that keeps its `next.config.ts`, which only ignoring the `next` dependency would have missed.

A changelog fragment is added at `.changes/1276-vinext-detected-as-next.md`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Closes #1276

## How it was verified

New test in `init/src/detect/detect.test.ts`: a fixture with deps `{ next, vinext, vite }` and both `next.config.ts` and `vite.config.ts` must detect as `Framework.VITE`.

- **I checked that the test fails without the fix**: before changing `detect.ts`, `npx vitest run src/detect/detect.test.ts` (in `init/`) gave `1 failed | 41 passed` (`Expected: "vite"`, `Received: "next"`). With the fix: `42 passed`.

## Gates run

- [x] `pnpm lint && pnpm typecheck && pnpm test:unit`, scoped to the touched package: `turbo run lint typecheck test:unit --filter=@reticlehq/init` (5/5 tasks OK, 91 files / 1060 tests pass), plus `node scripts/check-boundaries.mjs`, `node scripts/check-lossy-transforms.mjs` and `prettier --check .` (all clean). The full monorepo `test:unit` was not run locally.
- [ ] `pnpm test:e2e` (~8 min)
- [ ] `pnpm gate:install` (~15 min) — touches `reticle init` detection, but not run locally (no Vinext app in `reticle-fixtures`); leaving it to CI
- [ ] `pnpm test:e2e:desktop` (~3 min)
- [ ] None of the above tiers apply to this change

## Checklist

- [x] **Every commit is signed off** (`git commit -s`)
- [x] Tests added/updated (RED → GREEN); the change is covered by a test that would fail without it
- [x] No `any`, no free strings (wire strings live in `@reticlehq/core`), no non-null `!`
- [x] No `console.log` or internal tracking codes left in the diff
- [x] Each changed file is under the 1000-line cap (`detect.ts` is 607 lines)
- [x] Docs updated, and a user-facing change adds a **new file** under `.changes/`: `.changes/1276-vinext-detected-as-next.md` (no docs page lists detection precedence, so no docs change)
- [ ] Security-affecting? — n/a
