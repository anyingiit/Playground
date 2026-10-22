<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KU5CcqhtizgR6Af7udenHiG)_

## Description

With the `ternary` strategy, the autofix of `jsx-no-leaked-render` drops the parentheses around the right side, so the common multi-line pattern

```jsx
{item.validateResult && item.validateResult.error && (
  <ErrorWrapper>
    <Text>{item.validateResult.error.message}</Text>
  </ErrorWrapper>
)}
```

is fixed to

```jsx
{item.validateResult && item.validateResult.error ? <ErrorWrapper>
    <Text>{item.validateResult.error.message}</Text>
  </ErrorWrapper> : null}
```

This still reproduces on master. #3623 fixed the same thing for the `coerce` strategy, but the ternary branch builds its replacement from `getText(rightNode)`, which doesn't include the parentheses.

The fix: in the ternary branch, if the right side is parenthesized, use the source text from its opening paren to its closing paren (so the line breaks inside are kept as written). The output is now:

```jsx
{item.validateResult && item.validateResult.error ? (
  <ErrorWrapper>
    <Text>{item.validateResult.error.message}</Text>
  </ErrorWrapper>
) : null}
```

A parenthesized non-JSX right side is kept as well, e.g. `count && (a ? b : c)` becomes `count ? (a ? b : c) : null` instead of `count ? a ? b : c : null`. Unparenthesized right sides are unchanged.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #3357

## Checklist

- [x] Tests: two new invalid cases (ternary strategy) in `tests/lib/rules/jsx-no-leaked-render.js`. Without the fix they fail (6 failures across the parsers); with it the rule's tests pass (249). Full mocha run over `tests/lib`, `tests/util` and `tests/index.js`: 18298 passing. `eslint .`, `tsc` and `npm run lint:docs` pass.
- [x] `CHANGELOG.md` updated under Unreleased / Fixed
- [ ] Documentation — n/a (behaviour of the autofix only)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012YkMb3Q6rZmThSA5aAF7CA
