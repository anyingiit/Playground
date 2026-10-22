## Description

`Translator::exists()` only looks up the key it is given, but a string with plural forms is stored under its singular and plural msgids joined by a NUL byte (the key `ngettext()` builds). So, as reported in #59, `exists('event')` is `false` for an entry with `msgid "event"` / `msgid_plural "event+"`, and there was no way to check such an entry at all.

This adds an optional second parameter, mirroring `ngettext()`:

```php
$translator->exists('event', 'event+'); // true
```

Existing calls are unaffected (`exists('event')` keeps its meaning and still returns `false` for a plural-only entry, since the lookup by singular alone would need a scan of the cache, which `ApcuCache` cannot do cheaply). The docblock says how plural entries are checked. A new `MoFilesTest::testExistsWithPlural` runs over every `.mo` fixture, like `testExists`.

I did not add a CHANGELOG entry since entries there reference the PR number — happy to add one once the PR exists, and to retarget `5.4.x` / `6.0.x` if you'd rather ship this as a fix there.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues / help-wanted issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #59

## Checklist

- [x] Tests pass locally — `vendor/bin/phpunit` → 127 tests OK (21 skipped: the APCu tests, no APCu here). Without the change the 6 new data sets fail. `vendor/bin/phpcs` on the changed files is clean; PHPStan reports the same output as on `master` (I ran it without the phpstan extensions installed).
- [ ] `CHANGELOG.md` is updated — see above.
- [x] Documentation is updated — the method docblock.
