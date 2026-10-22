Closes #526 (part of #506).

Adds `TransactionStatus` to `spring-lens-core` in `com.sdlcpro.springlens.model.transaction`, as described in the issue:

- `COMMITTED("Committed")`, `ROLLED_BACK("Rolled Back")` and `ERRORED("Errored")`
- a final `label` field with a public `getLabel()` getter
- JavaDoc on the enum, each constant and `getLabel()`

`TransactionStatusTest` checks the constants and their labels. `mvn -pl spring-lens-core -am test` passes (136 tests).

I prepared this with help from an AI coding assistant (Claude Code) and reviewed the change myself.
