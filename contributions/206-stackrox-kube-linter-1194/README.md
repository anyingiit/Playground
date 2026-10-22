# stackrox/kube-linter#1194 — Allow to disable sorted-keys for labels and annotations

| 项 | 值 |
|---|---|
| Issue | https://github.com/stackrox/kube-linter/issues/1194 |
| Tier | 高活跃高Star |
| Labels | 无（未打标签的 feature request，维护者未回复） |
| Status | ✅ ready — patch + PR text done, red→green verified (2026-10-22) |
| 重复 PR 检查 | 2026-10-22：issue open、无指派、无评论；`gh pr list --search 1194` 无结果；`sorted-keys` 关键词只有原始实现 #1042（已合并）。owner 的 #1273（env-value-from）仍 open，与本改动无文件交集 |
| Base | `main` @ abea26c |

## 问题理解
`sorted-keys` 检查递归应用到所有 mapping，包括 `metadata.labels` / `metadata.annotations`。Helm chart 常用 `include` 渲染用户自定义标签，顺序不可控，用户希望能对 labels/annotations 关掉排序检查。

## 合理性判断（是否低设计风险）
- 模板已有参数机制（`internal/params/params.go` + `go generate` 生成 `gen-params.go` 和文档），加一个可选参数是现成模式；`danglingservice` 有类似的 `ignoredLabels []string`。
- 默认值为空 → 现有行为完全不变；只有自定义 check 显式配置才生效。
- 唯一的设计选择是匹配方式：选了最简单的"按 key 名精确匹配、任意层级"（`+noregex`、`+notnegatable`），这样一次配置就能覆盖 `metadata.labels` 和 `spec.template.metadata.labels`。PR 正文里说明可改为路径或正则匹配。
- 仓库无 AI 政策（CONTRIBUTING/.github/labels 均无相关规定；有个 `ai-review` 标签但无描述）。

## 改动
- `pkg/templates/sortedkeys/internal/params/params.go`：新增 `IgnoredKeys []string \`json:"ignoredKeys"\``；`gen-params.go` 由 `go generate` 重新生成。
- `pkg/templates/sortedkeys/template.go`：`checkNode` 改为 `checker` 方法（持有 recursive 和 ignoredKeys 集合）；递归子节点时跳过被忽略 key 的值。被忽略 key 本身在兄弟间的顺序仍检查。
- `template_test.go` + `testdata/unsorted-labels-annotations.yaml`：4 个新表驱动用例（不忽略 / 忽略两者 / 只忽略 annotations / 被忽略 key 本身仍参与排序）。
- `docs/generated/templates.md`：用构建出的二进制 `templates list --format markdown` 重新生成（`checks.md` 无变化）。
- Commit：`feat(sorted-keys): add ignoredKeys parameter`，作者 anyingiit <49945850+anyingiit@users.noreply.github.com>，正文 `Fixes #1194`。

## 验证
环境：go1.26.8（GOTOOLCHAIN，本机缓存），GOCACHE 在工作目录（仓库外）。
- RED（只还原 template.go，保留参数和测试）：`go test ./pkg/templates/sortedkeys/` → `labels_annotations_ignored`、`only_annotations_ignored` FAIL。
- GREEN：`go test ./pkg/templates/sortedkeys/...` → ok。
- `go test -p 3 ./pkg/... ./docs/...` → 全部 ok。
- `golangci-lint run ./pkg/templates/sortedkeys/...`（tool-imports 锁定版本）→ 0 issues。
- 手工：自定义 check `template: sorted-keys, params: {recursive: true, ignoredKeys: [labels, annotations]}` lint 新 testdata → 只剩 `containers[0]` 一条；内置 `--include sorted-keys` 仍报 5 条。
- 未跑：bats e2e（默认行为不变，内置 check 参数未改）。
- 备注：`gofmt -l` 会列出 `gen-params.go`，这是生成器模板本身的既有格式（原文件同样被列出），与本改动无关。

## 需要提交者注意
- 这是未打标签、无维护者回复的 feature request；参数名/匹配语义是设计选择，维护者可能要求改名或改为路径匹配。
- 仓库不要求 DCO/CLA，无 PR 模板、无 CHANGELOG；无 AI trailer 要求。
- 与 owner 已开的 #1273 无冲突（不同模板）。

## 如何提交
```bash
git clone https://github.com/anyingiit/kube-linter && cd kube-linter   # 先 fork
git remote add upstream https://github.com/stackrox/kube-linter.git && git fetch upstream
git checkout -b sorted-keys-ignored-keys upstream/main
git am /path/to/contributions/206-stackrox-kube-linter-1194/0001-*.patch
go test ./pkg/templates/sortedkeys/...
git push origin sorted-keys-ignored-keys
```
PR 标题：见 `pr_title.txt`；PR 正文：见 `pr_body.md`。

## 独立复核（2026-10-23）
- 上游复查：#1194 仍 open、无指派、无评论；无相关 PR（仅原实现 #1042 已合并）。
- 新浅克隆 main @ abea26c，`git am` 干净；作者 anyingiit。
- RED（仅还原 template.go）：`labels_annotations_ignored`、`only_annotations_ignored` FAIL；GREEN：`go test ./pkg/templates/sortedkeys/...` ok；`go test -p 4 ./pkg/... ./docs/...` 全 ok。
- `go generate ./pkg/templates/...` 与用构建出的二进制重生成 `docs/generated/{templates,checks}.md` 均无差异；`golangci-lint run ./pkg/templates/sortedkeys/...`（tool-imports 版本）0 issues；gofmt 只列出既有的 gen-params.go（全仓 65 个同类，既有）。
- 手工：自定义 check `ignoredKeys: [labels, annotations]` 只剩 containers[0] 一条；内置 sorted-keys 仍 5 条。
- 设计判断：纯增量可选参数、默认不变、与 `danglingservice.ignoredLabels` 同形，范围小，不算过度推测；风险仅在维护者可能偏好路径匹配（PR 已说明）。
- 修改：PR 正文删去 "CHANGELOG n/a" 勾选行（仓库无 PR 模板/CHANGELOG，此行是噪音）。补丁未改。
