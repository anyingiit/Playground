<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KU5CcqhtizgR6Af7udenHiG)_

## Description

DB2 for i accepts two forms of key/value pair in `JSON_OBJECT()` and `JSON_OBJECTAGG()`: `KEY 'k' VALUE v` and `'k' : v` ([IBM i reference](https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_76/db2/rbafzscajsonobject.htm)). The db2i dialect has no `:` operator, so the colon form fails:

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

I kept it to db2i, as reported in the issue.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #773

## Checklist

- [x] Tests pass locally: `pnpm test` (27 suites, 5887 passed, 1 skipped), plus `tsc --noEmit`, `prettier --check .` and `eslint .`
- [x] Added tests in `test/db2i.test.ts`; the JSON_OBJECT test fails without the source change and passes with it
- [ ] `CHANGELOG.md` — n/a (the repo has no changelog)
- [ ] Documentation — n/a

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012YkMb3Q6rZmThSA5aAF7CA
