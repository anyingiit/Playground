<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KU5CcqhtizgR6Af7udenHiG)_

## Description

When the closing tag shares a line with the content, the `jsx-closing-tag-location` autofix inserts a newline before it. If the content ends with spaces, those spaces are rendered before the fix, but JSX drops trailing whitespace once a newline follows, so the fix changes the output:

```jsx
<div>
  foo </div>        // renders "foo "
```

is fixed to

```jsx
<div>
  foo
</div>            // renders "foo"
```

(The issue title names `jsx-closing-bracket-location`, but the example is about the closing tag, and it is `jsx-closing-tag-location` whose fix does this. It still reproduces on master.)

As agreed in #1501, the autofix shouldn't change what is rendered. With this change, when the last child is text ending in spaces or tabs, the fixer moves those characters into an expression container (`{' '}`) before the newline (tabs are kept as written):

```jsx
<div>
  foo{' '}
</div>
```

You suggested `{'foo '}` in the issue; `foo{' '}` changes less of the user's text, but I'm happy to switch. `{' '}` is the same form `jsx-one-expression-per-line` uses to keep significant spaces. Everything else about the fix is unchanged: content without trailing spaces gets only the newline, and the `matchIndent` / `alignWithOpening` re-indent path isn't touched.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #1501

## Checklist

- [x] Tests: two new invalid cases in `tests/lib/rules/jsx-closing-tag-location.js` (text with a trailing space, and an expression followed by a space). Without the fix they fail (6 failures across the parsers); with it the rule's tests pass (58). Full mocha run over `tests/lib`, `tests/util` and `tests/index.js`: 18298 passing. `eslint .`, `tsc` and `npm run lint:docs` pass.
- [x] `CHANGELOG.md` updated under Unreleased / Fixed
- [ ] Documentation — n/a (autofix behaviour only)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012YkMb3Q6rZmThSA5aAF7CA
