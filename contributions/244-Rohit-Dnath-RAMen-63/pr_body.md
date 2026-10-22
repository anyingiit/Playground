## Summary

`SPOP` and `SRANDMEMBER` no longer copy the whole set to pick members. A plain call (no count, or count 1) is now O(1) and allocates only the one-element result, so `SPOP` no longer holds the shard's write lock for an O(n) copy and draining a big set is no longer O(n²).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related Issue
Closes #63

## Changes
- `internal/store/set.go`: `sampleMembers(members []string, …)` is replaced by `sampleSet(set map[string]struct{}, count)`, which works on the map directly:
  - **count 1:** first key of a `range` over the map, then return. O(1), same approach as `RandomKey`. As the issue allows, this relies on Go's randomised map iteration, so it's random but not perfectly uniform; this is documented in the code comment and in `docs/commands.md`.
  - **1 < count < size:** reservoir sampling (Algorithm R) over one pass of the map, then a shuffle of the `count` results so their order is random too. Uniform, allocates only `count` slots (no O(n) copy; still one O(n) pass).
  - **count ≥ size**, or **negative count** (repeats, needs random access): copy the members as before.
- `internal/store/store_test.go`:
  - `TestSetSampleDoesNotCopyWholeSet`: on a 100k-member set, `SRANDMEMBER`/`SPOP` with count 1 and 5 each allocate ≤ 4 KiB per call (before: ~1.6 MB per call), and the pops remove the right number of members. Fails on `main`.
  - `TestSRandMemberCountReachesEveryMember`: 2000 draws of 3 from 10 members are always distinct and reach every member a plausible number of times (300–900 against an expectation of 600).
  - `BenchmarkSRandMember` / `BenchmarkSPop` on a 1M-member set.
- `docs/commands.md`: notes the single-member pick is O(1) and not perfectly uniform.

Benchmarks (1M members, 4 cores):

| | before | after |
|---|---|---|
| `BenchmarkSRandMember` | 71.0 ms/op, 16.0 MB/op | 535 ns/op, 16 B/op |
| `BenchmarkSPop` | 69.5 ms/op, 16.0 MB/op | 791 ns/op, 16 B/op |

## Checklist
- [x] I've read CONTRIBUTING.md
- [x] Tests pass (`go test -race ./...`: all packages ok; `go vet ./...` clean)
- [x] Code is formatted (`gofmt -l .` reports nothing)
