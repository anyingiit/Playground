#### What this PR does / Which issue(s) does the PR fix:

Fixes #1687

`--config.check` currently only parses/validates the YAML, so a configuration that points to a missing TLS certificate, `body_file` or credential file passes the check and only fails later at probe time. This makes `--config.check` less useful as a deployment preflight (systemd `ExecStartPre`, Kubernetes init containers, CI).

This PR adds `(*config.Config).CheckFiles()`, which verifies that every local file referenced by the configuration exists, is not a directory, and can be opened for reading. All problems are reported at once (via `errors.Join`), each prefixed with the module name and the YAML path of the field, e.g.:

```
module "tcp_tls": tcp.tls_config.cert_file: open /certs/missing.crt: no such file or directory
```

Covered fields:
- `http.body_file`
- HTTP client config of the `http` prober and `websocket.http_config`: `basic_auth.username_file` / `password_file`, `authorization.credentials_file` (which `bearer_token_file` is normalised into by `Validate()`), `oauth2.client_secret_file` / `client_certificate_key_file` / `oauth2.tls_config.*`, `tls_config.ca_file` / `cert_file` / `key_file`, `http_headers.<name>.files`
- `websocket.headers.<name>.files`
- `tls_config.*` of the `tcp`, `unix`, `dns` and `grpc` probers

The check is only run in `--config.check` mode (`main.go`), so normal startup and config reload behaviour is unchanged. It is purely local: no DNS lookups or network connections are made. Relative paths are checked as-is, i.e. relative to the working directory, which is how the probers resolve them at runtime. The README documents the extended behaviour and the flag help text is updated.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

#### Does this PR introduce a user-facing change?

```release-notes
[ENHANCEMENT] `--config.check` now also verifies that local files referenced by the configuration (body_file, TLS CA/cert/key files, credential and header files) exist and are readable. #1687
```

**Checklist**
- [x] Tests updated — new `TestCheckFiles` in `config/config_test.go` with `config/testdata/check-files-{good,missing}.yml`; `go test ./config/ .` passes, `golangci-lint run ./config/... .` (v2.13.1, repo config) reports 0 issues, `gofmt -l .` clean, `yamllint` clean on the new testdata. Manually: `blackbox_exporter --config.check` exits 1 with the per-file errors for the missing-files config and 0 for `blackbox.yml`.
- [x] Documentation added — README section on `--config.check`, updated flag help.
- [x] CHANGELOG added in `release-notes` section of PR Desc.
