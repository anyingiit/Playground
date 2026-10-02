### Reasons for making this change

A string field with a `const` and `ui:widget: 'checkbox'` currently throws `No widget 'checkbox' for type 'string'`, so there is no way to render the "please confirm" checkbox from #3882:

```json
{ "title": "Confirmation", "type": "string", "const": "foo" }
```

With this change `StringField` handles that one case (`ui:widget` is `checkbox` and `schema.const` is a string) by rendering the registry's `CheckboxWidget` (or a widget registered as `checkbox`, if there is one) and translating between the two shapes:

- the box is checked when the value equals the `const`;
- checking it sets the value to the `const`, unchecking it clears the value (`undefined`, so it is dropped from the submitted data just like a cleared text input);
- `onFocus`/`onBlur` receive the same string value instead of a boolean.

Because it is done in `StringField`, every theme picks it up through its own `CheckboxWidget` (I spot-checked `@rjsf/mui` and `@rjsf/antd` locally). A `required` const keeps the checkbox's `required` attribute (via `schemaRequiresTrueValue`), and an unchecked box is reported as a missing required property. A string without a `const` still throws as before.

One behavior worth calling out: with the default `experimental_defaultFormStateBehavior.constAsDefaults: 'always'`, the `const` is populated as a default, so the box starts checked (unchecking it works and sticks). For an opt-in confirmation, `constAsDefaults: 'never'` starts it unchecked. I documented this in `widgets.md` rather than changing the defaults behavior — happy to adjust if you'd prefer something else.

Since this adds a feature, the changelog entry goes under a `6.12.0` heading (renamed from `6.11.1`).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

fixes #3882

### Checklist

- [x] **I'm updating documentation**
  - [ ] I've [checked the rendering](https://rjsf-team.github.io/react-jsonschema-form/docs/contributing) of the Markdown text I've added — one bullet added to `docs/usage/widgets.md`; not rendered with mkdocs locally
- [x] **I'm adding or updating code**
  - [x] I've added and/or updated tests. — 7 new tests in `packages/core/test/StringField.test.tsx` (all fail on `main` with `No widget 'checkbox' for type 'string'`); `packages/core`: `vitest run` 36 files / 2089 tests passed; `packages/playground`: 10 passed; `pnpm run lint` (oxlint) on core/playground, `oxfmt --check` on changed files, `pnpm run typecheck`, `pnpm run knip` all pass. No snapshot changes were needed (the snapshot suites don't use this schema).
  - [x] I've updated [docs](https://rjsf-team.github.io/react-jsonschema-form/docs) if needed
  - [x] I've updated the [changelog](https://github.com/rjsf-team/react-jsonschema-form/blob/main/CHANGELOG.md) with a description of the PR
- [x] **I'm adding a new feature**
  - [x] I've updated the playground with an example use of the feature — `confirmation` field in the Widgets sample
