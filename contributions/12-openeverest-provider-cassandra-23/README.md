# openeverest/provider-cassandra#23 — softPodAntiAffinity for dev/test clusters

Status: 🚧 in progress — implementing (audit done)

| Item | Value |
|---|---|
| Issue | https://github.com/openeverest/provider-cassandra/issues/23 |
| Tier | 新锐 |
| Labels | area/topology, enhancement, good first issue, roadmap (milestone 0.2) |
| Status | open, unassigned, no comments (opened 2026-09-24 by maintainer spron-in) |
| Duplicate-PR check | open PRs: #28 (lifecycle e2e), #14 (Backup CR) — none touch anti-affinity |

Notes so far:
- k8ssandra-operator webhook: dc-level softPodAntiAffinity requires dc-level Resources -> set it at cluster-level DatacenterOptions (merged into the DC) where resources live.
- cass-operator webhook: allowMultipleNodesPerWorker needs cpu+memory requests AND limits; field is immutable after creation.
