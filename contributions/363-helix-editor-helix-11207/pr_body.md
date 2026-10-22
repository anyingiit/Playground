## Description

Adds [Liquid](https://shopify.github.io/liquid/) (Shopify themes, Jekyll and other static site generators) using [hankthetank27/tree-sitter-liquid](https://github.com/hankthetank27/tree-sitter-liquid), the grammar nvim-treesitter uses:

- `languages.toml`: `liquid` language (`.liquid` files, `{% comment %}…{% endcomment %}` block comments, 2-space indent) and the grammar pinned to the current `main` (e45dbac).
- `runtime/queries/liquid/highlights.scm`: adapted from the grammar's own highlight query, mapped to Helix scopes: `{{ }}` / `{% %}` delimiters as `punctuation.special`, `if`/`unless`/`case`/`when` as `keyword.control.conditional`, `for`/`tablerow`/`break`/`continue` as `keyword.control.repeat`, `include`/`render`/`section`/`layout` as `keyword.control.import`, filters as `function`, `{% doc %}` blocks as documentation comments with `@param` types/names highlighted, and the body of `{% raw %}` as `markup.raw` (the grammar's `raw_content` node is zero-width, so the whole `raw_statement` is captured and the tag keywords inside it win as inner nodes).
- `runtime/queries/liquid/injections.scm`: the grammar's injections, unchanged: the template text as combined HTML, `{% schema %}` as JSON, `{% style %}`/`{% stylesheet %}` as CSS, `{% javascript %}` as JavaScript and front matter as YAML.
- A highlight fixture in `tests/query/highlights/liquid/` and the regenerated `lang-support.md` row.

No language server is configured by default; Shopify's theme language server needs the Shopify CLI (`shopify theme language-server`) and can be added by users.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all.

## Related issue

Closes #11207

## Checklist

- [x] `hx --grammar fetch` / `hx --grammar build` fetch and build the grammar at the pinned rev
- [x] `cargo xtask query-check liquid` → `Query check succeeded`
- [x] `cargo xtask highlight-check liquid` → `Highlight check succeeded (14 assertions)` (all 14 fail without `highlights.scm`)
- [x] Checked `cargo xtask highlight-check --dump liquid` on sample templates covering `{% liquid %}`, whitespace-control delimiters, `case/when`, ranges, `{% doc %}`, inline `{% # %}` comments, `{% schema %}`, `{% style %}` and `{% javascript %}` (the last three get JSON/CSS/JS highlighting through the injections)
- [x] `cargo xtask docgen`
