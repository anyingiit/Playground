## Summary

`sysknife history --since <datetime>` (and the MCP `sysknife_history` tool) converted the datetime to a whole-hour count with `(now - epoch) / 3600`, and the daemon then filtered on `julianday('now', '-N hours')`. A cutoff 30 minutes ago became `since_hours = 0` and returned nothing; 90 minutes ago became `1` and dropped the rows between 60 and 90 minutes old.

This PR sends the exact cutoff instead:

- **CLI**: `since_to_hours` is replaced by `since_to_cutoff`, which normalises `--since` (RFC 3339 with `Z`/offset, or a bare `YYYY-MM-DD` = midnight UTC) to an RFC 3339 UTC timestamp. Both callers, `run_history` (`ListJobHistory` params) and the MCP tool (`query_history` request), send it as `since`.
- **Daemon**: the store's history methods take `Option<HistorySince>`, which is either `Hours(n)` (the planner's `query_job_history` `since_hours`, same semantics as before) or `Cutoff(DateTime<Utc>)`. `ListJobHistory` and `query_history` both accept `since`; giving `since` and `since_hours` together is rejected as a `validation_failure`.
- **UTC normalisation**: SQLite compares via `julianday(created_at) >= julianday(?)`, so `...Z` rows, explicit-offset rows and legacy `datetime('now')` rows are all compared in UTC. Postgres uses `created_at::timestamptz >= $n::timestamptz`.

Compatibility note: a new CLI talking to an older daemon would send `since`, which the old daemon ignores, so it gets unfiltered history instead of an empty list. Nothing public is removed. `since_to_hours` was a `pub fn` in the binary crate's `runner` module, and its only callers were in this crate.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related Issue

Closes #567

## Validation

- [x] Tests added or updated
  - Regression tests matching the issue's 20-minute and 75-minute entries:
    - `dispatcher::tests::query_history_since_keeps_sub_hour_precision` (cutoffs 30/90/10 min, expect 1/2/0 rows)
    - `dispatcher::tests::list_job_history_since_keeps_sub_hour_precision`
    - `transactions::tests::list_history_filters_by_exact_cutoff_below_one_hour`
    - `transactions::tests::list_history_cutoff_normalises_offsets_and_legacy_rows` (`+02:00` and `datetime('now')`-shaped rows)
    - `dispatcher::tests::resolve_history_since_parses_and_rejects_ambiguity`
    - `runner` tests: `since_to_cutoff_*` (they replace the 5 `since_to_hours_*` tests)
    - `tests/postgres_store.rs` exercises a `Cutoff` both ways. I could not run it because no Postgres was available (5 ignored).
  - Red before the fix: with only the dispatcher tests applied on `main`, both failed. For example, a cutoff 30 minutes ago returned 2 entries instead of 1, and a cutoff 10 minutes ago listed 2 transactions instead of none.
  - Net change: +6 Rust tests (daemon +5, CLI +1).
- [x] `cargo fmt --all -- --check`: clean
- [x] `cargo clippy -p sysknife-daemon -p sysknife-cli --all-targets --locked -- -D warnings`: clean
- [x] `cargo test -p sysknife-cli --locked`: all pass (unit 295, cli_smoke 22 + 1 ignored, config_file_honoured 2, doctor_output 4, mcp_stdio 3)
- [x] `cargo test -p sysknife-daemon --lib --locked`: 923 passed, 5 failed. The 5 failures are the `transactions::tests::*watermark*` tests. They need one process per test (`OnceLock` test sink, as `audit_watermark.rs` notes), and each one passes when run alone with `--exact`. I did not have `cargo-nextest` installed.
- [x] `cargo test -p sysknife-daemon --test '*' --locked --no-fail-fast`: everything passed except `execute_spec::a_sigterm_ignoring_child_is_escalated_to_sigkill_within_the_grace`. That test fails the same way on unmodified `main` in my sandbox, so it is environmental.
- [x] `python3 scripts/check_evidence_claims.py`: "Published figures match the evidence artifacts."
- [ ] Not run: `cargo nextest run --workspace`, `scripts/ci-local.sh`, and the GUI crate (no Tauri system libraries here). Following CONTRIBUTING's fallback, I left `tests/evidence/workspace-tests.json` and the three prose files untouched. The suite figure moves by +6.
- [x] Documentation updated if behavior changed: n/a. The user-facing `--since` syntax is unchanged. The CHANGELOG entry is left to the maintainer, as with recent `docs(changelog): log #…` commits.
- [x] Security impact considered: the cutoff is parsed with `chrono` and bound as a SQL parameter, never interpolated.
- [x] Trust boundary preserved (daemon remains the only privileged executor)
- [ ] CI passes: pending

## Notes for Reviewers

`HistorySince::Cutoff` is inclusive (`>=`), like `audit export --since`. `Hours` keeps the existing strict `>`.
