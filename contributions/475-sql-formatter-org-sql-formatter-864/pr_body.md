<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KU5CcqhtizgR6Af7udenHiG)_

## Description

In the PostgreSQL dialect, `INTO` in `SELECT ... INTO` is not a clause, so the target table gets appended to the last selected column:

```sql
SELECT
  r.*,
  nrm.idx INTO parking_driveways
FROM
  ...
```

The Transact-SQL and DB2 dialects already list `INTO` as a reserved clause, and `SELECT col INTO #temp FROM tbl` formats with `INTO` on its own line there. This PR does the same for PostgreSQL, so the example from the issue now formats as:

```sql
SELECT
  r.*,
  nrm.idx
INTO
  parking_driveways
FROM
  ...
```

As you noted in the issue, `INTO` appears in other places too, so I checked those:

- `INSERT INTO` is matched as a whole phrase first, so it is unchanged (the existing tests pass).
- `MERGE INTO` was formatted on one line before. With `INTO` as a clause alone it would have become `MERGE` / `INTO` on two lines, so I also added `MERGE INTO` as a clause. It now formats as `MERGE INTO` followed by the indented rest. (Open PR #993 adds fuller MERGE support with the same `'MERGE INTO'` entry, so the two should merge without trouble.)
- `RETURNING ... INTO var` and `SELECT ... INTO STRICT var` (PL/pgSQL forms) also put `INTO` on its own line, which reads consistently with the above.
- `IMPORT FOREIGN SCHEMA ... FROM SERVER s INTO local_schema` now puts `INTO` on its own line instead of after `SERVER s`.

Redshift has the same `SELECT INTO` statement but I left it alone to keep the change small.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #864

## Checklist

- [x] Tests pass locally: `pnpm test` (27 suites, 5887 passed, 1 skipped), plus `tsc --noEmit`, `prettier --check .` and `eslint .`
- [x] Added tests in `test/postgresql.test.ts`; both fail without the source change and pass with it
- [ ] `CHANGELOG.md` — n/a (the repo has no changelog)
- [ ] Documentation — n/a

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012YkMb3Q6rZmThSA5aAF7CA
