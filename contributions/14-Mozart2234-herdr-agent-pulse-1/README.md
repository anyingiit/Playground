# Mozart2234/herdr-agent-pulse#1 — Singleton lock: pidfile unlink races with a starting daemon

| Item | Value |
|---|---|
| Issue | https://github.com/Mozart2234/herdr-agent-pulse/issues/1 |
| Tier | 自由 |
| Labels | bug, help wanted |
| Status | 🚧 in progress — audit done, implementing |
| Duplicate-PR check | no linked PRs / no comments (WebFetch 2026-09-24) |

## Notes
- Candidate choice: glassbox #970/#966 are "Stellar Wave" labelled (Drips wave issue-farm style, ~1000 issues); herdr-agent-pulse is a new human-authored repo, issue is a real concurrency bug with clear acceptance criteria.
