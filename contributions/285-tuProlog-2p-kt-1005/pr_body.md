Fixes #1005.

`ceiling/1` turned its result into a `Long` via `ceil(real.value.toDouble()).toLong()`, which saturates at `Long.MAX_VALUE` and also loses precision in the `Double` round-trip. So `X is ceiling(1.0e30)` gave `9223372036854775807`, while `floor/1`, `round/1` and `truncate/1` already return big integers.

### Changes

- `Ceiling.mathFunction(real, ...)` now uses `Numeric.of(real.value.setScale(0, RoundingMode.CEILING).toBigInteger())`, the same approach as `Floor.kt` and the fix suggested in the issue. Integer inputs are still returned unchanged.
- Added `testIsCeilingOfLargeReal` to the shared `TestIs` suite in `test-solve` (wired into `TestPrologIs` and `TestProblogIs`). It checks `X is ceiling(1.0e30)` and `X is ceiling(-1.0e30)`, plus `ceiling(2.1)` and `ceiling(-0.5)` to cover rounding of small values.

### Testing

- `./gradlew :solve-prolog:jvmTest --tests '*TestPrologIs*'`: without the fix the new test fails with `X_1=9223372036854775807`. With the fix it passes. `:solve-problog:jvmTest --tests '*TestProblogIs*'` passes too.
- `ktlintCheck` (solve, test-solve, solve-prolog, solve-problog) and `detekt` (solve, test-solve) pass. I couldn't run the JS tests locally (yarn could not be downloaded in my environment).

### Motivation and disclosure

This is a confirmed `good first issue` with a clear fix. I wrote it with help from an AI coding assistant (Claude Code), reviewed the change myself, and ran the tests listed above.
