## Description

Fixes #5207

Changes proposed in this pull request:
- Add a **Hidden characters facet** entry to *Facet → Customized facets* (right after "Unicode char-code facet"). It is a plain list facet whose expression lists, for each cell, the escape codes (`\u00A0`, `\u200B`, `\uFEFF`, …) of the invisible characters it contains. Rows without hidden characters are not listed, so selecting a choice directly shows the affected rows, ready to be cleaned with a GREL `replace()`.
- The character set follows the invisible characters that VS Code highlights ([hediet/vscode-unicode-data](https://github.com/hediet/vscode-unicode-data), as suggested in the issue), plus the C0/C1 control characters. Tab, line feed and the regular space are deliberately left out so that ordinary multi-word or multi-line cells do not flood the facet.
- No backend change: the expression is `forEach(value.find(/[…]/), c, c.escape('javascript'))`, using existing GREL functions, so users can see and tweak it via the facet's "change" link. `escape('javascript')` produces the `\uXXXX` form (characters outside the BMP, e.g. tag characters, show up as their surrogate pair).
- Add a Cypress test in the (previously empty) `customized-facets` folder, and the English UI string (other languages go through Weblate).

Design decisions reviewers may want to weigh in on: the menu location / label, and whether CR (U+000D, included, as VS Code does) and the C0/C1 controls should be part of the set. The `showHiddenChars()` / `removeHiddenChars()` GREL functions mentioned in the issue are left for a follow-up.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #5207

## Checklist

- [x] Tests pass locally — `CYPRESS_SPECS=cypress/e2e/project/grid/column/facet/customized-facets/hidden-chars-facet.cy.js ./refine e2e_tests`: 1 passing (fails without the change: the menu entry does not exist). All `cypress/e2e/project/grid/column/facet/` specs: 29 passing, 1 failing (`facets.cy.js` "Test collapsing facet panels"), which fails identically on `master` in my environment.
- [x] Lint — `yarn lint` in `main/tests/cypress` (prettier + eslint): 0 errors (only pre-existing warnings in other files). No Java files changed.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (OpenRefine has no changelog file in the repo).
- [ ] Documentation is updated (if applicable) — the user manual lives in OpenRefine/openrefine.org; happy to add an entry to the "Customized facets" section there if this is accepted.
- [x] Screenshot (UI change) — facet on a small test column, with the `\u00A0` choice selected:

  <!-- attach screenshot-hidden-chars-facet.png here -->
