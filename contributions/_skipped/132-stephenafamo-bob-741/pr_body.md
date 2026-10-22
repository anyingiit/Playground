## Description

Without `PreloadAs`, `orm.Preload` gave every joined table an alias with a suffix from the global `bob.NextUniqueInt()` counter (`"users_10001"`, `"users_10005"`, ...). So building the same query twice gave different SQL text. As #741 explains, that defeats statement caches keyed by the SQL text, like pgx's automatic prepared statement cache (and it grows that cache).

The suffix now comes from a new helper, `preloadAlias`. It is an FNV-1a 64-bit hash, printed in base 36, of the join's position in the preload tree: parent alias, relationship name and side index. As a result:

- the same query always builds to the same SQL;
- different relationships to the same table from the same parent (e.g. `Author` / `Editor` → `users`) get different aliases;
- the same relationship nested under different parents (e.g. `Author.Pets` / `Editor.Pets`) gets different aliases, because the parent alias is part of the hash;
- the alias length is bounded (`<table>_` plus at most 13 characters), however deep the nesting. Using the readable path directly could go past PostgreSQL's 63-byte identifier limit for the `"<alias>.<column>"` select names.
- `PreloadAs` is unchanged.

Example (`posts` preloading `Author.Pets` and `Editor.Pets`), the same on every build:

```sql
LEFT JOIN "users" AS "users_3hq9we9h8wy8n" ON "posts"."author_id" = "users_3hq9we9h8wy8n"."id"
LEFT JOIN "pets" AS "pets_1cpdn7gbvyp8g" ON "users_3hq9we9h8wy8n"."id" = "pets_1cpdn7gbvyp8g"."owner_id"
LEFT JOIN "users" AS "users_lxhlruvdplb9" ON "posts"."editor_id" = "users_lxhlruvdplb9"."id"
LEFT JOIN "pets" AS "pets_g05b7vta445g" ON "users_lxhlruvdplb9"."id" = "pets_g05b7vta445g"."owner_id"
```

Things reviewers may want to weigh:

- This is not random like the old `randInt` that #639 replaced. The alias depends only on the preload path, so two different joins in one query can only collide if their 64-bit hashes collide.
- If the *same* relationship is preloaded twice from the same parent in one query, both joins now get the same alias. Before, they got two different aliases. That seems like a mistake in the calling code anyway, but it is a behaviour change.
- The generated join helpers (`gen/templates/joins/table/120_joins.go.tpl`) still use `NextUniqueInt`. This PR keeps to the `Preload` path the issue is about.
- If you would prefer a different scheme (e.g. readable `parent_Rel` names, or a per-query counter, which would need an API change to `Preloader`), I'm happy to change it.

Tests: `orm/load_alias_test.go` builds a `psql.Select` with nested preloads several times. It checks that the SQL is identical every time, that the four join aliases are distinct and keep the `<table>_` prefix, and that `PreloadAs` still sets the alias. No database is needed.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #741

## Checklist

- [x] Tests pass locally. `go test -race -count=1 ./orm/ . ./dialect/sqlite ./dialect/mysql ./expr` passes. Without the change, `TestPreloadAliasesAreDeterministic` fails (`users_10001` vs `users_10005`). In `go test -race ./...`, every package that doesn't need Docker passes. `dialect/psql` and the `gen/bobgen-*/driver` packages could not run because they start testcontainers and there is no Docker in my environment. `golangci-lint run ./orm/...` reports 0 issues.
- [x] `CHANGELOG.md` is updated (if applicable). There is an entry under Unreleased → Changed.
- [ ] Documentation is updated (if applicable). n/a: the docs only describe `PreloadAs`, which is unchanged.
