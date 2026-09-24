# ruby/rdoc#1743 — Broken HTML when crossref matches `#<` without linking `<`

| Item | Value |
|---|---|
| Issue | https://github.com/ruby/rdoc/issues/1743 |
| Tier | 自由 |
| Labels | (none) |
| Status | 🚧 in progress — issue chosen, checking AI policy / cloning |
| Duplicate-PR check | `is:pr 1743` → 0 results; `is:pr crossref` → no open PR for this (2026-09-24) |

## Notes
- CROSSREF_REGEXP matches ` #<`; handle_regexp_CROSSREF returns the raw `<` which is emitted unescaped into HTML.
