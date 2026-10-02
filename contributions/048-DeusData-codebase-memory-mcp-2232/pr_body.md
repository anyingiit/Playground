## Description

`GET /api/project-health` passed the results of `cbm_store_count_nodes` / `cbm_store_count_edges` straight into its reply. Since #2065 those helpers return `CBM_STORE_ERR` (-1) on a failed read, so a store whose `nodes`/`edges` tables are missing or damaged was reported as `{"status":"healthy","nodes":-1,"edges":-1,...}`.

This applies the same rule `index_status` already uses: a negative count is a failed read, not a row count. In that case the handler now answers `{"status":"corrupt","reason":"cannot read <nodes|edges|nodes and edges>"}`, naming the table(s) that could not be read. `corrupt` is already one of the states `graph-ui/src/components/StatsTab.tsx` renders, so the UI needs no change. The healthy path is unchanged.

Regression test: `ui_server_project_health_reports_unreadable_counts_issue2232` in `tests/test_httpd.c` checks that an intact store reports `healthy`. It then drops `nodes` and `edges` and checks that the response is `corrupt` with the reason, and contains no `healthy` or `-1`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #2232

## Checklist

- [x] Tests pass locally (Ubuntu 24.04 x86_64, gcc + ASan/UBSan): `make -f Makefile.cbm test-focused TEST_SUITES=httpd` → `66 passed, 1 skipped`. Without the `src/ui/http_server.c` change the new test fails: `FAIL tests/test_httpd.c:1470: strstr(resp, "healthy") is not NULL`.
- [x] Lint: `clang-format` 20.1.8 `--dry-run --Werror` is clean on `tests/test_httpd.c` and on the changed hunk. The violations it reports in `src/ui/http_server.c` (lines 56–716) are already on `main` and are untouched here. `cppcheck` (2.13, Makefile.cbm flags) on `src/ui/http_server.c` reports the same findings before and after the change, so nothing new. `make -f Makefile.cbm lint-no-suppress` passes.
- [x] Commit is DCO signed-off.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a
- [ ] Documentation is updated (if applicable) — n/a, no API shape change (`corrupt` + `reason` already existed for `cannot open`)
