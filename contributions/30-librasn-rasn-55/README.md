# librasn/rasn#55 — X9CM hold-instruction OIDs are under the wrong root (and have a typo arc)

| Field | Value |
|---|---|
| Issue | https://github.com/librasn/rasn/issues/55 |
| Tier | 新锐 |
| Labels | area/standard, area/types, good first issue, help wanted, kind/bug |
| Status | 🚧 in progress — audit done (benign), fix implemented, running tests |

Notes: `src/types/oid.rs` still defines `JOINT_ISO_ITU_T_MEMBER_BODY_US_X9CM_HOLD_INSTRUCTION*` as
`2.2.840.100400.2.x`; correct OIDs (RFC 5280 errata / oidref) are `1.2.840.10040.2.x` (root ISO, arc 10040 not 100400).
