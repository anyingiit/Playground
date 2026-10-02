## Description

When a procedure, function, event or trigger is created or edited through the editor dialog, the success message shows the executed query without `DELIMITER`. As soon as the body contains `;` (e.g. `BEGIN ... ; ... END`), copying that query into the SQL tab or the mysql client, or using the **Edit** / **Edit inline** links, fails, because the first `;` ends the statement.

This PR wraps the displayed `CREATE ...` statement in `DELIMITER $$ ... $$ DELIMITER ;`, the same way the routine and trigger export already does it (`"DELIMITER $$\n" . $definition . "$$\nDELIMITER ;\n"`):

- New helper `Util::getQueryWithDelimiter()`.
- `Database\Routines`, `Database\Events`, `Database\Triggers`: the query passed to `Generator::getMessage()` is now wrapped, both in "add" and in "edit" mode. In edit mode the `DROP ... ;` statement stays in front of the `DELIMITER $$` line, so it still ends with a normal `;`.
- Only the query that is **displayed** changes. The query sent to the server is the same as before.
- ChangeLog entry under 5.2.4.

Example (create procedure), before:

```sql
CREATE PROCEDURE `p`() BEGIN SELECT 1; SELECT 2; END
```

after:

```sql
DELIMITER $$
CREATE PROCEDURE `p`() BEGIN SELECT 1; SELECT 2; END$$
DELIMITER ;
```

`UtilTest::testGetQueryWithDelimiter` checks the exact output, and that the SQL parser reads the wrapped query as exactly one `CREATE` statement (and the edit form as `DROP` + `CREATE`) with no errors. The `handleEditor()` code paths that render the message end with `exit` in AJAX mode, so they are not unit-testable on QA_5_2. That is why the logic is in a small helper.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #19578

## Checklist

- [x] Tests pass locally (PHP 8.3)
  - `vendor/bin/phpunit --testsuite unit`: OK (3190 tests, 44 skipped). The new test errors without the fix (`Call to undefined method Util::getQueryWithDelimiter()`) and passes with it.
  - `vendor/bin/phpcs` on the changed files: clean.
  - `vendor/bin/phpstan analyse` and `vendor/bin/psalm` on the changed files: same issues as on `QA_5_2` without this change, no new ones.
  - Not run: the selenium tests (no MySQL/browser available locally).
- [x] `ChangeLog` is updated — entry under 5.2.4
- [ ] Documentation is updated (if applicable) — n/a
- [x] I have read [CONTRIBUTING.md](https://github.com/phpmyadmin/phpmyadmin/blob/master/CONTRIBUTING.md).
- [x] The pull request targets the correct branch (`QA_5_2`, bug fix for a released version).
- [x] Every commit has a proper `Signed-off-by` line as described in the [DCO](https://github.com/phpmyadmin/phpmyadmin/blob/master/DCO).
- [x] Every commit has a descriptive commit message, and each commit is needed on its own.
- [x] Any new functionality is covered by tests.
