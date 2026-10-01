## Description

`StreamableHttpTransport` logs a warning whenever it is constructed with `middleware: []`. Integrations like Drupal's `mcp_server` pass an empty list on purpose (CORS and trusted-host validation are already handled by the framework's HTTP layer), and since PHP builds a new transport per request, every MCP request produces one warning.

This adds a trailing constructor argument `bool $warnOnEmptyMiddleware = true`. Passing `middleware: [], warnOnEmptyMiddleware: false` marks the empty list as deliberate and skips the warning; an accidental empty list still warns, and `null` still installs the defaults. The flag only affects logging — behaviour is unchanged.

While there, the warning text no longer says that protocol version validation is disabled: handshake-era requests always go through `handshakeMiddleware()` regardless of the custom list. The message now also mentions the new opt-out.

`docs/run/http.md` documents the flag next to the existing `middleware: []` paragraph, and `CHANGELOG.md` gets an entry under 0.9.0.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #523

## Checklist

- [x] Tests pass locally — new `testEmptyMiddlewareListWithOptOutDoesNotWarn` fails without the change and passes with it; `vendor/bin/phpunit --testsuite unit` → OK (1583 tests, 4 skipped); `tests/Integration/DualEraEndpointTest.php` and `HandshakeTest.php` OK; `vendor/bin/php-cs-fixer fix --dry-run --diff` → 0 files to fix; `vendor/bin/phpstan` → No errors. (Inspector tests weren't run: they need `npx @modelcontextprotocol/inspector`, which isn't reachable in my environment.)
- [x] `CHANGELOG.md` is updated (if applicable) — entry under 0.9.0
- [x] Documentation is updated (if applicable) — `docs/run/http.md`
