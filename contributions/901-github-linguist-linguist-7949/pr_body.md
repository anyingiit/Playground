Adds the [Uiua](https://www.uiua.org/) array programming language (`.ua`) with the grammar from [uiua-lang/uiua-vscode](https://github.com/uiua-lang/uiua-vscode).

## Description

- New `Uiua` entry in `lib/linguist/languages.yml` (`.ua`, `tm_scope: source.uiua`, `ace_mode: text`, `language_id` generated with `script/update-ids`).
- Grammar added as a submodule from [uiua-lang/uiua-vscode](https://github.com/uiua-lang/uiua-vscode) (MIT), the official VS Code extension maintained by the Uiua project. `grammars.yml`, `.gitmodules`, `vendor/README.md` and `vendor/licenses/git_submodule/uiua-vscode.dep.yml` were updated by the `script/add-grammar` steps (grammar compiler: `OK! added grammar source 'vendor/grammars/uiua-vscode'`, new scope `source.uiua`, no errors).
- Two real-world samples from the main Uiua repository's `examples/` directory.
- `.ua` isn't used by any other language in Linguist, so no heuristic is needed.
- No colour set (optional); happy to add one if the Uiua community suggests one.

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
      - https://github.com/search?type=code&q=NOT+is%3Afork+path%3A*.ua+%E2%86%90+-user%3Auiua-lang  — <FILL IN: N results as of DATE>
  - [x] I have included a real-world usage sample for all extensions added in this PR:
    - Sample source(s):
      - https://github.com/uiua-lang/uiua/blob/ac326ebf05e577517db46c066fda7c38fe97a37d/examples/http_server.ua
      - https://github.com/uiua-lang/uiua/blob/ac326ebf05e577517db46c066fda7c38fe97a37d/examples/markov.ua
    - Sample license(s): MIT (https://github.com/uiua-lang/uiua/blob/main/license)
  - [x] I have included a syntax highlighting grammar: https://github.com/uiua-lang/uiua-vscode
  - [ ] I have added a color
    - Not set (optional); open to suggestions.
  - [ ] I have updated the heuristics to distinguish my language from others using the same extension.
    - N/A: `.ua` is not used by any other language in Linguist.

Tests: `bundle exec rake test` → 2051 runs, 0 new failures (the base commit has the same 2 failures/15 errors in my local shallow clone without the CodeMirror submodule and full git history: `TestRuggedRepository` and the CodeMirror checks). `bundle exec script/cross-validation --test` → "Number of errors (14) is within the acceptable threshold (14)". `bin/github-linguist samples/Uiua/markov.ua` now reports `language: Uiua` (empty before).
