## Description

In Ruby, `]a` / `[a` (and `ma`/`mia` on arguments) only work on parameter lists (`def`, block and lambda parameters). Arguments of a method call are not captured, so in the example from #5817 `]a` jumps over the arguments of `super(...)` entirely, and in `foo(bar, baz)` it does nothing.

This adds `argument_list` to `runtime/queries/ruby/textobjects.scm` using the same pattern the Python and Rust queries use for their argument lists:

```scheme
(argument_list
  ((_) @parameter.inside . ","? @parameter.around) @parameter.around)
```

tree-sitter-ruby uses `argument_list` both for parenthesized calls (`foo(bar, baz)`, `super(a, **opts)`) and for command calls without parentheses (`puts bar, baz`), so both are covered.

The existing parameter-list captures are left as they are.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all.

## Related issue

Closes #5817

## Checklist

- [x] Added an integration test (`tree_sitter_motions_work_across_ruby_call_arguments` in `helix-term/tests/test/movement.rs`): `]a` from the start of `foo(bar, baz)` selects `bar,`, again selects `baz`, and the same works for `puts bar, baz`. With the ruby grammar built, `cargo integration-test -- ruby_call_arguments` fails without the query change (the cursor doesn't move) and passes with it.
- [x] `cargo xtask query-check ruby` → `Query check succeeded`
