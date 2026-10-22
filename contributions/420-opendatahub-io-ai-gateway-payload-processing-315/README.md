# 420 — opendatahub-io/ai-gateway-payload-processing#315: 合并 model_store_test.go 到 store_test.go

| 项 | 内容 |
|---|---|
| Issue | https://github.com/opendatahub-io/ai-gateway-payload-processing/issues/315 |
| 层级 | 自由（Red Hat OpenDataHub 组织，活跃：每天多个合并） |
| Labels | good first issue（维护者 yossiovadia 本人开的 issue 并打标签） |
| Base 分支 | `main`（补丁基于 91dc39e） |
| 状态 | ✅ 可提交 |
| 重复检查 | 2026-10-22：issue 无评论、无指派、无关联 PR；/pulls 搜 model_store_test 只有已合并的 #288/#308 |
| AI 政策 | 仓库无 CONTRIBUTING / AI 条款（其他 .md 里的 LLM 字样是产品内容） |
| CLA/DCO | 近 20 个提交有 34 行 Signed-off-by，按 DCO 习惯已加 `Signed-off-by: anyingiit`（owner 授权可代签） |

## 问题理解
#288/#308 把 provider store 和 model store 合并成 store.go 里的一个 infoStore，测试还分在两个文件。维护者要求合并测试文件，低优先级、无功能影响。

## 改动
把 4 个 `TestModelStore_*` 原样移到 `store_test.go` 末尾，补 `common/provider` import，删除 `model_store_test.go`。

## 验证
纯测试文件重排，没有红→绿可做；改为验证"测试集合不变且全部通过"：
- `go test -count=1 -list '.*' ./pkg/plugins/model-provider-resolver/`：改前 74、改后 74。
- `go test -count=1 ./pkg/plugins/model-provider-resolver/` ok；`go vet` 通过。
- `make lint`（golangci-lint，仓库 pinned 版本）：0 issues。
- `gofmt -l` 对新 store_test.go 无输出（该包其他 5 个文件在 Go 1.26 gofmt 下有既有差异，与本改动无关）。

## 需要提交者注意
- 提交信息为 Conventional Commits（`test:`），PR 标题同。仓库无 PR 模板。
- 价值不大但完全是维护者要求的清理，合并概率高。

## 如何提交
```
git clone https://github.com/opendatahub-io/ai-gateway-payload-processing && cd ai-gateway-payload-processing
git checkout -b test-merge-store-tests origin/main
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
- 全新 `git clone --depth 30`，origin/main 仍为 91dc39e；`git am` 补丁干净应用。
- 改动只涉及两个文件：删除 `model_store_test.go`，`store_test.go` 末尾追加 4 个 `TestModelStore_*`，并补一个 `common/provider` import。逐字比对函数体：与原文件完全一致，无其他改动。
- `go test -count=1 ./pkg/plugins/model-provider-resolver/` ok；`go vet` 通过；`gofmt -l store_test.go` 无输出；`make lint`（golangci-lint v2.9.0）0 issues（./bin 已删除）。
- `go test -list '.*'`：改前 74、改后 74，排序后的测试名集合完全相同。
- 重复检查：issue #315 仍 open，无评论、无指派、无关联 PR；`/pulls?q=315` 和 `?q=model_store` 没有相关 PR；11 个 open PR 中没有相关的（#486 只改 pkg/controller 等，不碰本包）。
- PR 文本：英文；前两行是 attribution 块；含 Motivation / disclosure 段落；#288（合并为 infoStore）、#308（Nir 的 review 提出拆分测试的问题）的引用与事实相符；"74 tests"、lint/vet 的说法均已复现。
- 复核用的克隆已删除。

结论：PASS
