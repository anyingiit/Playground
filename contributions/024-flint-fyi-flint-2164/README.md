# flint-fyi/flint#2164 — Add functionDeclarationStyles to TS plugin's stylisticStrict

| | |
|---|---|
| Issue | https://github.com/flint-fyi/flint/issues/2164 |
| Tier | 新锐 |
| Labels | `good first issue`, `status: accepting prs`, `plugin: ts`, `package: rule-data`, `type: feature` |
| Status | ✅ ready |
| Duplicate-PR check | PR search for `functionDeclarationStyles` / `2164` finds only #1599 (the original rule implementation, closed in Jan 2026). The issue has no assignee, no comments and no linked PR (checked when the issue was picked and again after the work was done, 2026-09-24) |
| Base | `main` @ `664805c` (2026-09-24) |

## 为什么这个项目符合"新锐"标准

- **Flint** (https://github.com/flint-fyi/flint): an experimental, fast linter for JS/TS and other languages (ESLint/Biome/oxlint alternative), with a hybrid TS-typed core.
- ~308 stars and 33 forks. Created 2025-05-22, so it is about 16 months old. MIT licence.
- Led by Josh Goldberg (typescript-eslint maintainer), with real human maintainers. Several different human contributors (Eli, michael faith, Konv Suu and others) have had commits merged recently, plus Renovate. There were 5+ commits on the day the issue was picked (2026-09-24).
- Value: a new-generation, type-aware linter with 296 rules. It dogfoods itself (`pnpm flint` runs on its own repo in CI).
- The repo is not an issue farm. Issues are written by the maintainer, with a real triage label flow (`status: accepting prs`).

## 需要提交者注意 (AI policy!)

- Flint has an explicit AI policy: https://flint.fyi/project/contributing-with-ai. AI-assisted code is allowed if the contributor reviews it closely and understands it well enough to handle review feedback without the AI. **They ask that issue, comment and PR description text not be AI-generated** ("AI PR descriptions … tend to just be nearly-verbatim descriptions of the diff"). They reserve the right to close PRs that don't follow this.
  → **Before submitting, read the diff yourself and rewrite the PR description below in your own words.** Keep it short. Treat the draft below only as notes, and keep the disclosure sentence.
- The PR title must follow Conventional Commits (the project squash-merges): `feat(ts): add functionDeclarationStyles to stylisticStrict`.
- Fill in the repo's PR template (`.github/PULL_REQUEST_TEMPLATE.md`): PR Checklist (3 boxes) + Overview.
- There's a changeset, `.changeset/function-declarations-strict.md`: `@flint.fyi/ts` minor, because the default option changes, and `@flint.fyi/rule-data` patch. Maintainers may prefer `patch`. Earlier preset-only changes were patch. Adjust the bump if they ask.
- No DCO or sign-off requirement.

## 问题理解

`ts/functionDeclarationStyles` (the equivalent of ESLint's `func-style`) was implemented in #1599 but not added to any preset. The maintainer's issue asks to:
1. add it to the TS plugin's `stylisticStrict` preset, and
2. change the default `style` from `"expression"` to `"declaration"`.

Preset membership comes from each rule's `about.presets` (`packages/core/src/plugins/createPlugin.ts` → `collectPresetsFromRules`). The site's rule table and preset metadata come from `packages/rule-data/src/data.json` (`"preset": "stylistic", "strictness": "strict"` is how `stylisticStrict` rules are recorded, for example `caughtVariableNames`).

## 合理性判断

- The request is from the lead maintainer, labelled `status: accepting prs` + `good first issue`, and still open with no activity.
- **Side effect:** the repo lints itself with `ts.presets.stylisticStrict` (`flint.config.ts`). Adding the rule with the new default immediately produced **33 `ts/functionDeclarationStyles` reports in 21 files of Flint's own code**, which would fail the CI `pnpm run flint` job. So the PR also converts those `const x = (...) => {...}` helpers into function declarations. That is the dogfooding the preset implies.
- There are 2 intentional `flint-disable-next-line ts/functionDeclarationStyles` exceptions:
  - `createTypeScriptServerHost.ts`: `patchedReaddirSync` is typed as `typeof fs.readdirSync`, which is overloaded and already needs an `@ts-expect-error`. A declaration would need its own overload-compatible signature plus casts at both assignment sites.
  - `createNodeVisitorsForFile.ts` (the `exit`-only visitor): converting it to a hoisted function declaration loses TS's narrowing of `exit` inside the closure (TS18048 `'exit' is possibly 'undefined'`). The sibling `enter` visitors in the same function are also arrow functions (inside a ternary, which the rule doesn't flag).

## 改动 (single commit)

- `packages/ts/src/rules/functionDeclarationStyles.ts`: `presets: ["stylisticStrict"]`; `style` default `"expression"` → `"declaration"`.
- `packages/ts/src/rules/functionDeclarationStyles.test.ts`: tests for the new default (function expressions/arrows flagged with no options, `function` declarations valid with no options, `allowArrowFunctions: true` alone is valid). The old default-dependent cases now pass `{ style: "expression" }` explicitly.
- `packages/rule-data/src/data.json`: `"preset": "stylistic"`, `"strictness": "strict"` (`sort-data --check` still passes).
- `packages/site/.../functionDeclarationStyles.mdx`: the examples and option docs show `"declaration"` as the default, and the option JSON examples were updated to match.
- `.changeset/function-declarations-strict.md`.
- Dogfooding: 31 helpers in core / markdown-language / yaml-language / typescript-language / package-json / plugin-flint / rule-tester tests / ts / vitest / vue are now `function` declarations, with no behaviour change. `conditionalExpects`' `inTestCase && depth++` one-liners became `if` bodies (their return value was never used). `globs/all.ts` now spells out the `(config: ProcessedConfigDefinition): FilesGlobObject` signature instead of `: FilesComputer`. `eslint --fix` (perfectionist/sort-modules) reordered 3 files' functions.

## 验证

Environment: Node v26.9.0 (repo requires >=26.1.0), pnpm 11.27.1, `pnpm install --frozen-lockfile --ignore-scripts`, `pnpm --filter=site prebuild` (astro sync, as in CI).

| Command | Base `664805c` | Patched |
|---|---|---|
| `pnpm exec vitest run --project ts packages/ts/src/rules/functionDeclarationStyles.test.ts` (old test) | 14/14 pass | – |
| same, **new test**, base rule (red) | **3 failed** / 15 passed (the 2 default-invalid cases + default-valid `function doSomething() {}`) | **18/18 pass** (green) |
| `pnpm run flint:cache-ignore` (dogfood) | – | rule change alone: 33 `ts/functionDeclarationStyles` reports → after conversions: **No linting issues found** (2351 files, 296 rules) |
| `pnpm exec vitest run --project='!e2e'` | – | **596 files / 9936 tests passed** |
| `pnpm exec vitest run --project e2e` | – | 4/4 passed |
| `pnpm exec tsc -b` | – | exit 0 |
| `pnpm run lint` (eslint --max-warnings 0) | – | pass |
| `pnpm exec prettier --check <changed files>` | – | pass |
| `pnpm run --filter=rule-data sort-data --check` | – | pass |
| `pnpm run build` + `pnpm run lint:knip` | – | pass |

Not run: `pnpm --filter=site check` (astro check), `pnpm dedupe --check` (lockfile untouched), `lint:knip:prod`.

## 如何提交

```bash
git clone https://github.com/<you>/flint && cd flint
git checkout -b feat/function-declaration-styles-stylistic-strict origin/main
git am /path/to/0001-feat-ts-add-functionDeclarationStyles-to-stylisticSt.patch
# optionally re-run: pnpm i && pnpm --filter=site prebuild && pnpm run flint && pnpm test --project ts
git push -u origin HEAD   # open PR against flint-fyi/flint:main
```

## PR title

`feat(ts): add functionDeclarationStyles to stylisticStrict`

## PR body (draft: **rewrite the prose in your own words** per Flint's AI policy)

```markdown
## PR Checklist

- [x] Addresses an existing open issue: fixes #2164
- [x] That issue was marked as [`status: accepting prs`](https://github.com/flint-fyi/flint/issues?q=is%3Aopen+is%3Aissue+label%3A%22status%3A+accepting+prs%22)
- [x] Steps in [CONTRIBUTING.md](https://github.com/flint-fyi/flint/blob/main/.github/CONTRIBUTING.md) were taken

## Overview

Adds `functionDeclarationStyles` to `stylisticStrict` and switches its default `style` to `"declaration"`, as proposed in the issue.

Since this repo lints itself with `ts.presets.stylisticStrict`, turning the rule on flagged 33 spots in Flint's own source; those are converted to function declarations. Two places keep an arrow function with a `flint-disable-next-line` instead:
- `patchedReaddirSync` in `createTypeScriptServerHost.ts`, which is typed as the overloaded `typeof fs.readdirSync`
- the exit-only `visit` in `createNodeVisitorsForFile.ts`, where a hoisted declaration loses the narrowing of `exit` (TS18048)

The changeset marks `@flint.fyi/ts` as `minor` because the default option changes. Happy to switch it to `patch` if you prefer.

Verified locally: `pnpm run flint` (no issues), `pnpm exec vitest run` (all projects), `pnpm exec tsc -b`, `pnpm run lint`, `pnpm run lint:knip`, `sort-data --check`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code; I reviewed it and verified it as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it. No hard feelings at all 🙂
```
