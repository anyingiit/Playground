## Description

`direnv reload` only returned an error when the `.envrc` had been explicitly **denied** (added in #1543).
For an `.envrc` that has never been allowed — or whose content changed after it was allowed, which is the
common case — `RC.Allowed()` returns `NotAllowed`, so the command just touched the file and exited `0`.
The user gets no feedback and assumes the reload worked, which is exactly what #1588 describes.

The fix changes the check in `cmd_reload.go` from `== Denied` to `!= Allowed`, so both `NotAllowed` and
`Denied` produce the existing error message (the same one `RC.Load` uses for `NotAllowed`) and a non-zero
exit status:

```
$ direnv reload        # .envrc never allowed
direnv: error /tmp/p/.envrc is blocked. Run `direnv allow` to approve its content
$ echo $?
1
```

Allowed `.envrc` files behave as before (touch + exit 0). New unit tests in
`internal/cmd/cmd_reload_test.go` cover the not-allowed, denied and allowed cases; the not-allowed test fails
without the fix.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1588

## Checklist

- [x] Tests pass locally — `go test ./...` (all ok), `go test ./internal/cmd -run TestReload -v` (3 passed; `TestReloadNotAllowed` fails on master), `go vet ./...` clean, `golangci-lint run ./internal/cmd/...` 0 issues, `bash ./test/direnv-test.bash` passes, and a manual check with the built binary (never allowed → exit 1, allowed → exit 0, denied → exit 1)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the changelog is generated during `make prepare-release`
- [ ] Documentation is updated (if applicable) — n/a, no documented behaviour changes
