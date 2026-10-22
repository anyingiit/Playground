<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KMcyNnzD6JeAFXoMMWEfs3D)_

## Description

The provider store and the model store were unified into a single `infoStore` in `pkg/plugins/model-provider-resolver/store.go` (#288 / #308), but their tests were still split between `store_test.go` and `model_store_test.go`.

This moves the four `TestModelStore_*` tests into `store_test.go` (after the `TestProviderStore_*` tests) and deletes `model_store_test.go`. The only other change is the `common/provider` import that the model tests need. No test logic is changed: the package still has the same 74 tests, and all of them pass.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #315

## Checklist

- [x] Tests pass locally: `go test -count=1 ./pkg/plugins/model-provider-resolver/` ok; `go test -list` gives 74 tests both before and after; `go vet` clean; `make lint` (golangci-lint) reports 0 issues
- [ ] Changelog: n/a
- [ ] Docs: n/a

🤖 Generated with [Claude Code](https://claude.com/claude-code)
