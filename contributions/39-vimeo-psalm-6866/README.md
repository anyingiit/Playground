# vimeo/psalm #6866 — implode(<non-empty-string>, non-empty-list<string>) wrongly inferred as non-empty-string

| 项 | 值 |
|---|---|
| Issue | https://github.com/vimeo/psalm/issues/6866 |
| Tier | 自由 |
| Labels | Help wanted, bug, easy problems, good first issue, internal stubs/callmap |
| Status | 🚧 in progress — audit |
| Duplicate-PR check | (pending) |

## Notes so far
- Issue (2021, jnvsor): `implode('asdf', [''])` returns `''`, but Psalm infers `non-empty-string`. orklah (maintainer) suggested adding a nested conditional to the stub. Reporter re-hit it 2022.
- Stub still unchanged on master 79465b8 (stubs/CoreGenericFunctions.phpstub `implode`).
- No AI policy found in CONTRIBUTING.md / docs/contributing / .github.
- Project very active (danog), merges outside PRs (yuriy-sorokin, janedbal, Portll, Eljees ... Sep 2026).
