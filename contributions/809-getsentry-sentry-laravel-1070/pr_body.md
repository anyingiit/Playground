### Description

Adds a default `class_serializers` entry for `Illuminate\Http\Client\Response`, so HTTP client responses in stack trace frames show useful information. Today they only show the class name.

- New `Sentry\Laravel\Serializer\HttpClientResponseSerializer` (marked `@internal`). It always returns:
  - `status` and `reason`
  - `url`: the effective URI, only when transfer stats are available (a request was actually sent). User info, query string and fragment are stripped unless `send_default_pii` is enabled.
  - `content_type`, when the header is present
- When `send_default_pii` is enabled, it also returns the response `headers`, flattened to strings so the serializer's max depth does not cut them off.
- The response **body is never included**. It can be large and can hold sensitive data, and reading it could consume a non-seekable stream. I kept the payload to this minimal safe set on purpose. Happy to add a truncated body behind `send_default_pii` if you'd prefer.
- `ServiceProvider::configureAndRegisterClient()` appends the default to the end of the user's `class_serializers` (only if the user has no entry for this class). Since sentry-php uses the first matching serializer, a user-defined serializer for the same class, or for a parent class or interface such as `ArrayAccess`, still wins. The default is only registered when the class exists (`class_exists` guard). If the user set `class_serializers` to a non-array value, it is left untouched. No new config options. The code stays PHP 7.2 compatible.
- Tests: `test/Sentry/Features/HttpClientResponseSerializerTest.php` checks that the serializer is registered, the output with PII off and on, a response without transfer stats, and that a user-configured serializer (for the class itself or for an interface it implements) takes precedence.
- `CHANGELOG.md` is not touched, as `AGENTS.md` asks. A release-notes entry would be something like: "Add class serializer for `Illuminate\Http\Client\Response` to show response details in stack traces (#1070)".

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

#### Issues

* resolves: #1070

#### Checklist

- [x] Tests pass locally (PHP 8.3, Laravel 13 / Testbench 11, PHPUnit 11): `vendor/bin/phpunit --filter HttpClientResponseSerializerTest` → OK (6 tests, 12 assertions). Without the `ServiceProvider` change, 4 of the 6 fail (the two precedence tests are regression guards). Full `vendor/bin/phpunit` → OK (247 tests, 728 assertions). The 13 PHPUnit deprecations are also there on `master`.
- [x] `composer cs-check` → 0 files to fix
- [ ] `composer phpstan` was not run locally (I couldn't install it in my environment). I'm relying on CI for that.
- [ ] `CHANGELOG.md`: n/a, per `AGENTS.md` it is updated at release time (suggested entry above)
- [ ] Documentation: n/a, there is no new option
