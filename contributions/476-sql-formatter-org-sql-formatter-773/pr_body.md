## Description

DB2 for i accepts two forms of key/value pair in `JSON_OBJECT()` and `JSON_OBJECTAGG()`: `KEY 'k' VALUE v` and `'k' : v` ([IBM i reference](https://www.ibm.com/docs/en/i/7.5?topic=functions-json-object)). The db2i dialect has no `:` operator, so the colon form fails:

```
SELECT JSON_OBJECT('key':'val') FROM SYSIBM.SYSDUMMY1;
-- Parse error: Unexpected ":'val') FR" at line 1 column 25. SQL dialect used: "db2i".
```

This adds `':'` to the db2i operators. The formatter already has a rule for a standalone `:` (no space before, one space after), so the result is:

```sql
SELECT
  JSON_OBJECT('key': 'val')
FROM
  SYSIBM.SYSDUMMY1;
```

Named host variables like `:id` are still matched as parameters before the operator, so `WHERE id = :id` is unchanged (covered by a new test). One edge case stays as it was: `'id':id` with no space after the colon is still read as the string `'id'` followed by the host variable `:id`, the same as before this change. Since IBM i requires the key in the colon form to be a string literal, the common `'key': value` and `'key' : value` spellings are what this fixes.

Because db2i is the only dialect that has both `:name` parameters and a `:` operator, there is one more small change: with `denseOperators: true`, `:` keeps the space after it in dialects where `:name` is a named parameter. Without that, `'arr' : JSON_ARRAY(1, 2)` would be printed as `'arr':JSON_ARRAY(1, 2)`, which reads back as the host variable `:JSON_ARRAY`. This follows the same idea as the existing `identifierDashes` guard for `-`. It is covered by a test.

As a side effect, colon labels such as `lbl: BEGIN ... END lbl`, which were also parse errors before, now format.

I kept it to db2i, as reported in the issue.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #773

## Checklist

- [x] Tests pass locally: `pnpm test` (27 suites, 5888 passed, 1 skipped), plus `tsc --noEmit`, `prettier --check .` and `eslint .`
- [x] Added tests in `test/db2i.test.ts`; the JSON_OBJECT and denseOperators tests fail without the source change and pass with it
- [ ] `CHANGELOG.md` — n/a (the repo has no changelog)
- [ ] Documentation — n/a

🤖 Generated with [Claude Code](https://claude.com/claude-code)
