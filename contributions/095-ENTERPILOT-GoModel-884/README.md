# ENTERPILOT/GoModel #884 — Write down the JSON library policy and fix the drift it already caused

| 项 | 值 |
|---|---|
| Issue | https://github.com/ENTERPILOT/GoModel/issues/884 |
| Tier | 新锐 |
| Labels | good first issue |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：`pulls?q=884` 只匹配到无关的 #423（virtual models，已合并）；按 "json helper" 关键词搜索也没有相关 PR。issue 无人分配，没有评论。 |
| Base | `main` @ 39c217e1（2026-09-29） |

## 问题理解
项目用了 goccy/go-json、encoding/json、gjson、yaml.v3 四个库，但选择规则没有写在任何地方，已经出现三处偏差：
1. `[]string` JSON 列的 encode/decode 有三份：`users/store_sql.go`（stdlib）、`virtualmodels/store.go`（goccy）、`storage/sqlutil`（goccy，可空版本）。
2. `server/messages_native.go` 的注释说用 stdlib 是因为需要 `InputOffset`，但 goccy 也有 `InputOffset`。
3. `auditlog/body.go` 同时用两个库却没解释。
issue 建议：写一个 ADR 或集中注释记录规则；把 store 里的 helper 合并到 sqlutil；修正注释。

## 合理性判断
- issue 由维护者提出，带 good first issue 标签，没有设计争议，建议的工作很具体。
- 第 3 点在 main 上已解决：`auditlog/body.go` 已有注释说明 stdlib `Valid` 是严格、无分配的扫描。所以只在 ADR 里引用它，没有改代码。
- 仓库已有 `docs/adr/0001…0013`，所以规则写成 ADR-0014。

## 改动
- 新增 `docs/adr/0014-json-libraries.md`：规则 + 目前 stdlib 站点的理由（pluginapi 只能依赖标准库、echo binder、config/merge.go 的严格解码、messages_native 的拼接、auditlog 的 Valid）+ sqlutil 两组 helper 的使用约定。
- `AGENTS.md` 加一行指向该 ADR。
- `internal/storage/sqlutil`：新增 `EncodeJSONStrings`（nil→`"[]"`，返回错误）和 `DecodeJSONStrings`（空/`[]`→nil，格式错误返回 error），与现有可空/容错的 `NullableJSONStrings`/`StringsFromJSON` 区分开。
- `users/store_sql.go` 删除 `encodeAllowedModels`/`decodeAllowedModels` 和 `encoding/json` 引用；`virtualmodels/store.go` 删除 `encodeUserPaths`/`decodeUserPaths`。调用处改为 sqlutil 的新函数，并在调用处包装错误，保留原来的 `encode allowed_models:` / `decode user_paths:` 等前缀。行为不变。
- `messages_native.go`：注释改为真实理由（拼接依赖 stdlib 文档化的 RawMessage 原始字节 + InputOffset 行为；goccy 虽然也有这两个 API，但这里只在 stdlib 下验证过，而且这条路径不是热点）。

## 验证（Go 1.27.1，GOFLAGS=-p=2）
- Red：恢复 base 的 `sqlutil.go`，只保留新测试：`go test ./internal/storage/sqlutil/ -run JSONStrings` → build failed（`undefined: EncodeJSONStrings / DecodeJSONStrings`）。
- Green：同一命令 `TestEncodeJSONStrings`、`TestDecodeJSONStrings`、`TestJSONStringsRoundTrip` 通过。
- `make frontend-stub` 后 `go test ./cmd/... ./config/... ./ext/... ./internal/... ./run/...`：全部 ok（等同 `make test`，没有加 -race/-v）。
- `gofmt -l ./internal ./cmd ./config`：无输出；`go vet`（sqlutil/users/virtualmodels/server）、`go build ./...`：通过。
- `golangci-lint` v2.13.1（Makefile 固定版本，用 `GOTOOLCHAIN=go1.27.1` 构建）`run --build-tags=swagger,e2e,integration,contract ./internal/storage/... ./internal/users/... ./internal/virtualmodels/... ./internal/server/...`：0 issues。
- **没有运行**：e2e/integration（需要 docker/mongo）、dashboard JS 测试、`npx mint validate`（ADR 不在 Mintlify 导航里，其他 ADR 也不在）、全仓 `make lint`（只 lint 了改动的包）。

## 独立复核（2026-10-01）
- 新的浅克隆（main @ 39c217e，与 base 相同）`git am` 干净应用；作者 anyingiit，无 commit body、无 trailer。
- Red/Green 复现：恢复 base `sqlutil.go` → build failed（undefined EncodeJSONStrings/DecodeJSONStrings）；恢复后 3 个新测试通过。
- `go build ./...`、`go vet`、`gofmt -l` 干净；全量单元测试通过；golangci-lint v2.13.1（用 go1.27.1 构建）对改动包 0 issues。注意：GOMODCACHE 不能放在仓库目录内，否则 `internal/testconventions` 会扫描到依赖源码而失败（与本 patch 无关）。
- 核对 issue 原文三项建议，均已覆盖；goccy v0.10.6 确有 `Decoder.Token`/`InputOffset`，新注释准确。
- 小差异：`users` 的 allowed_models 解码从 stdlib 变为 goccy，对 `[]string` 无实际行为差异。

## 需要提交者注意
- AI 政策：仓库允许 AI（CONTRIBUTING 说维护者自己也用 AI 工具），但 AGENTS.md/CLAUDE.md 要求：**不要写 AI co-author，不要在 PR/commit 里放 AI（Claude）链接，PR 描述保持简洁，没必要不写 commit body**。因此 patch 没有 commit body 和任何 trailer；pr_body.md 的 disclosure 段落改写成不带链接、不点名工具的版本。如需更严格，可以删掉 disclosure 段落。
- 用 `gh pr create` 时注意不要让工具自动追加 "Generated with Claude Code" 之类的链接。
- PR 模板只有 `## Description` 和可选的 `## AI Generated (optional)`；pr_body 用 chefs-pick 格式，Description 在最前，和模板兼容。
- 建议打标签 `release:internal`（如果你有权限；没有就交给维护者）。
- 不需要 DCO，没有 CHANGELOG。
- Greptile/CodeRabbit 会自动 review，需要关注评论。

## 如何提交
```bash
git clone https://github.com/ENTERPILOT/GoModel && cd GoModel
git checkout -b refactor/json-library-policy origin/main
git am /home/user/Playground/contributions/095-ENTERPILOT-GoModel-884/0001-refactor-document-JSON-library-policy-and-share-stri.patch
make frontend-stub && go test ./cmd/... ./config/... ./ext/... ./internal/... ./run/... && make lint
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/095-ENTERPILOT-GoModel-884 ENTERPILOT/GoModel main refactor/json-library-policy contributions/095-ENTERPILOT-GoModel-884/pr_title.txt contributions/095-ENTERPILOT-GoModel-884/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
