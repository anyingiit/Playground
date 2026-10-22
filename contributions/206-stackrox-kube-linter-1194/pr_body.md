## Description

Adds an `ignoredKeys` parameter to the `sorted-keys` template. The values of the listed keys are not checked for sorting at any nesting level, so a custom check with `ignoredKeys: ["labels", "annotations"]` skips `metadata.labels`/`annotations` (including `spec.template.metadata.*`), which Helm charts often render from user values via `include`. The position of the ignored key among its siblings is still checked, and the default (empty list) keeps the current behavior. Keys are matched by exact name (`+noregex`); happy to switch to path- or regex-based matching if you prefer.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1194

## Checklist

- [x] Tests pass locally
  - `go test ./pkg/templates/sortedkeys/...` — new table cases fail without the template change and pass with it
  - `go test ./pkg/... ./docs/...` — ok
  - `golangci-lint run ./pkg/templates/sortedkeys/...` — 0 issues
  - Checked with a built binary and a custom check using `ignoredKeys: ["labels", "annotations"]`: only the container key-order finding remains
- [x] Documentation is updated (if applicable) — `go generate` for params and regenerated `docs/generated/templates.md`
