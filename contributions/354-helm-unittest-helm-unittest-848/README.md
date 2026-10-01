# helm-unittest/helm-unittest#848

| 项 | 值 |
|---|---|
| Issue | https://github.com/helm-unittest/helm-unittest/issues/848 — Duplicate map keys in values files rejected by strict YAML parser, but accepted by real Helm |
| Tier | 自由 |
| Labels | 无 |
| Status | ✅ ready — patch + PR 文本已完成，red→green 已验证 |
| 重复 PR 检查 | 2026-10-01：`/pulls?q=848` 0 结果；`/pulls?q=is:pr duplicate` 无相关 PR；issue 无评论、无 assignee |
| Base | `main` @ 0d79286 |

## 问题理解
测试套件 `values:` 列表（以及 `--values` 参数）里的 values 文件用 yaml.v3 严格模式解析，同一层出现重复 key 会直接报错 `mapping key ... already defined`；而真实 Helm 用 sigs.k8s.io/yaml 解析，接受重复 key，后者覆盖前者。导致 helm 能渲染的 chart 在 helm-unittest 中无法测试。

## 合理性判断
Issue 合理：helm-unittest 的目标是模拟 helm 渲染，values 解析行为应与 Helm 一致。仓库无 AI 贡献禁令（grep AGENTS/CLAUDE/CONTRIBUTING/.github 无相关条款），无 DCO 要求，无 PR 模板。

## 改动
- `internal/common/utilities.go`：新增 `YmlUnmarshalValues`：先解析为 yaml.v3 `Node`（解析 Node 时不做重复 key 检查），递归删除 mapping 中重复 key 的较早出现（比较方式同 yaml.v3 的 Kind+Value），再 `node.Decode`。空文档直接返回。
- `pkg/unittest/test_job.go` (`getUserValues`) 与 `pkg/unittest/test_runner.go`（values 文件加载）改用该函数。其余地方（测试套件文件、snapshot）仍保持严格解析。
- 没有直接换成 sigs.k8s.io/yaml：那会把整数变成 float64 等，可能改变现有用户测试结果，风险更大。
- 测试：`TestV4RunJobWithValuesFileContainingDuplicateKeys`（pkg/unittest）、`TestYmlUnmarshalValuesWithDuplicateKeys` / `TestYmlUnmarshalValuesEmptyAndInvalid`（internal/common）。
- CHANGELOG 由维护者发版时编写，未改。

## 验证
环境：Go 1.26.0，`GOCACHE`/`GOPATH` 放在 /home/user/work 下（已清理）。
- Red（仅加测试、无修复）：`go test ./pkg/unittest/ -run TestV4RunJobWithValuesFileContainingDuplicateKeys` → FAIL，`line 2: mapping key "nameOverride" already defined at line 1`
- Green：同一命令 PASS；`go test ./internal/common/` ok
- `gofmt -l -s .` 无输出；`go vet ./internal/common/ ./pkg/unittest/` 通过
- `go test -p 2 ./...`：全部 ok，除 `TestV4RunnerOkWithPostRenderer`、`TestV3RunnerWith_Fixture_Chart_PostRenderer` —— 在未修改的 main 上同样失败（本机 `yq` 是 Python 版，不是 mikefarah/yq），与本改动无关
- `golangci-lint`（Makefile `go-lint`）本机无法运行：本地二进制用 go1.25 构建，低于仓库要求的 1.26；CI（go.yml）不跑 golangci-lint

## 需要提交者注意
- 无 DCO、无 AI trailer 要求；commit 作者为 anyingiit（noreply 邮箱），未加 Signed-off-by。
- PR body 中已包含 AI 辅助披露段落。
- 若 CI 的 SonarCloud 有意见，可能是关于新函数的复杂度，按需调整。

## 如何提交
```bash
git clone https://github.com/anyingiit/helm-unittest.git && cd helm-unittest   # 先 fork
git remote add upstream https://github.com/helm-unittest/helm-unittest.git && git fetch upstream
git checkout -b fix/values-duplicate-keys upstream/main
git am /path/to/contributions/354-helm-unittest-helm-unittest-848/0001-*.patch
go test ./pkg/unittest/... ./internal/common/...
git push origin fix/values-duplicate-keys
```
或使用脚本：
```bash
tools/submit_pr.sh contributions/354-helm-unittest-helm-unittest-848 helm-unittest/helm-unittest main fix/values-duplicate-keys contributions/354-helm-unittest-helm-unittest-848/pr_title.txt contributions/354-helm-unittest-helm-unittest-848/pr_body.md
```

PR 标题：见 `pr_title.txt`；PR 正文：见 `pr_body.md`。
