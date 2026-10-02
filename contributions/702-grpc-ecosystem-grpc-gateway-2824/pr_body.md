#### References to other Issues or PRs

Fixes #2824

#### Have you read the [Contributing Guidelines](https://github.com/grpc-ecosystem/grpc-gateway/blob/main/CONTRIBUTING.md)?

Yes.

#### Brief description of what is fixed or changed

## Description

`protoc-gen-openapiv2` had its own hand-written parser for the `http.proto` path template syntax (`templateToParts` plus `processParametersInSegment`). It duplicated `internal/httprule`, which `protoc-gen-grpc-gateway` uses. This PR removes the duplicate and uses the httprule parser for both generators, as #2824 proposes.

- `internal/httprule`: add `SplitTemplate(tmpl) ([]Segment, verb string, error)`. It parses with the existing parser (`Parse` now delegates to the same internal `parse` function) and returns the top-level segments: literal/wildcard segments, and variable segments as `FieldPath` + pattern. The root template `/` has no segments.
- `genopenapi.templateToParts` now builds its parts from `SplitTemplate`, so the output format is the same as before (`""` for the leading `/`, `{name}` / `{name=pattern}` parts, `:verb` last). `partsToOpenAPIPath`, `partsToRegexpMap` and `expandPathPatterns` are unchanged. A trailing `:` (parsed as an empty verb) is still kept in the path, so `TestRenderServicesWithColonLastInPath` stays as it is.
- Bazel: `//internal/httprule` added to the `genopenapi` library deps.

Behavior notes for reviewers:

- `templateToParts` only ever receives `b.PathTmpl.Template`, which was already validated with `httprule.Parse` when the registry was loaded. Templates that httprule rejects could never reach the OpenAPI generator. I updated the unit-test inputs that only the old parser accepted: added the missing leading `/` to the `test/{a}` camel-case cases, dropped the trailing `/` in the expand-slashed cases, and removed `/{test1}/{test2}/`, `/test/{name=*}/`, `/{name=prefix/*}/:customMethod` and `/foo/:bar`, which `httprule.Parse` rejects. `TestPartsToOpenAPIPathVerbSuffix` (from #7191) is kept as is, because it tests `partsToOpenAPIPath` directly.
- One visible change: an explicit `{name=*}` is now treated exactly like `{name}`, as the gateway does, so it no longer gets a redundant `pattern: "[^/]+"`. A test case in `TestFQMNToRegexpMap` covers this. No proto in the repo uses `{x=*}`.
- To check that nothing else changes, I compared the old and new `templateToParts` on all 145 distinct path templates found in the repo's `.proto`/`.yaml` files (examples, testdata), with and without `json_names_for_fields`. Both produced identical OpenAPI paths and regexp maps. This was a throwaway test and is not part of the PR.
- `protoc-gen-openapiv3` has its own `convertPathTemplate`. I left it alone to keep this PR focused, but it could use `SplitTemplate` in a follow-up.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #2824

## Checklist

- [x] Tests pass locally
  - New `TestSplitTemplate` (httprule) and new cases in `TestTemplateToOpenAPIPath` / `TestFQMNToRegexpMap`. With the implementation reverted, httprule fails to build (`undefined: SplitTemplate`) and `TestFQMNToRegexpMap` fails for `/{test=*}`. With the change, both pass.
  - `go test ./internal/... ./protoc-gen-openapiv2/... ./protoc-gen-grpc-gateway/... ./protoc-gen-openapiv3/...`: all ok
  - `go tool staticcheck ./internal/httprule/ ./protoc-gen-openapiv2/...`: clean. `gofmt -l`: clean. `go build ./...`: ok
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (release notes are written from PRs)
- [ ] Documentation is updated (if applicable) — n/a (internal refactor, no user-facing options)

#### Other comments

I didn't run Bazel or `make generate` locally. The only Bazel change is the `//internal/httprule` dep, which is what gazelle would add. No generated files change.
