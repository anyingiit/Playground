## Description

Adds the `NotZero[T comparable]()` filtering operator requested in #74: it forwards only the items that are not the zero value of their type (`0`, `""`, `false`, `nil`, empty struct, ...), and mirrors error/completion notifications and the context chain like the other filtering operators (same structure as `Distinct`).

Following the end-to-end checklist in `docs/docs/hacking.md`:
- `operator_filter.go`: the operator, placed after `DistinctBy`.
- `operator_filter_test.go`: `TestOperatorFilterNotZero` (ints, strings, structs, pointers, all-zero source, `Empty`, `Throw`).
- `ro_example_test.go`: `ExampleNotZero_ok` / `ExampleNotZero_error`.
- `docs/data/core-notzero.md` + an entry in `docs/static/llms.txt`.
- The `sourceRef` line numbers of the filtering docs pointing below the new function in `operator_filter.go` were resynced (each one verified to point to its `func` line).

There's no `// Play:` link yet since the operator isn't released (an empty `// Play:` line fails `godot`); `playUrl` is left empty in the doc page, as done for other unreleased helpers.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #74

## Checklist

- [x] Tests pass locally (`go test -race .` in the root module: ok; the new test fails to compile without the operator (`undefined: NotZero`) and passes with it; `golangci-lint run ./` (v2.6.2): 0 issues; `headercheck`: no findings on the changed files)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog file
- [x] Documentation is updated (if applicable) — `docs/data/core-notzero.md`, `docs/static/llms.txt`, godoc example
