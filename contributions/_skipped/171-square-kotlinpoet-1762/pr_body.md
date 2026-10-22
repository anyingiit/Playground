## Description

Fixes the badly indented output from `callThisConstructor()` / `callSuperConstructor()` when one of the delegated-constructor arguments renders to more than one line, e.g. a lambda (#1762). Previously the arguments were joined inline, so wrapped lines lined up with `: this(`, and the lambda body was indented less than the call. The closing `)` also ended up on its own line, because the argument's trailing newline was kept:

```kotlin
  public constructor(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx: String, yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy: String)
      : this(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx, yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy,
      xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx, yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy,
      thisIsAMethodThatUsesALambdaAndReturnsSomethingForTheConstructor {
    zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz()
  }
  )
```

With this change the call is emitted like a multiline parameter list: one argument per indented line, with a trailing comma.

```kotlin
  public constructor(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx: String, yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy: String) : this(
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx,
    yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy,
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx,
    yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy,
    thisIsAMethodThatUsesALambdaAndReturnsSomethingForTheConstructor {
      zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz()
    },
  )
```

Implementation details (`FunSpec.emitSignature` → new private `emitDelegateConstructorCall`):

- A trailing newline is first trimmed from each argument with the existing `trimTrailingNewLine()`, the same helper property initializers use.
- An argument counts as multiline when its rendered form (`CodeBlock.toString()`) contains `\n`. Rendering it means newlines that only appear inside nested blocks passed through `%L` or positional placeholders such as `%1L` are detected too.
- If no argument is multiline, the output is exactly as before: inline and wrappable (the existing `constructorDelegation` test is unchanged).
- Otherwise the arguments are joined with `,\n` inside `⇥`/`⇤` and a trailing comma is added. `: this(` stays attached to the signature with non-breaking spaces. Trailing commas in constructor delegation calls are valid since Kotlin 1.4.

One known limitation, which applies to property initializers as well: `trimTrailingNewLine()` doesn't look inside a nested `CodeBlock` argument. A nested block that itself ends in `\n` (e.g. `CodeBlock.of("%L", buildCodeBlock { beginControlFlow(...); endControlFlow() })`) therefore still leaves an empty line before its comma. I didn't touch that shared helper in this PR.

This PR is a fresh, independent implementation for #1762. The earlier PRs #2332 and #2354 were closed only because the CLA wasn't signed.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1762

## Checklist

- [x] Tests pass locally: `./gradlew :kotlinpoet:jvmTest :kotlinpoet:spotlessCheck` → BUILD SUCCESSFUL (1009 tests, 0 failures, 40 skipped). The two new `TypeSpecTest` tests (`constructorDelegationWithMultilineArgument`, `superConstructorDelegationWithNestedMultilineArgument`) fail without the `FunSpec` change and pass with it. JS/Wasm test tasks were not run locally.
- [x] Documentation is updated (if applicable): n/a.

<!-- Repository template (kept verbatim): -->
- [x] `docs/changelog.md` has been updated if applicable.
  - Changes not visible to library consumers, such as build script, documentation, or test code updates, don't need to
    be added to the changelog.
- [ ] [CLA](https://spreadsheets.google.com/spreadsheet/viewform?formkey=dDViT2xzUHAwRkI3X3k5Z0lQM091OGc6MQ&ndplr=1) signed.
