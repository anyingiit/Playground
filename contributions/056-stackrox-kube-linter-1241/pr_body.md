## Description

`env-value-from` only inspected `container.env[].valueFrom`, so a workload that pulls a missing ConfigMap/Secret in through `envFrom`, or mounts one as a volume, passed the check (see the reproduction in #1241).

This extends the existing check rather than adding a new one:

- `containers[].envFrom[].configMapRef` / `.secretRef`: the referenced object must exist (no key to check). Reported as `The container "app" is referring to an unknown config map "x"`, same wording as today.
- `volumes[].secret` / `.configMap`: the referenced object must exist, and every key listed in `items` must exist in it. Reported as `The volume "v" is referring to an unknown secret "x"` / `... unknown key "k" in secret "x"`. A missing object is reported once, not once per item.
- `optional: true` references and the `IgnoredSecrets` / `IgnoredConfigMaps` parameters are honored for the new sources too; namespace matching reuses the existing logic.
- Existing messages are unchanged (`checkResourceReference` now takes a subject like `container "app"` / `volume "v"`).

Not covered: projected volume sources (`projected.sources[].configMap/secret`); happy to add them if you'd like.

The check is not enabled by default, so this only affects users who opted in.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1241

## Checklist

- [x] Tests pass locally
  - `go test ./pkg/templates/envvarvaluefrom/...` — new `TestEnvFromReferences` and `TestVolumeReferences` fail without the fix and pass with it
  - `go test ./pkg/... ./internal/... ./cmd/... ./docs/...` — ok
  - `golangci-lint run ./pkg/templates/envvarvaluefrom/...` — 0 issues
  - `bats e2etests/bats-tests.sh -f env` (with a freshly built binary) — 4/4 ok; `tests/checks/env-var-value-from.yml` gained an envFrom + volume case and the `env-value-from` bats test now expects 6 reports
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog file
- [x] Documentation is updated (if applicable) — regenerated `docs/generated/templates.md` (template description now mentions volumes)
