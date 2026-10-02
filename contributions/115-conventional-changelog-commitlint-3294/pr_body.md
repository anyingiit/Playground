## Description

`start-case` compared the (quote-stripped) subject with es-toolkit's `startCase()`. That helper also splits words on periods and digits, so a subject like `Add Module 1.0.0` becomes `Add Module 1 0 0` and `Add Core.js` becomes `Add Core Js`, and both were reported as not start case.

This PR keeps the check in `@commitlint/ensure` (`case.ts`) but runs it per space-separated word for `start-case` only:

- A word still passes when `startCase(word) === word` (unchanged behaviour for plain words, e.g. `fix: Typo`, `chore: Release`, `Sub Ject`, `Äm Ne`).
- A word that contains periods or digits also passes when the part before the first period/digit is start case (or the word starts with a digit) and the rest only contains letters, digits and periods: `1.0.0`, `Core.js`, `Node.js`, `V2`, `Es2015`.
- Still rejected: lowercase words (`module`, `core.js`, `v1.0.0`), camel case (`FooBar.js`), words with `_` or `-` (`Foo_bar`, `Foo-bar`, `foo_bar`), and consecutive spaces (`Add  Module 1.0.0`), as before.

The existing early return (empty subject, or subject whose transformed form starts with a digit) is untouched, `toCase()` is untouched (so the prompt / cz-commitlint case forcing is unchanged), and no other target case (sentence-case, lower-case, …) changes behaviour.

One edge to be aware of: with `"never", "start-case"`, subjects such as `Add Core.js` or `Add Module 1.0.0` are now considered start case and will be rejected, which is consistent with the `always` side but is a behaviour change at the edges.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Motivation and Context

Fixes #3294 — `subject-case: [2, "always", "start-case"]` rejects `feat: Add Module 1.0.0`; the only workaround today is quoting the version.

## Usage examples

```js
// commitlint.config.js
export default {
  rules: {
    "subject-case": [2, "always", "start-case"],
  },
};
```

```sh
echo "feat: Add Module 1.0.0" | commitlint # passes (failed before)
echo "feat: Add Core.js" | commitlint # passes (failed before)
echo "fix: Typo" | commitlint # passes (as before)
echo "feat: Add module 1.0.0" | commitlint # fails (as before)
echo "feat: Add Foo_bar 1.0.0" | commitlint # fails (as before)
```

## How Has This Been Tested?

Following the test-driven flow, there are two commits:

1. `test(ensure): …` adds cases to `@commitlint/ensure/src/case.test.ts` (true for `Add Module 1.0.0`, `Add Core.js`, `Support Node.js 22 And Es2015`, `Typo`, `Release`; false for `Add module 1.0.0`, `Add core.js`, `Add Module v1.0.0`, `Add FooBar.js`, `Add Foo_bar 1.0.0`, `Add Foo-bar 1.0.0`, `Add Foo_bar.js`, `Add  Module 1.0.0` with a double space) and a rule-level case for `feat: Add Module 1.0.0` to `@commitlint/rules/src/subject-case.test.ts`. On this commit 4 tests fail on assertions.
2. `fix(ensure): …` makes them pass.

Run locally (Node 22.22, pnpm 12.8.0):

- `pnpm build`
- `pnpm vitest run @commitlint/ensure/src/case.test.ts @commitlint/rules/src/subject-case.test.ts` — 4 failed before the fix, 147/147 after
- `pnpm vitest run` — 91 files / 1273 tests pass
- `pnpm format`, `pnpm lint` — clean
- the CLI examples above with the built `@commitlint/cli/lib/cli.js`
- `commitlint --from <base> --to HEAD` on the two commits

## Types of changes

- [x] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)

## Checklist:

- [ ] My change requires a change to the documentation.
- [ ] I have updated the documentation accordingly.
- [ ] I have verified that any documentation examples I added/changed actually work.
- [x] I have added tests to cover my changes.
- [x] All new and existing tests passed.
- [x] For a feature/bug fix, my commits follow the [test-driven flow](https://github.com/conventional-changelog/commitlint/blob/master/.github/CONTRIBUTING.md#test-driven-development): a failing-test commit, then the implementation.
