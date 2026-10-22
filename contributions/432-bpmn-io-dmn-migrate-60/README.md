# 432 — bpmn-io/dmn-migrate#60: migrate typeRefs of imported types when migrating 1.1→1.3

| Item | Details |
|---|---|
| Issue | https://github.com/bpmn-io/dmn-migrate/issues/60 |
| Tier | Free / high-profile (bpmn.io / Camunda ecosystem) |
| Labels | backlog, pr welcome. barmac (maintainer) said contributions are welcome; nikku questioned the need for the extra error, which this patch does not implement. |
| Base branch | `main` (patch built on 5fb8357) |
| Status | Independent review done (see below); ready to submit |
| Duplicate check | 2026-10-22: no open PR, issue unassigned. Closed unmerged PR #61 (kilisamemarisaaa, 2026-09-07/08) took the same approach and was closed because its author could not sign the CLA; the author invited others to reuse the work. The PR body credits #61. |
| AI policy | None |
| CLA/DCO | **CLA required** (bpmn-io uses CLA assistant, signed with a GitHub login). Sign it when the bot comments on the PR. |

## Change
- `migrateImports`: an unnamed import is named after the xmlns prefix bound to its namespace. Every `typeRef` that uses that prefix is rewritten from `prefix:Local` to `prefix.Local`.
- Prefixes containing `-` or `.` are skipped (they would make `prefix.Type` ambiguous in FEEL; one of the Copilot points on #61). Those imports keep the ID-based name and their typeRefs stay unchanged.
- New fixture `test/fixtures/imported-types.dmn` and 6 new specs in an `imports` describe block.

## Verification
- Red: without the fix (src reverted and dist rebuilt; specs import the built dist), the new specs for import naming, typeRef migration and the FEEL-name guard fail.
- Green: `npm run all` passes: lint, build, 20 passing (1 pending), and distro 2 passing.
- The migrated output passes XSD validation against DMN 1.3.

## How to submit
The PR body follows the bpmn-io PR template. Do not change the template headers or the checklist; the PR quality check enforces them.
```
git clone https://github.com/bpmn-io/dmn-migrate && cd dmn-migrate && git checkout -b migrate-imported-typerefs origin/main
git am --keep-cr /path/to/0001-*.patch   # --keep-cr is required: src and spec files use CRLF
```

## 独立复核
- 复核人：独立 agent，2026-10-22。在全新 clone 上 `git am --keep-cr` 干净应用，CRLF 保留；`npm ci && npm run all` 通过；红→绿复现；边界情况（无 import、无前缀、非 import 前缀、已命名 import、嵌套 typeRef、`t:B:C`）均正确，迁移结果通过 DMN 1.3 XSD。
- 首轮指出的文档问题已改：CLA 实际需要签；查重补记已关闭的 PR #61；`git am` 需 `--keep-cr`。同时按 #61 上 Copilot 的意见加了 FEEL 名字防护（含 `-`/`.` 的前缀不改写）并补测试，复跑 `npm run all` 通过、红→绿成立。
- 已知不处理：只看根元素上的 xmlns 声明（子元素重声明同一前缀极少见），PR 正文已说明。
- 结论：PASS
