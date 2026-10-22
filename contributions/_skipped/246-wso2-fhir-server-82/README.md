# wso2/fhir-server#82 — `Patient?name=` search returns no results

| 项 | 值 |
|---|---|
| Issue | https://github.com/wso2/fhir-server/issues/82 |
| Tier | 新锐（WSO2） |
| Status | ⏭️ skipped — 已有竞争 PR #89 "fix(index): index HumanName/Address text parts for string search params"（open） |

## 记录
- 根因已确认：`internal/index/extractor.go` 的 `appendString` 对 HumanName/Address 用 `fmt.Sprintf("%v")`，索引成 `map[family:Reyes given:[Daniel]]`，所以只有 `:contains` 能命中。
- 本地用 PG16 + 服务端二进制端到端复现并验证了修复（name=reyes/Daniel/rey、:exact=Reyes、address=spring 修复前 0、修复后 1），但开 PR 前查重发现 #89 已在做同一件事，放弃。
- 教训：查重要在动手前做（这次先实现后查重，浪费约 20 分钟）。
