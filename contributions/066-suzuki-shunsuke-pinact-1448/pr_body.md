## Check List

- [x] Read [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] [Write a GitHub Issue before creating a Pull Request](https://github.com/suzuki-shunsuke/oss-contribution-guide/blob/main/README.md#create-an-issue-before-creating-a-pull-request)
  - Link to the issue: #1448
- [x] [All commits are signed](https://github.com/suzuki-shunsuke/oss-contribution-guide/blob/main/docs/commit-signing.md)
  - This repository enables `Require signed commits`, so all commits must be signed
- [Avoid force push](https://github.com/suzuki-shunsuke/oss-contribution-guide?tab=readme-ov-file#dont-do-force-pushes-after-opening-pull-requests)

## Description

`ErrCantPinned` ("action can't be pinned") was returned from several branches of `processAction` without any context, so users couldn't tell why pinact refused to pin an action (#1448).

This PR wraps the sentinel with the reason via a small helper (`fmt.Errorf("%w: %s", ErrCantPinned, reason)`), so `errors.Is(err, ErrCantPinned)` still holds and exit codes (`classifyLineError`) are unchanged. Examples:

```
failed to handle a line: action can't be pinned: the version "master" isn't semver: only semver versions (e.g. v1.2.3) and full-length commit SHAs are supported by design. To pin branches, use --branch-to-tag. See https://github.com/suzuki-shunsuke/pinact/blob/main/docs/why_pinact_not_pin.md
failed to handle a line: action can't be pinned: the version "d41d8cd98f00b204e9800998ecf8427e" looks like a commit hash but isn't a full-length (40 characters) commit SHA
```

Other cases covered: invalid version comment on a tag (`@v3 # v3`), non-semver version with a semver comment without `--update`, comment already at the latest version, `--no-api`, and `--branch-to-tag` finding no semver tag.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code, reviewed by me, and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1448

## Checklist

- [x] Tests pass locally — new `TestController_parseLine_cantPinnedReason` fails before the change and passes after; `go test ./... -race -covermode=atomic` ok, `go vet ./...` ok, `golangci-lint run` (v2.14.0) 0 issues, `gofumpt -l` clean
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (releases are generated)
- [ ] Documentation is updated (if applicable) — n/a (error message only; it links the existing `docs/why_pinact_not_pin.md`)
