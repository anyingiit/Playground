## Proposed changes

On a multi-remote browser only `$` and `$$` were turned into a `MultiRemoteElement` / `MultiRemoteElementArray`. `custom$`, `react$`, `shadow$` and their `$$` variants went down the default path of the multi-remote command wrapper in `multiRemote.ts` and returned one raw result per instance (`[Element, Element]`, `[ElementArray, ElementArray]`). Those results had no `isMultiRemote`, `getInstance()` or `select()`, element commands could not run on them, and the list metadata (`selector`, `foundWith`, `parent`, `props`) that matchers use was missing (#15851).

This PR:

- sends `custom$`, `react$` and `shadow$` down the same path as `$` (`MultiRemote.elementWrapper`), and `custom$$`, `react$$` and `shadow$$` down the same path as `$$` (`ElementArray.fromAsyncCallback`, zipped per index);
- keeps each `$$` variant's own metadata on the list, matching the single-session lists: `foundWith` is the command name, `props` is `strategyArguments` for `custom$$` and `[props, state]` for `react$$`. For `custom$$` the entries keep the selector they were found with, because the first argument is a strategy name, not a selector;
- updates the multi-remote types: `custom$$` / `react$$` now return `MultiRemoteElementArray` (the type comment said they were not zipped), and `shadow$` / `shadow$$` on a `MultiRemoteElement` return `MultiRemoteElement` / `MultiRemoteElementArray` (before, they were typed as an array of per-instance results);
- updates the three docs that described the old behavior (`website/docs/Multiremote.md`, `website/docs/v10Migration.md` and the `wdio-v10-migration` skill, kept in sync as `AGENTS.md` asks).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

Closes #15851

## How you tested

- [x] Unit tests for the touched package(s): `pnpm run test:package webdriverio` → 189 files, 1539 passed, 2 skipped, no type errors. The new tests in `packages/webdriverio/tests/multiRemote.test.ts` (`element queries other than $ and $$ (#15851)`, 6 tests) fail without the fix (6 failed / 21 passed) and pass with it (27 passed).
- [x] Type definition tests: `test:typings:webdriver|webdriverio|mocha|jasmine|cucumber` all pass (`npx tsc --skipLibCheck` in each). The new lines in `tests/typings/webdriverio/async.ts` fail against a build without the fix (5 errors, e.g. `Property 'isMultiRemote' does not exist on type 'MultiRemoteElement[]'`).
- [x] Smoke: `pnpm run test:smoke multiRemote` passes (regression check only; the mocked-driver suite does not call these queries). I could not run a real-browser example script here (no browsers or drivers in my environment).
- Also: `npx oxlint` on the changed files is clean, `npx tsc --noEmit -p packages/webdriverio/tsconfig.json` passes, and the multi-remote naming check from `AGENTS.md` reports no lines from this diff.

## Types of changes

- [ ] Polish (an improvement for an existing feature)
- [x] Bugfix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [x] Documentation update (improvements to the project's docs)
- [ ] Specification changes (updates to WebDriver command specifications)
- [ ] Internal updates (everything related to internal scripts, governance documentation and CI files)

## Checklist

- [x] I have read the [CONTRIBUTING](https://github.com/webdriverio/webdriverio/blob/main/CONTRIBUTING.md) doc
- [x] I have added tests that prove my fix is effective or that my feature works
- [x] I have added the necessary documentation (if appropriate)
- [x] I have added proper type definitions for new commands (if appropriate)
- `CHANGELOG.md`: n/a (the release process generates it)

## Backport Request

- [x] This change is solely for `v10` (targets the `v10` branch, as the issue is on the v10 milestone) and doesn't need to be back-ported

## Further comments

The `$$` variants change from "one result per instance" to one zipped `MultiRemoteElementArray`. That is what the issue asks for and what the `custom$` / `react$` types already promised, but it does change the runtime shape of `custom$$` / `react$$` / `shadow$$` on multi-remote. Because this is v10, I did not add a flag for it.

### Reviewers: @webdriverio/project-committers
