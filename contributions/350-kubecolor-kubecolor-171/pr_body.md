## Description

`InspectSubcommandInfo` picked the first argument that looked like a known subcommand, without considering that it might be the value of a global flag. So in `kubecolor -n config get pod` the namespace value `config` was taken as the subcommand and the wrong printer was used (same for e.g. `--context logs get pod`).

This change adds a list of kubectl's global flags that take a value (from `kubectl options`: `-n/--namespace`, `--context`, `--kubeconfig`, `-s/--server`, `--user`, `--cluster`, `-v`, ...) and, while looking for the subcommand, skips the argument that follows such a flag when its value is passed separately (`-n config`). The `-n=config`, `--namespace=config` and `-nconfig` forms were already a single argument and keep working. Flags after the subcommand are unaffected because the loop returns at the first subcommand found.

Regression cases added to `TestInspectSubcommandInfo` (e.g. `-n config get pod`, `--context logs get pod`, `-s top --user exec get pod -o wide`, `-n get` → help).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #171

## Checklist

- [x] Tests pass locally (`go test ./...` and `go test -race ./kubectl/` all ok; `make corpus` 98 passed / 0 failed; `go fmt ./...` and `go vet ./...` clean; `staticcheck ./...` reports nothing in changed files — only pre-existing findings in `internal/cmd/configdoc`). New test cases fail without the fix (7 subtests) and pass with it.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, internal parsing fix
