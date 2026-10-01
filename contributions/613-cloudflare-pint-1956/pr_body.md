## Description

`alerts/for` reports both invalid `for` / `keep_firing_for` durations (Bug) and fields that are explicitly set to the default value `0` (Information). Some teams prefer to always write `for: 0m` explicitly, but the only way to silence that report today is disabling the whole check, which also drops the invalid-duration validation.

This adds an optional `check "alerts/for"` settings block, following the same pattern as `check "promql/regexp" { smelly = ... }`:

```js
check "alerts/for" {
  redundant = false
}
```

- `redundant` defaults to `true`, so existing behaviour is unchanged.
- When set to `false`, `for` / `keep_firing_for` fields with the default value are no longer reported; invalid values are still reported.
- Wired into `config.Check.Decode()` so the block is accepted in `.pint.hcl`.
- Docs (`docs/checks/alerts/for.md`) and `docs/changelog.md` (new `v0.89.0` section) updated.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1956

## Checklist

- [x] Tests pass locally
  - New unit cases in `internal/checks/alerts_for_test.go` (+ snapshots) and a new testscript `cmd/pint/tests/0278_alerts_for_redundant_disabled.txt`; both fail without the change and pass with it.
  - `go test -race -count=1 ./internal/checks/ ./internal/config/ ./cmd/pint/` — all pass except `TestScripts/0228_watch_pidfile_remove_error`, which also fails on `main` in my environment (runs as root, so `chmod 000` does not deny access).
  - `make format` (no changes) and `make lint` (0 issues, deadcode clean).
- [x] `CHANGELOG.md` is updated (if applicable) — added `v0.89.0` / Added entry in `docs/changelog.md`
- [x] Documentation is updated (if applicable) — `docs/checks/alerts/for.md` Configuration section
