Part of #4489 (SCSS / Stylus `@keyframes` `from` / `to` item only)

## Description

CSS and Less highlight the `from` / `to` keyframe selectors as `selector-tag`; SCSS and Stylus left them as plain text. The difference is visible in the shared `css_consistency` markup test:

```scss
@keyframes important1 {
  from { margin-top: 50px; }   /* css/less: hljs-selector-tag, scss/stylus: plain */
  50%  { margin-top: 60px !important; }
  to   { margin-top: 100px; }
}
```

### Changes

- `src/languages/lib/css-shared.js`: new shared `KEYFRAME_POSITION` mode (the issue asks for shared matchers in `css-shared.js` rather than copy-paste). It is a multi-match: an unscoped `(?:^|[\s,{}])` prefix, then `from` / `to` scoped as `selector-tag`, followed by a lookahead for `{`, `,` or end of line. The language lint config targets ES2015, so I used the prefix group instead of a lookbehind.
- `scss.js` and `stylus.js` both add `modes.KEYFRAME_POSITION` next to their `selector-tag` mode. `css.js` / `less.js` are unchanged.
- The `scss` and `stylus` `css_consistency.expect.txt` files now match the css one for the `@keyframes important1` block.
- New `keyframes` markup tests for scss and stylus. Besides the positive cases (`from, 50% {`, `to {`, and Stylus indentation syntax with a bare `from` / `to` line), they check that these stay plain:
  - `@for $i from 1 through 3 { ... }` (SCSS; the `@` at-rule mode already consumes it)
  - `linear-gradient(to right, red, blue)` in a property value
  - BEM / Vue transition style selectors `&-enter-from, &-leave-to`
- `CHANGES.md`: entry under 11.12.1 "Core Grammars".

I did not touch function highlighting (#4497), escaped selector characters (#4513) or `preserve-3d` (#4545).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

Assisted-by: Claude Code

## Related issue

Part of #4489. This covers only the SCSS and Stylus `@keyframes` `from` / `to` items of the checklist, so the issue should stay open.

## Checklist

- [x] Added markup tests, or they don't apply here because...: `test/markup/{scss,stylus}/keyframes.txt` are new, and both `css_consistency.expect.txt` files are updated. On `main` the 4 tests fail; with this change they pass.
- [ ] I have read and followed our [AI-assisted contributions](../docs/ai-contributions.md) policy (human review, no slop)
- [x] Tests pass locally:
  - `node tools/build.js -t node css less scss stylus && ONLY_LANGUAGES="css less scss stylus" npm run test-markup` → 16 passing
  - `node tools/build.js -t node && npm test` (markup + detect + api + parser) → 1652 passing, 3 pending, 0 failing
  - `npm run lint-languages` → clean. `npm run lint` → only the existing "ignored file" warning for `tools/vendor/jquery-2.1.1.min.js`
- [x] `CHANGES.md` is updated: one line under 11.12.1 "Core Grammars", plus a contributor link
- [ ] Documentation is updated (if applicable): n/a, grammar-only change
