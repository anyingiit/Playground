## Description

Gherkin highlighting landed in #11083, but `.feature` files still have no language server, which is the remaining half of #3115. This adds the official Cucumber language server ([`@cucumber/language-server`](https://github.com/cucumber/language-server), the one behind the Cucumber VS Code extension) as the default server for `gherkin`:

```toml
[language-server.cucumber-language-server]
command = "cucumber-language-server"
args = ["--stdio"]
```

plus `language-servers = [ "cucumber-language-server" ]` on the `gherkin` language, and the regenerated `book/src/generated/lang-support.md` row (`cargo xtask docgen`). The command and `--stdio` argument match the package's `bin` entry and nvim-lspconfig's `cucumber_language_server`.

No `config` is needed: the server asks for the `cucumber` section via `workspace/configuration`; Helix answers `null` when no config is set, and the server then uses its built-in defaults for feature and glue globs (Cucumber-JVM, Cucumber-JS, Behat, Behave, pytest-bdd, cucumber-rs, Cucumber-Ruby, SpecFlow, Godog layouts). Users with a different layout can set `[language-server.cucumber-language-server.config.cucumber]` `features = [...]` / `glue = [...]`.

Install: `npm install -g @cucumber/language-server`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #3115

## Checklist

- [x] `cargo xtask docgen` regenerated `lang-support.md` (only the gherkin row changes)
- [x] `hx --health gherkin` with the server on `PATH` → `✓ cucumber-language-server`
- [x] Ran `cucumber-language-server --stdio` (1.7.0, `npm install -g`) against a small project (`features/greeting.feature` + `features/step_definitions/steps.ts`) with an LSP client that sends Helix's `initialize`/`workspace/configuration` responses (the latter answered with `[null]`, as Helix does without a `config`): the server picked up its default globs, found the 2 step definitions, and, once indexing finished, reported diagnostics only for the step that has no matching definition
