## What & why

A Vinext app depends on `next` (for the Next.js APIs it re-implements) but builds with Vite and never evaluates `next.config.*`. `Framework.NEXT` is first in `DETECTION_ORDER`, so `detectFramework` matched it on the `next` dependency, and the plan wired `withReticle` into a config nothing runs — the app never connects.

Fix: `FrameworkSignals` gains an optional `depsUnless` — dependency names whose presence disproves both of a framework's signals (deps and config files), so detection moves on down the chain. Only `Framework.NEXT` uses it, with `vinext`. A Vinext app then falls through to `Framework.VITE` through the `vite` dependency it declares, which is the outcome the issue asks for. A `next.config.*` left in a Vinext project no longer matches either. Plain Next apps, and apps that list both `next` and `vite` without `vinext`, are unchanged (the existing "prefers next over vite" test still passes).

I went with "detected as Vite" as the issue's completion criteria allow, rather than a separate `Framework` entry. Happy to switch to a distinct entry if you'd rather have Vinext-specific wiring later (for example if the Vite plugin's `transformIndexHtml` injection turns out not to reach Vinext's server-rendered HTML).

Changelog: `.changes/1276-vinext-detected-as-next.md` (`### Fixed`).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Closes #1276

## How it was verified

- New test in `init/src/detect/detect.test.ts`: `{ next, vinext, vite }` plus `next.config.ts` + `vite.config.ts` → `Framework.VITE`.
- **Checked that the test fails without the fix** (per CONTRIBUTING's AI-assisted rule): with `detect.ts` reverted, `npx vitest run src/detect/detect.test.ts` → `1 failed | 41 passed` (`expected 'next' to be 'vite'`); with the fix → `42 passed`.
- `pnpm turbo run lint typecheck test:unit --filter=@reticlehq/init` → 5/5 tasks successful, init unit tests `91 files / 1060 tests passed`.
- `prettier --check .` → clean; `node scripts/check-boundaries.mjs` and `node scripts/check-lossy-transforms.mjs` → OK.

## Gates run

- [x] `pnpm lint && pnpm typecheck && pnpm test:unit` (~2 min — **always**) — run scoped to `@reticlehq/init` (the only package touched), plus the root `format:check` / boundary / lossy-transform checks
- [ ] `pnpm test:e2e` (~8 min) — _touched the tool surface, `core`, an observer, or telemetry_
- [ ] `pnpm gate:install` (~15 min) — _touched `reticle init`, `vite-plugin`, `next`, or `babel-plugin`_ — not run locally (needs a local registry + real fixture apps); the change is confined to the pure detection function
- [ ] `pnpm test:e2e:desktop` (~3 min) — _touched `adapters/realm/electron`, `adapters/realm/tauri`, or desktop capture_
- [ ] None of the above tiers apply to this change

## Checklist

- [x] **Every commit is signed off** (`git commit -s`) — CI's DCO check fails the PR without it. Already pushed? `git rebase --signoff origin/main && git push --force-with-lease`
- [x] Tests added/updated (RED → GREEN); the change is covered by a test that would fail without it
- [x] No `any`, no free strings (wire strings live in `@reticlehq/core`), no non-null `!`
- [x] No `console.log` or internal tracking codes left in the diff
- [x] Each changed file is under the 1000-line cap
- [x] Docs updated, and a user-facing change adds a **new file** under `.changes/` (never edit `CHANGELOG.md` — that file is assembled at release time, and editing it is what makes PRs conflict; format in `.changes/README.md`)
- [ ] Security-affecting? — n/a
