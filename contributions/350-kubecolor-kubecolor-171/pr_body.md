# Description

`InspectSubcommandInfo` picked the first argument that looked like a known subcommand, without considering that it might be the value of a global flag. So in `kubecolor -n config get pod` the namespace value `config` was taken as the subcommand and the wrong printer was used (same for e.g. `--context logs get pod`).

## Type of change

- [x] Bug fix (fixes an issue)

## Changes

- Added a list of kubectl's global flags that take a value (from `kubectl options`: `-n/--namespace`, `--context`, `--kubeconfig`, `-s/--server`, `--user`, `--cluster`, `-v`, ...).
- While looking for the subcommand, the argument following such a flag is skipped when the value is passed separately (`-n config`). The `-n=config`, `--namespace=config` and `-nconfig` forms were already a single argument and keep working. Flags after the subcommand are unaffected because the loop returns at the first subcommand found.
- Added regression cases to `TestInspectSubcommandInfo` (e.g. `-n config get pod`, `--context logs get pod`, `-s top --user exec get pod -o wide`, `-n get` → help). They fail without the fix (7 subtests) and pass with it.

Verified locally: `go test ./...` and `go test -race ./kubectl/` ok; `make corpus` 98 passed / 0 failed; `go fmt ./...` and `go vet ./...` clean; `staticcheck ./...` reports nothing in changed files.

## Motivation

Fixes incorrect coloring when global flags with values are placed before the subcommand, as reported in #171.

Disclosure: I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue (if exists)

Closes #171
