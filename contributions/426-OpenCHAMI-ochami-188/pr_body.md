<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KMcyNnzD6JeAFXoMMWEfs3D)_

Fixes #188

The four `metadata * delete` commands (`defaults`, `group`, `instance`, `peer`) created the metadata-service client in `RunE` and called `rt.HandleToken` at the top of `runCore*`. Both happened before the "Really delete?" prompt. With no base URI or token configured, they failed (exit 3) without ever prompting.

This PR moves the client creation and the token handling after the confirmation block. That matches `runCoreBootBmcDelete` and the other delete commands already covered by `TestDeleteConfirm_DeclineBeforeClient`. The `runCore*` functions no longer take the client as a parameter, the same as the boot delete commands. Nothing else in the repo calls them.

### Testing

- Added `metadata defaults/group/instance/peer` cases to `TestDeleteConfirm_DeclineBeforeClient` in `cmd/prompts_test.go`.
  - Without the change, all 4 new cases fail.
  - With it, they pass.
- `go test ./...`: all packages pass.
- `golangci-lint run ./...` (v2.15.0, as in CI): 0 issues.
- Manual check, reproducing the issue:
  ```
  $ echo n | ochami --ignore-config metadata peer delete id1
  Really delete? [yn]: ... WRN ... user aborted WireGuard peer deletion
  exit=8
  $ ochami --ignore-config metadata peer delete --no-confirm id1
  ... ERR ... base URI for metadata-service not found ...
  exit=3
  ```

The commit is signed off (DCO).

This change was prepared with AI assistance (Claude Code). I reviewed the diff and ran the tests above myself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
