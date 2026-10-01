## Description

Adds PHP support to the diff viewer, as proposed in #156:

- **Syntax highlighting:** `.php` files are registered in `src/command/diff/highlight/config.rs` using `tree_sitter_php::LANGUAGE_PHP` (the variant that handles `<?php ... ?>` tags mixed with inline text) and the crate's bundled `HIGHLIGHTS_QUERY`, following the same pattern as Elixir and Java.
- **Context lines:** adds a `PHP_CONTEXT_QUERY` in `src/command/diff/context.rs` (namespaces, classes, interfaces, traits, enums, functions, methods, closures/arrow functions, loops, `if`/`switch`/`match`/`try`), so sticky context shows the enclosing PHP scopes.
- **Dependency:** `tree-sitter-php = "0.23"` (resolves to 0.23.11, grammar ABI 14, compatible with the `tree-sitter = "0.24"` already in use; same `0.23` line as most other grammars here). `Cargo.lock` only gains the new package entry — no other dependencies moved.
- **Tests:** `test_php_highlighting` and a `"php"` assertion in `test_all_configs_load` (highlight), plus `test_php_method_context` (context lines). All of them fail without the change and pass with it.

About the `fix(html): ...` scope mentioned in the issue: `lumen draft` leaves the scope choice to the model, which reads the diff, and this PR doesn't change the prompt. I'd expect `.php` to be read as PHP in most cases already, so I haven't tried to force a scope.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #156

## Checklist

- [x] Tests pass locally — `cargo test --locked`: 136 passed, 1 failed (`vcs::git::tests::test_get_merge_base_returns_ancestor`, which fails the same way on `main` in my environment because the test repo's default branch isn't `main`: "reference 'refs/heads/main' not found"); the new PHP tests fail before the change and pass after it. `cargo clippy --all-targets --locked`: no new warnings (27 before and after). `cargo fmt --check`: no new diffs in the changed code (`main` already has some unrelated ones).
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, the README doesn't list the supported languages
