## Description

When nothing has been saved in the admin panel, `AppConfig::getVerifyPeerOff()` falls back to the `eurooffice` section of `config.php` and compared the value with the string `"true"`. Writing `'eurooffice' => ['verify_peer_off' => true]` — the natural way in PHP — therefore gave `true === "true"` → `false`, and peer verification silently stayed on.

As suggested in #151, the fallback now goes through the existing `AppConfig::isTrue()` helper (added in #150 for the same bug class), so a native bool works, and the string forms it already accepts (`"true"`, `"yes"`, `"on"`, `"1"`) keep working. The value saved through the admin panel is read exactly as before.

A new `tests/unit/lib/AppConfigTest.php` covers the fallback with a native `true`/`false`, the strings `"true"`/`"false"` and an unset key.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #151

## Checklist

- [x] Tests pass locally — Nextcloud 34 (`stable34`, SQLite, app enabled as in the PHPUnit workflow), `composer test` → `OK (40 tests, 84 assertions)`. Without the fix the "native bool true" case fails. `phpcs --standard=./ruleset.xml` on the changed files and `php -l` are clean.
- [ ] `CHANGELOG.md` is updated — n/a, the changelog is generated from PR titles at release time.
- [ ] Documentation is updated — n/a.
