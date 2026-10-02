## Description

Adds a `trace_ignore_status_codes` option, following the `traceIgnoreStatusCodes` option from the [Traces spec](https://develop.sentry.dev/sdk/telemetry/traces/). `sentry-python` uses the same option name.

```php
\Sentry\init([
    'traces_sample_rate' => 1.0,
    // single status codes and inclusive [min, max] ranges
    'trace_ignore_status_codes' => [404, [301, 303], [305, 399]],
]);
```

How it works:

- When a sampled `Transaction` finishes, it reads its `http.response.status_code` data (an int or a numeric string). If the value matches an entry in the option, the transaction is marked as not sampled and is not sent, and an `info` message naming the matched status code is written to the SDK logger.
- Transactions without `http.response.status_code` data (CLI commands, queue jobs and so on) are never affected, so in practice the option only applies to incoming-request transactions. sentry-laravel's tracing middleware already sets this data key. Integrations that only call `setHttpStatus()` (for example sentry-symfony) would need to set it as well. I left `Span::setHttpStatus()` unchanged so this PR doesn't change any existing payloads.
- The option accepts ints and `[min, max]` pairs of ints (`min <= max`). Any other value is rejected by the options resolver like other invalid options: a debug message is logged and the default is used.
- The default is `[]`, so nothing changes for existing users. The spec suggests `[[301, 303], [305, 399], [401, 404]]` as the default for the next major release.
- `Options` gets a getter and a setter, the `init()` array-shape docs in `src/functions.php` are updated, and `OptionsTest::optionsDataProvider()` has a new case.
- This SDK has no client reports, so no `event_processor` discard is recorded.

README and CHANGELOG are untouched, per AGENTS.md. A follow-up in `sentry-docs` will be needed to document the new option.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

* resolves: #1913

(I don't have a Linear ID for this one.)

## Checklist

- [x] Tests pass locally (PHP 8.3)
  - New tests: `TransactionTest::testFinishRespectsTraceIgnoreStatusCodesOption` (exact code, ranges and inclusive bounds, numeric string, no match, default), `TransactionTest::testFinishIgnoresTraceIgnoreStatusCodesOptionWithoutStatusCode` and `OptionsTest::testTraceIgnoreStatusCodesOptionIsValidatedCorrectly`, plus the new `optionsDataProvider()` and default-values entries. They fail without the `src/` changes and pass with them.
  - `vendor/bin/phpunit`: OK, 1561 tests (10 skipped, the same as on `master`).
  - `vendor/bin/php-cs-fixer fix --verbose --diff --dry-run`: no changes. `vendor/bin/phpstan analyse`: no errors. `vendor/bin/mago --config=mago.toml analyze`: no new issues (only the 3 warnings `master` already has).
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, it is updated during releases (AGENTS.md)
- [x] Documentation is updated (if applicable) — option docs in `src/functions.php` and the `Options` getter/setter docblocks; the user-facing docs in `sentry-docs` need a follow-up
- [x] PR title uses conventional commit style (`feat:`)
