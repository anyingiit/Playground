# Pull Request

## Description

Adds `openmed/core/language_coverage_diff.py`, which compares two versioned clinical language-pack coverage manifests by canonical locale and reports `added`, `removed`, `improved`, `regressed` and `changed` entries, plus an `unchanged` list and per-status counts. Output is byte-stable JSON (`to_json()`) and Markdown (`to_markdown()`).

There was no existing coverage-manifest format in the repo, so this PR defines a small closed one (happy to adjust it to whatever the readiness/conformance work settles on):

- manifest: exactly `version` + `entries`;
- entry: exactly `locale`, `script` (ISO 15924), `identifier_classes` (lowercase tokens), `surrogate_support` (`none` < `partial` < `full`), `evidence_digest` (`sha256:<64 hex>`).

Design notes:

- Locales go through the existing `normalize_locale_tag`, so case variants and explicit `aliases` match the same entry; canonical duplicates are rejected.
- Entries and identifier classes are sorted, so reordered manifests give identical output.
- A locale that lost an identifier class or surrogate support is `regressed`, even if it also gained something, so a mixed change is never reported as an improvement. Script- or digest-only differences are `changed`.
- Unknown keys are rejected and errors are constant, value-free categories (same style as `LocaleTagError`), so fixture text, model paths or raw examples cannot reach the diff or the error messages.
- Standard library only; no models, fixtures, network or evaluation. Release gating stays out of scope (only a `has_regressions` convenience flag).

**Motivation / disclosure:** I had some spare AI coding-assistant quota and am using it to try to help projects with open good-first-issues. The change was prepared with an AI coding assistant and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Type of Change
- [x] New feature (non-breaking change which adds functionality)
- [x] Documentation update
- [x] Test addition/improvement

## Changes Made
- New `openmed/core/language_coverage_diff.py` (`parse_language_coverage_manifest`, `diff_language_coverage`, `LanguageCoverageDiff.to_json/to_markdown`).
- New `tests/unit/core/test_language_coverage_diff.py` with golden JSON/Markdown for equal, added, removed, changed, alias and reordered manifests, and validation-failure cases.
- New `docs/i18n/language-coverage-diffs.md`, registered in `mkdocs.yml` nav and `docs/brand/system/publication.yml`.
- `CHANGELOG.md` entry under Unreleased / Added.
- `tests/browser/brand/budgets.json`: the new guide grows the staged Pages artifact by about 238 KB (mostly the page itself plus the extra nav item on every page), which is more than the remaining headroom. Following the existing notes, the ceilings are set to the measured build plus the same 115486-byte aggregate and 5792-byte search allowances; other limits are unchanged.

## Testing
- [x] I have added tests that prove my fix is effective or that my feature works
- [x] New and existing unit tests pass locally with my changes
  - `pytest tests/unit/core/test_language_coverage_diff.py -q` → 24 passed
  - `pytest tests/unit/test_docs_publication.py tests/unit/core/test_locale_tag.py -q` → passed (also with the locked docs extra installed, so the mkdocs hook tests run)
  - `python scripts/docs/stage_pages.py` builds and validates; the staged artifact fits the updated byte budgets
  - `pytest tests/unit/core -k "language or locale"` → 664 passed; 11 modules could not be collected in my minimal environment (optional deps such as numpy/jsonschema not installed), unrelated to this change
- [ ] I have tested this change with different models/inputs — n/a, no models involved

## Documentation
- [x] I have updated the documentation accordingly
- [x] I have added docstrings to new functions/classes
- [x] I have updated the CHANGELOG.md

## Code Quality
- [x] I ran `ruff check .`, `ruff format --check .` (ruff 0.15.22) and `mypy` — all clean
- [ ] For Swift/OpenMedKit changes, I ran `make format-swift` and `make lint-swift` — n/a
- [x] I have performed a self-review of my own code
- [x] I have commented my code, particularly in hard-to-understand areas
- [x] My changes generate no new warnings

## Dependencies
- [x] I have not added any new dependencies

## Checklist
- [x] I have read the contributing guide, Code of Conduct, and maintainer guide
- [x] My commits have clear, descriptive messages
- [x] I have squashed/organized my commits appropriately

## Related Issues
Closes #3101
Related to #3195

## Screenshots/Examples

```markdown
| Locale | Status | Details |
| --- | --- | --- |
| `de` | removed | script `Latn`; identifiers: phone; surrogates: full |
| `fr` | changed | evidence digest changed |
| `hi` | improved | +identifiers: pan; surrogates: partial -> full |
| `pt-BR` | regressed | -identifiers: phone |
| `sw` | added | script `Latn`; identifiers: phone; surrogates: partial |
```
