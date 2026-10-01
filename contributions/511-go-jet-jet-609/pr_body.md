## Description

In MySQL, a backslash is an escape character inside string literals (unless the `NO_BACKSLASH_ESCAPES` sql mode is enabled). The shared `stringQuote` helper only doubles single quotes, so a value such as `\'; DROP TABLE sensitive; --` passed to `jet.FixedLiteral` (or rendered by `DebugSql()`) produced `'\''; DROP TABLE sensitive; --'`, where `\'` escapes the quote and the rest of the value escapes the literal.

This PR makes the MySQL dialect's `ArgumentToString` handle `string` values itself, escaping `\` → `\\` in addition to `'` → `''`. This also covers `driver.Valuer` values that return a string, since they go through the same hook. PostgreSQL and SQLite are unchanged because they treat backslashes literally in standard string literals. `[]byte` already uses hex literals.

Notes for reviewers:
- On a server running with `NO_BACKSLASH_ESCAPES`, an escaped literal now shows each backslash twice in the value. That is a cosmetic difference and can't break out of the literal. Not escaping is exploitable under the default sql mode, so escaping looked like the safer default.
- JSON object keys (`WriteJsonObjKey`) still use the generic quoting. The existing `tests/mysql/select_json_test.go` depends on MySQL reading backslash escapes inside aliases, so I left that path alone.
- `fmt.Stringer` values still use the generic path.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #609

## Checklist

- [x] Tests pass locally: the new `TestStringLiteralBackslashEscaping` fails without the fix and passes with it; `go test ./mysql/ ./postgres/ ./sqlite/ ./internal/...` all ok; `go vet ./mysql/` and `gofmt -l` clean; `golangci-lint run ./mysql/...` reports the same 7 issues as master and none new. I didn't run the DB-backed `tests/mysql` suite because it needs a MySQL server.
- [ ] `CHANGELOG.md` is updated (if applicable): n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable): n/a
