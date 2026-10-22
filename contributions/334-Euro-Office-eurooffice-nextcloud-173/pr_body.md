## Description

`EditorController::users()` passed the result of `IUserManager::get()` straight into `filterUser(IUser $user, …)`. `get()` returns `null` for a user id that no longer exists, so a stale entry in the share access list (or a group folder membership row of a deleted user) made the request fail with a `TypeError` — an HTTP 500 for everyone who opens the file, which breaks the mention/protect user picker.

This skips `null` users at both call sites (the access list and the group folder members), the smaller of the two fixes suggested in #173. It keeps `filterUser()`'s non-nullable signature and matches how `CallbackController` already guards the same call. I also looked at the other call sites named in the issue: `EmailManager` already checks for an empty result, and `EditorApiController` only passes the user to `setVolatileActiveUser()`, so they are left alone.

A new `tests/unit/lib/Controller/EditorControllerTest.php` drives `users()` with an access list of `["deleted-user", "alice"]` and asserts that only `alice` is returned. It mocks `OC\Files\Node\File` because the controller calls `getFileInfo()`, which is not part of `OCP\Files\File`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #173

## Checklist

- [x] Tests pass locally — Nextcloud 34 (`stable34`, SQLite, app enabled as in the PHPUnit workflow), `composer test` → `OK (36 tests, 70 assertions)`. Without the fix the new test fails with `TypeError: …filterUser(): Argument #1 ($user) must be of type OCP\IUser, null given`. `phpcs --standard=./ruleset.xml` on the changed files and `php -l` are clean.
- [ ] `CHANGELOG.md` is updated — n/a, the changelog is generated from PR titles at release time.
- [ ] Documentation is updated — n/a.
