## Description

Adds the [Uiua](https://www.uiua.org/) array programming language (`.ua`), as requested in #7949.

- `lib/linguist/languages.yml`: new `Uiua` entry (`type: programming`, `.ua`, `tm_scope: source.uiua`, `ace_mode: text`); `language_id` generated with `script/update-ids`.
- Grammar: [uiua-lang/uiua-vscode](https://github.com/uiua-lang/uiua-vscode) (official Uiua VS Code extension, MIT) added as a submodule; `grammars.yml`, `.gitmodules`, `vendor/README.md` and the cached license record (`vendor/licenses/git_submodule/uiua-vscode.dep.yml`) updated accordingly.
- Samples: three real-world programs from the official [uiua-lang/uiua](https://github.com/uiua-lang/uiua/tree/14f6dcdeff83e697c169c3a87a4f1685d36bb238/examples) repository.

`.ua` is not used by any other language in `languages.yml`, so no heuristic is needed.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #7949

## Checklist:

- [x] **I am adding a new language.**
  - [x] The extension of the new language is used in hundreds of repositories on GitHub.com.
    - Search results for each extension:
      - https://github.com/search?type=code&q=NOT+is%3Afork+path%3A*.ua+%E2%86%90
  - [x] I have included a real-world usage sample for all extensions added in this PR:
    - Sample source(s):
      - https://github.com/uiua-lang/uiua/blob/14f6dcdeff83e697c169c3a87a4f1685d36bb238/examples/n-body.ua
      - https://github.com/uiua-lang/uiua/blob/14f6dcdeff83e697c169c3a87a4f1685d36bb238/examples/markov.ua
      - https://github.com/uiua-lang/uiua/blob/14f6dcdeff83e697c169c3a87a4f1685d36bb238/examples/http_server.ua
    - Sample license(s): MIT (https://github.com/uiua-lang/uiua/blob/main/license)
  - [x] I have included a syntax highlighting grammar: https://github.com/uiua-lang/uiua-vscode
  - [x] I have added a color
    - Hex value: `#c87dff`
    - Rationale: picked as a purple tone (not an official brand color); happy to change it to whatever the Uiua community prefers.
  - [ ] I have updated the heuristics to distinguish my language from others using the same extension. — n/a, `.ua` is not used by any other language.

Tests run locally (Ruby 3.3.6):
- `bundle exec rake samples && bundle exec rake test` → `2051 runs, 41087 assertions, 0 failures, 14 errors, 1 skips`. The 14 errors are all in `TestRuggedRepository` (`Rugged::OdbError: object not found`) because my checkout is shallow; they fail identically on the base commit.
- An ad-hoc check that `Language.find_by_extension("foo.ua") == [Language["Uiua"]]` and that the upstream example files are classified as Uiua: fails before this change, passes after.
- `script/check-regex-compatibility` → `Checked 607 regexes ... (0 allowlisted failures)`.
- Grammar validated with the grammar compiler (`grammar-compiler add vendor/grammars/uiua-vscode` → `OK! ... new scope: source.uiua`); `licensed status` passes for `uiua-vscode`.
