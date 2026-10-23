Fixes #186

The help text for `ochami metadata --uri` said "boot service", because it was copied from the `boot` command. It now says "metadata service":

```
$ ochami metadata --help | grep -- --uri
      --uri string           absolute base URI or relative base path of metadata service
```

The issue asks to check the other service commands as well. To keep that checked going forward, this PR adds `TestServiceURIFlagUsage` in `cmd/root_test.go`. For each top-level command with a persistent `--uri` flag (boot, bss, cloud-init, metadata, pcs, rcs, smd), it checks that the help text names that command's service. It also fails if a new service command adds `--uri` without a matching entry. The other six were already correct.

### Testing

- `go test ./cmd/ -run TestServiceURIFlagUsage` fails on `main` (`ochami metadata --uri usage = "... of boot service"`) and passes with this change.
- `go test ./...`: all packages pass.
- `golangci-lint run ./...` (v2.15.0, as in CI): 0 issues.

The commit is signed off (DCO).

This change was prepared with AI assistance (Claude Code). I reviewed the diff and ran the tests above myself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
