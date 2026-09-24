# pmd/pmd#7100 — [groovy] CPD fails on GStrings that end in an interpolated variable

| Item | Value |
|---|---|
| Issue | https://github.com/pmd/pmd/issues/7100 |
| Tier | 高活跃高Star |
| Labels | a:bug |
| Status | 🚧 in progress — audit done, building |
| Duplicate-PR check | open PR list 2026-09-24: none references #7100 |

Notes: reporter suggests using `GroovyLangLexer` (subclass used by the Groovy compiler) instead of `GroovyLexer` in `GroovyCpdLexer`. No AI policy found in CONTRIBUTING/.github/devdocs.
