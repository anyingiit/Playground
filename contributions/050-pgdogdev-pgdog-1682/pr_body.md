## Description

`try_multi_set()` passed every `VariableSetStmt` except `SET TRANSACTION` (`VAR_SET_MULTI`) to `parse_set_param()`, and that function panics on any kind other than `SET x TO value`, `SET x TO DEFAULT` and `RESET x`. A multi-statement query containing `RESET ALL` or `SET x FROM CURRENT` therefore panicked the client's task (`parse_set_param called on invalid kind 5`). The Npgsql connection-reset sequence (`SET SESSION AUTHORIZATION DEFAULT;RESET ALL;CLOSE ALL;...`) is one example. A single `SET x FROM CURRENT` hit the same panic through `set()`.

Fix: a small `is_set_param()` helper (`VAR_SET_VALUE | VAR_SET_DEFAULT | VAR_RESET`) now decides which statements count as trackable SET params:

- In `try_multi_set()`, `RESET ALL` and `SET ... FROM CURRENT` are treated as "other" statements. The existing mixed-SET logic then handles them: `SET a TO 1; RESET ALL` is split (and the split `RESET ALL` becomes `Command::ResetAll` as before), and the Npgsql reset sequence returns `MultiStatementSafety` in transaction mode instead of panicking. Session mode already forwards it verbatim.
- In `set()`, a standalone `SET ... FROM CURRENT` is forwarded to the server like `SET TRANSACTION`.

Regression tests were added to `query/test/test_set.rs`: `test_multi_statement_reset_all` and `test_set_from_current`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1682

## Checklist

- [x] Tests pass locally: `cargo test -p pgdog --bin pgdog -- query::test::test_set::` gives 18 passed. Both new tests fail with the issue's panic without the fix and pass with it. `cargo test -p pgdog --bin pgdog -- router::parser` gives 760 passed. The remaining failures are shared-global-state tests that pass when run in isolation, as nextest runs them (`test-threads = 1`, one process per test), plus one test that needs a running Postgres.
- [x] `cargo fmt --all -- --check` and `cargo clippy -p pgdog --bin pgdog` are clean.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, small bug fix
- [ ] Documentation is updated (if applicable) — n/a
