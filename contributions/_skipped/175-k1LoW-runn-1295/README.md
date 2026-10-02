# k1LoW/runn #1295 — OpenAPI readOnly/writeOnly validation

| 项 | 值 |
|---|---|
| Issue | https://github.com/k1LoW/runn/issues/1295 |
| Tier | 自由 |
| Labels | bug, pull request wanted |
| Status | ⏭ skipped — 已在 main 上修复（依赖升级），无需代码改动 |
| 重复 PR 检查 | 2026-10-01: /pulls?q=1295 无结果；无 assignee、无评论 |

## 问题理解
同一个 `User` schema 同时用于 POST 请求体和 200 响应体，`id` 为 readOnly、`name` 为 writeOnly，二者都在 `required` 中。
旧版本校验响应 `{"id":"123"}` 时报 `missing property 'name'`（没有按方向忽略 writeOnly 的 required）。

## 结论（为何跳过）
- runn main @ 651af61（2026-09-28）依赖 `github.com/pb33f/libopenapi-validator v0.14.0`，该版本新增
  `schema_validation/directional_schema.go`：请求体会从 required 中剔除 readOnly 属性，响应体剔除 writeOnly 属性。
- 用 issue 中的 schema 写了临时复现测试（请求 `{"name":"alice"}`、响应 `{"id":"123"}`），在 main 上
  `go test -run TestZZRepro -count=1 -v .` → **PASS**。即问题已由依赖升级修复（PR 搜索 "writeonly" 命中的是 dependabot 依赖升级 PR，如 #1482）。
- 因无法做出 red→green 的代码修复，按 brief 跳过。可选：owner 可在 issue 下留言告知已在 v1.11.x 修复，建议关闭；
  或者另提一个仅添加回归测试的 PR（未准备，价值有限）。

## AI 政策
仓库无 CONTRIBUTING / AGENTS 规则，标签描述也未限制 AI。
