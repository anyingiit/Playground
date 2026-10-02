## Description

Adds optional `name` and `match` query parameters to `GET /allocations`, so clients can list only the pins whose name matches instead of downloading the whole pinset and filtering it themselves.

```
GET /allocations?name=backup-2026&match=ipartial
GET /allocations?filter=pin&name=my-pin            # match defaults to exact
```

- The matching semantics are the same as the Pinning Services API (`/pins?name=…&match=…`). `match` accepts `exact` (the default when it is omitted), `iexact`, `partial` and `ipartial`. An unknown `match` value returns `400`, the same way an invalid `filter` does.
- The name filter combines with the existing `filter` (pin type) parameter. A pin is returned only if it passes both.
- To avoid duplicating the logic, `pinsvc.Pin.MatchesName` now delegates to a new package-level `pinsvc.MatchesName(name, nameOpt, strategy)` function. The REST handler calls that function. The `pinsvc.Pin` behaviour is unchanged.
- Test: the mock `Cluster.Pins` now gives its three pins the names `aaa`, `bbb` and `ccc`, the same names the `StatusAll` mock already uses. `TestAPIAllocationsEndpoint` now covers the exact default, a partial name not matching under exact, `ipartial`, `iexact` combined with `filter=pin`, and an invalid `match` returning 400.

Note: the pinset has no name index, so the filtering happens on the server while the pins are streamed. It makes the response smaller and saves the client work, but the server still iterates over every pin.

Not included: the Go client (`client.Client.Allocations(ctx, filter, out)`) and `ipfs-cluster-ctl pin ls` are unchanged. Adding a parameter to that exported interface method would be a breaking change. I'm happy to follow up with a non-breaking client/ctl addition (for example a new method or an options variant) if you want one.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #2323

## Checklist

- [x] Tests pass locally (Go 1.26.0):
  - `go test -run TestAPIAllocationsEndpoint ./api/rest/ -count=1` fails before the handler change (5 new assertions) and passes after it
  - `go test ./api/... ./cmd/... -count=1`: all pass
  - `go vet ./api/... ./test/`: clean; `gofmt -l` reports no changed files
- [x] Self-reviewed the diff
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a: the changelog is written at release time
- [ ] Documentation is updated (if applicable) — the REST API reference is on ipfscluster.io, which is outside this repo; I can open a docs PR if that's helpful
