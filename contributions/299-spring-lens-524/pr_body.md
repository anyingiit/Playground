Closes #524 (part of #506).

Adds `IsolationLevel` to `spring-lens-core` in `com.sdlcpro.springlens.model.transaction`:

- `DEFAULT(-1)`, `READ_UNCOMMITTED(1)`, `READ_COMMITTED(2)`, `REPEATABLE_READ(4)` and `SERIALIZABLE(8)`, the values Spring's `TransactionDefinition` and JDBC's `Connection` use.
- `value()` returns the integer, and `from(int)` looks it up in a cached `VALUES` array. Values outside 0–8, and the unmapped ones in between (0, 3, 5, 6, 7), fall back to `DEFAULT`. The skeleton in the issue left the lookup loop as a comment; this fills it in, following `BeanRole`.
- JavaDoc on the enum, each constant and both public methods.

`IsolationLevelTest` covers every mapping in both directions, the fallback for unsupported values (including `Integer.MIN_VALUE`/`MAX_VALUE`, 0, 3 and 9), and checks the values against the `java.sql.Connection` constants. With the lookup loop removed, as in the skeleton, 4 of its 16 cases fail. `mvn -pl spring-lens-core -am test -Djacoco.skip=true` passes (150 tests).

I prepared this with help from an AI coding assistant (Claude Code) and reviewed the change myself.
