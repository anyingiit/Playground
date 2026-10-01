| Q             | A
| ------------- | ---
| Bug fix?      | no
| New feature?  | no
| Docs?         | no
| Issues        | Fix #2430
| License       | MIT

## Description

As described in #2430, adding a `Result\XResult` type without a matching `Message\Content\X` class and a `Message::toContent()` arm is only noticed when application code passes the result to `Message::ofAssistant()` (it then throws `Unsupported assistant message part`). Bridge tests never hit that path, which is how `CustomToolCallResult` (#2382) initially slipped through.

This PR takes the allow-list approach suggested in the issue and keeps it next to `Message`, not in the bridges: a new `tests/Message/AssistantContentMappingTest.php` that

- scans `src/Result/*.php` for every concrete class implementing `ResultInterface`,
- requires each one to be either in the data provider of results that must become assistant content (one sample instance per type, each run through `Message::ofAssistant()`), or in an explicit `NOT_ASSISTANT_CONTENT` list (`BatchResult`, `ChoiceResult`, `JobResult`, `ObjectResult`, `RealtimeSessionResult`, `RerankingResult`, `VectorResult`),
- fails with a message pointing to `Message::toContent()` when a new type is unclassified, and checks that no type is listed in both places.

Test-only change, no production code touched. A marker interface would be the alternative; I went with the test since it needs no API change, but happy to switch if you prefer that.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fix #2430

## Checklist

- [x] Tests pass locally: `cd src/platform && vendor/bin/phpunit tests` → OK (1072 tests, 2 skipped). The new test fails as intended when (a) the `CustomToolCallResult` arm is removed from `Message::toContent()` (`Unsupported assistant message part of type "...CustomToolCallResult"`) and (b) a dummy `Result\FooResult` is added (`... is neither mapped to assistant content ... nor listed in NOT_ASSISTANT_CONTENT`).
- [x] `vendor/bin/php-cs-fixer fix --dry-run --diff src/platform/tests/Message/AssistantContentMappingTest.php` → 0 files to fix; `cd src/platform && vendor/bin/phpstan analyse tests/Message/AssistantContentMappingTest.php src/Message` → No errors
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, test-only change (bug fix/no feature, so the changelog check forbids an entry)
- [ ] Documentation is updated (if applicable) — n/a
