# go-git/go-git #1518 — split fetch/push code out of `remote.go`

Status: 🚧 in progress — audit done (AUDIT.md), implementing

| 项 | 值 |
|---|---|
| Issue | https://github.com/go-git/go-git/issues/1518 |
| Tier | 高活跃高Star (7.7k stars, commits daily, human maintainers pjbgf / aymanbagabas / hiddeco) |
| Labels | good first issue, help wanted, tech debt |
| Status | open, no assignee, no linked PR |
| Duplicate-PR check | (pending) |

## Notes so far
- Issue by mhagger (2025-04-14) proposes splitting `remote.go` into `remote.go` / `remote_fetch.go` / `remote_push.go` (+ tests). pjbgf & aymanbagabas approved. mhagger said he'd do it after #1512; never did. Bot auto-closed 2025-11-18, pjbgf reopened same day and added `good first issue` + `help wanted` → open to anyone.
- AI policy: `AI_POLICY.md` allows AI assistance; human accountable; disclose in PR; commits must carry an `Assisted-by:` trailer (see 需要提交者注意).
