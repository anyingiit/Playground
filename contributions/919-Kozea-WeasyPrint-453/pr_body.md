## Description

Add the `print-color-adjust` property from CSS Color Adjustment Level 1 (`economy` | `exact`, initial `economy`, inherited). Until now WeasyPrint dropped it with an "unknown property" warning.

WeasyPrint never removes backgrounds or changes colors to save ink, so both values render the same. With this change the declaration is accepted silently, and the value is kept in the computed style. The docs say this in a new "CSS Color Adjustment Module Level 1" section. The section also mentions `color-scheme`, which is already supported, and says that `forced-color-adjust` is not.

The prefixed `-webkit-print-color-adjust` from the issue is still ignored, like other non-`-weasy-` prefixed properties. I can add it as an alias if you'd like that.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #453

## Checklist

- [x] Tests pass locally: `python -m pytest tests/css/test_validation.py tests/css/test_common.py -k print_color_adjust` gives 7 failed without the fix and 7 passed with it. On the full `python -m pytest -n 4`, the same 763 tests fail before and after the change, all because Ghostscript (`gs`) is not installed on my machine. There are no new failures. `python -m ruff check` passes.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the changelog is written by maintainers at release time
- [x] Documentation is updated (if applicable) — new section in `docs/api_reference.rst`
