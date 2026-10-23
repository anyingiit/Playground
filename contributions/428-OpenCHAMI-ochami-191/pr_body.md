Fixes #191

`smd group add` and `smd rfe add` get their client from `smd.GetClient` (`internal/cli/smd/smd.go`), which already calls `rt.UseCACert`. Both commands then called `rt.UseCACert` again on the same client, so the CA file was read and parsed twice. This PR removes the second call and its comment from both commands, as the issue suggests. The `UseCACert` call in `discover static` stays, because that command builds its client with `smd.NewClient`.

### Testing

Both checks from the issue are covered:

- **Invalid `--cacert` still exits with `CodePayload`.** `TestCommands_RejectInvalidCACert` already covers `smd group add` and `smd rfe add`, and it still passes.
- **A valid `--cacert` is still used.** The new `TestSMDAdd_TrustsCACert` in `cmd/smd_test.go` runs both commands against an `httptest.NewTLSServer`. It writes the server's certificate to a temp file and passes it as `--cacert`, then asserts that the POST arrives.
  - I checked that it really depends on `--cacert`: with the flag removed from the test, both cases fail with a TLS error (exit 7).
  - It passes both before and after this change, because it is a regression guard for a refactor, not a red→green test.

Other runs:

- `go test ./...`: all packages pass.
- `golangci-lint run ./...` (v2.15.0, as in CI): 0 issues.

The commit is signed off (DCO).

This change was prepared with AI assistance (Claude Code). I reviewed the diff and ran the tests above myself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
