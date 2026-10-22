## Description

Adds a refactor code action, "simplify variable initialization", for the rewrite proposed in #2098:

```zig
const foo = @as(T, something); // -> const foo: T = something;
const bar = T{};               // -> const bar: T = .{};
```

It is offered (kind `refactor`) for the innermost variable declaration that contains the requested position, when:

- the declaration has no type annotation, and
- its whole initialization expression is either `@as(T, value)` or a typed struct initialization `T{ ... }`.

The type annotation is inserted right after the name, so declarations with `align(...)`/`linksection(...)` keep those after the type (`pub const foo: u32 align(4) = 5;`). Array types are skipped (conservatively, including `[N]T{}`), since `[_]u8{}` is parsed as a struct init but `[_]u8` is not a valid type annotation. If the text that would be removed contains a comment (e.g. `@as(u32, // note` or `S // note\n{}`), no action is offered rather than silently dropping it. Other builtins, anonymous literals, already-annotated declarations and expressions where `@as` is only part of the initializer get no action.

The action is generated from `generateCodeActionsInRange` before the string-literal context check, next to the existing string-literal refactors. I kept it as a cursor-based `refactor` rather than a whole-file `source.*` action; happy to change the kind or title if you'd prefer something else.

Tests: new cases in `tests/lsp_features/code_actions.zig` cover `@as` (local/global, complex types, `align`), struct inits (empty, with fields, generic `Generic(u8){ ... }` spanning multiple lines), picking the innermost declaration, and the "no action" cases above (including the comment cases). Without the change in `src/features/code_actions.zig` the three positive tests fail; the `[_]u8{}` case also fails if the array-type guard is removed.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #2098

## Checklist

- [x] Tests pass locally with Zig 0.17.0 (`zig build test` → 586 passed, 11 skipped, 0 failed; `zig build test -Dtest-filter="simplify variable"` → 4 passed)
- [x] `zig fmt --check src tests build.zig` passes
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a
