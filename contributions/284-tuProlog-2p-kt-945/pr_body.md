Fixes #945.

`JvmTheoryDeobjectifier` and `JsTheoryDeobjectifier` cast every deobjectified term to `Clause` without checking it. When a JSON/YAML theory contains a well-formed term that is not a clause (a number, a variable, or a struct like `foo(X)`), deserialization fails with a raw `ClassCastException` instead of the `DeobjectificationException` documented on `Deobjectifier.deobjectify` and `Deserializer.deserialize`.

### Changes

- Both deobjectifiers now use `it as? Clause ?: throw DeobjectificationException(it)`, as suggested in the issue. The exception carries the offending deobjectified term (e.g. `Error while deobjectifying 1`). The raw input element is no longer at hand at that point, and the term is also easier to read than the parsed map.
- `TestTheoryDeserialization` (commonTest, so it runs on JVM and JS) gets two tests that deserialize a theory with a non-clause element (`1`, a variable, `foo(X)`) from JSON and from YAML and assert `DeobjectificationException`.

### Testing

- `./gradlew :serialize-theory:jvmTest`: the new tests fail with `ClassCastException` without the fix and pass with it.
- `./gradlew :serialize-theory:ktlintCheck :serialize-theory:detekt :serialize-theory:jsTestClasses` pass. I could not run `jsTest` locally (yarn could not be downloaded in my environment), so the JS side relies on CI; the change there is the same one-liner as on the JVM.

### Motivation and disclosure

I picked this up because it is a small, well-specified `good first issue` with a clear expected behaviour. I wrote it with help from an AI coding assistant (Claude Code), reviewed the change myself, and ran the tests listed above.
