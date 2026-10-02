## Description

`PrimitiveDataFrameColumn<T>.ElementwiseEquals` / `ElementwiseNotEquals` compared the raw buffer values and ignored the validity (null) bitmap. A null element is stored as `default(T)`, so `0 == null` returned `true` and `0 != null` returned `false`, as shown by the test in #6820.

All typed/untyped overloads (column vs column of any primitive type, column vs scalar, with or without type conversion) end up in `PrimitiveColumnContainer<T>.HandleOperation(ComparisonOperation, ...)`, so the fix is there: after the vectorized comparison, a small post-processing step (`ApplyNullEqualitySemantics`) rewrites the result for rows where at least one operand is null, using validity only:

- `null == null` -> `true`, `null == value` / `value == null` -> `false`
- `ElementwiseNotEquals` is the exact inverse

This matches the existing semantics elsewhere in the DataFrame API: `ElementwiseEquals(null)` already means `ElementwiseIsNull()`, and `StringDataFrameColumn` treats two nulls as equal. The step returns immediately when neither side has nulls, so the fast path for null-free columns is unchanged, and only runs for Equals/NotEquals.

I intentionally did not change the ordering comparisons (`>`, `>=`, `<`, `<=`): what they should return for nulls (false? null?) is a semantic decision I'd rather leave to you. Happy to extend the PR if you tell me the preferred behavior.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Fixes #6820

## Checklist

- [x] There's a descriptive title that will make sense to other developers some time from now.
- [x] There's associated issues: Fixes #6820
- [x] Your change description explains what the change does, why you chose your approach, and anything else that reviewers should know.
- [x] You have included any necessary tests in the same PR: `TestElementwiseEqualsWithNulls` (the scenario from the issue plus null/null and NotEquals), `TestElementwiseEqualsWithNullsAndDifferentColumnTypes` (int vs double), `TestElementwiseEqualsScalarWithNulls` (column vs scalar, same and converted type) in `PrimitiveDataFrameColumnTests.cs`.

Tested locally on Linux (net8.0): `dotnet test test/Microsoft.Data.Analysis.Tests` -> 491 passed, 0 failed; the 3 new tests fail on `main` without the change; `dotnet format --verify-no-changes` on the changed files passes.
