# medusajs/medusa#16969 — applyTranslations collects IDs from alias services

- Issue: https://github.com/medusajs/medusa/issues/16969
- Category: high-activity / high-star project (Medusa, ~30k★, very active)
- Labels: `good first issue`, `type: bug`
- Status: implemented + tested locally, **PR not opened** (session has no fork/push rights outside this repo)

## Problem
With a locale set, `applyTranslations` (`packages/core/utils/src/translations/apply-translations.ts`)
recursively collects *every* nested `id`, including ids of entities returned by
aliased Remote Query services (e.g. a custom CMS with numeric ids). The resulting
query mixes types, `reference_id IN (770, 'prod_…')`, and Postgres fails with
`operator does not exist: text = integer`.

## Fix
`gatherIds` now only collects **string** ids. `translation.reference_id` is a text
column and every translatable Medusa entity uses string ids, so a numeric id can
never have a translation — dropping it is safe and removes the type error.
A changeset (`@medusajs/utils: patch`) is included.

## Tests
- New spec: `should only gather string ids and ignore numeric ids from aliased services`
- `apply-translations.spec.ts`: 17/17 pass with the fix; the new test fails without it.
  (Ran with a standalone jest + @swc/jest harness because a full monorepo install
  was too heavy for this session; re-run `yarn test` in `packages/core/utils` before opening the PR.)

## How to submit
```bash
git clone https://github.com/<you>/medusa && cd medusa   # your fork
git checkout -b fix/translations-ignore-non-string-ids origin/develop
git am /path/to/0001-fix-utils-ignore-non-string-ids-when-gathering-trans.patch
git push -u origin HEAD
```
Base branch: `develop`.

### PR title
fix(utils): ignore non-string ids when gathering translation reference ids

### PR body
```
Fixes #16969

**What**
`applyTranslations` collected every nested `id`, including numeric ids from entities
returned by aliased Remote Query services (e.g. a custom CMS). Mixed into the text
`reference_id IN (...)` filter, they made Postgres throw
`operator does not exist: text = integer`.

**How**
Only gather string ids in `gatherIds`. Translations are keyed by a text
`reference_id` and Medusa entity ids are strings, so non-string ids can never
match a translation.

**Testing**
Added a unit test in `apply-translations.spec.ts` covering a product with a nested
`cms: { id: 770 }` object; it asserts only `"prod_1"` is sent to the translations
query and that translations still apply.
```
