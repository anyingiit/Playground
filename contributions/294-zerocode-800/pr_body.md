# Allow a minimal echo step without url and assertions

## Fixed Which Issue?
- [x] Which issue or ticket was(will be) fixed by this PR? (capture the issue link here)
  https://github.com/authorjapps/zerocode/issues/800

## Motivation and Context

A step with an empty `url` and `operation` makes no call and returns its `request` as its response, which is handy for keeping values for later steps. Until now it only worked if `url`, `operation` and `assertions` were all written out, even when empty. This lets the step be just a `name` and a `request`:

```json
{
    "name": "store_ids",
    "request": {
        "orderId": 1001
    }
}
```

Two changes in `ZeroCodeMultiStepsScenarioRunnerImpl`:

- **`url` omitted:** `executeApi` treats a missing `url` as empty. Before, resolving the null url threw a `NullPointerException`.
- **`assertions` omitted:** `compareStepResults` passes a step without comparing anything when it makes no call (`ApiType.NONE`) and has no `assertions`, `verify` or `validators`. Before, the missing assertions were compared as `null` against the echoed request and the step failed.

Everything else behaves as before:

- Steps that already use `"url": ""`, `"operation": ""` and `"assertions": {}` are unchanged.
- Steps that make a real call (HTTP, Java, Kafka) still fail when `assertions` is omitted. I left that open question from the issue alone.
- One case does change: a step with a `url` but no `operation` was already an echo step (no call is made). If it also has no `assertions`, it now passes instead of failing.

The doc site update is for a separate PR, as the issue says.

## Checklist:

* [x] 1. New Unit tests were added
  * `ZeroCodeMultiStepsScenarioRunner_EchoStepTest` runs `e2e/EchoStepShortForm` with two scenarios under `integration_test_files/echo_step/`:
    * The short-form scenario stores values in a step with only `name` and `request`, reads them back in a step without `url`/`operation`, and in one with the empty values. It passes.
    * The Java call scenario (`MimeTypeConverter.jsonBlockToJson`) with no `assertions` still fails.
  * Without the change, the short-form scenario fails with the `NullPointerException`.

* [ ] 2. Integration tests were added
  * [ ] 2.1 Covered in existing Integration tests

* [x] 3. Test names are meaningful

* [x] 4. PR doesn't break any of the earlier features for end users
  * `mvn -pl core test` runs 457 tests. The only failures are `DbSqlExecutorScenarioPostgresTest`, which needs a running Postgres, and `KafkaFileRecordHelperTest.test_dodgyFile`, and both fail the same way on `master` in my environment.

* [ ] 5. PR doesn't break the HTML report features directly
  * Not checked by opening the HTML report. The echo step's report entry now has an empty url instead of none.

* [x] 6. PR doesn't break any HTML report features indirectly
  * [x] 6.1 I have not added or amended any dependencies in this PR

* [ ] 7. Branch build passed in CI

* [x] 8. No 'package.*' in the imports

* [x] 9. Relevant Documentation page added or updated: not in this PR, per the issue, the doc site goes in a separate PR.

* [x] 10.1 Not applicable. The changes did not affect HTTP automation flow
* [x] 11.1 Not applicable. The changes did not affect Kafka automation flow

## Disclosure

I prepared this with help from an AI coding assistant (Claude Code), reviewed the change myself, and ran the tests above.
