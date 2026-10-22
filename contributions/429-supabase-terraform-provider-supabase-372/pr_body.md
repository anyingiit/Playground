<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KMcyNnzD6JeAFXoMMWEfs3D)_

Fixes #372

`readProject` sets `instance_size` from the `compute_instance` entry in `selected_addons` returned by `GET /v1/projects/{ref}/billing/addons`. Before reading, it resets the value to null. Nano is the base compute size, not an addon, so a nano project has no such entry, and `instance_size` ends up null. With `instance_size = "nano"` in the config, apply then fails:

```
Error: Provider produced inconsistent result after apply
... .instance_size: was cty.StringVal("nano"), but now null.
```

This PR makes `readProject` default `instance_size` to `nano` when no `compute_instance` addon is selected. A selected compute addon still overrides it as before. `instance_size` is `Optional` + `Computed`, so configs that don't set it get `nano` in state on refresh, with no diff.

### Testing

- New `TestAccProjectResource_NanoInstanceSize` covers create and import, mocked with gock. The billing endpoint returns an empty `selected_addons`.
  - Before the change it fails with exactly the error from the issue.
  - After the change it passes. The import step checks that a nano project imports with `instance_size = "nano"`.
- `TF_ACC=1 go test ./internal/provider/ -count=1`: all tests pass. They use the gock mocks; nothing runs against the real API.
- `golangci-lint run ./...`: 0 issues.

Note: I don't have a Supabase account to test against, so I have not checked the live API. The change relies on the reporter's observation that `selected_addons` is empty for nano projects. This matches Supabase's [compute docs](https://supabase.com/docs/guides/platform/compute-and-disk), which describe Nano as the free-plan base instance rather than an add-on. The existing tests mock micro projects as returning a `ci_micro` compute addon.

This change was prepared with AI assistance (Claude Code). I reviewed the diff and ran the tests above myself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
