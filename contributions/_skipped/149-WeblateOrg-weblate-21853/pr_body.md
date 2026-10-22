## Description

shields.io recently added a blurred shadow behind badge text to improve contrast (WCAG) of the white text, and Weblate's SVG status badges still use the older look with only a sharp 1px shadow.

This mirrors the current shields.io `flat` renderer in `weblate/templates/svg/badge.svg` (used by the `svg` status badge and the language badge):

- adds a `feGaussianBlur` filter (`stdDeviation="1.6"`, i.e. shields.io's `16` at their 10× text scale),
- renders a blurred shadow (`fill-opacity=".8"`) in addition to the existing sharp shadow (`fill-opacity=".3"`), both offset by 1px,
- wraps the shadow texts in `<g aria-hidden="true">` so assistive technologies only see the real label/value.

Badge sizes and text positions are unchanged. A regression test checks that the badge defines the blur filter, that both visible texts have a blurred shadow, and that shadows are `aria-hidden`. Changelog entry added to `docs/changes.rst`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #21853

## Checklist

- [x] Tests pass locally (`pytest -n 3 weblate/trans/tests/test_widgets.py` with `DJANGO_SETTINGS_MODULE=weblate.settings_test` on PostgreSQL 16: 293 passed; the new `test_svg_badge_text_has_blurred_shadow` fails without the template change and passes with it)
- [x] `ruff check` / `ruff format --check` (0.16.9) pass on the changed Python file; `xmllint` passes on the SVG template
- [x] `docs/changes.rst` is updated (Improvements in 2026.10.1)
- [ ] Documentation is updated — n/a (no behavior/config change)
