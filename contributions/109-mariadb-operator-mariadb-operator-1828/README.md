# mariadb-operator/mariadb-operator #1828 — [Feature] Ability to disable service monitor

| 项 | 值 |
|---|---|
| Issue | https://github.com/mariadb-operator/mariadb-operator/issues/1828 |
| Tier | 自由 |
| Labels | feature, good first issue, help wanted |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue open、无 assignee、无评论、无关联 PR；`pulls?q=1828` 0 结果；`serviceMonitor`/`metrics` 关键词检索无相关 open PR；anyingiit 在该仓库 0 个 PR。 |
| Base | `main` @ b04f95f3（2026-09-24） |

## 问题理解
`spec.metrics.enabled: true` 时 operator 总是创建 `ServiceMonitor`；Prometheus 在另一个集群、本集群没有 ServiceMonitor CRD 时，metrics 协调失败。issue 请求在 CRD 上加 `metrics.serviceMonitor.enabled`，以便只部署 exporter 而不建 ServiceMonitor。

## 合理性判断
- 维护者打了 feature + good first issue + help wanted，字段名已在 issue 中给出，无需先讨论设计。
- AGENTS.md 明确欢迎 AI agent，并给出完整开发流程。

- 字段放在共享的 `ServiceMonitor` 结构体上，因此 MaxScale CRD 也会有这个字段，两个 controller 都按它处理，保证行为一致。

## 改动
- `api/v1alpha1/mariadb_types.go`：`ServiceMonitor` 新增 `Enabled *bool`（`json:"enabled,omitempty"`）。为 nil 时视为 true，保持向后兼容。新增 `ServiceMonitor.IsEnabled()` 和 `MariaDB.IsServiceMonitorEnabled()`（= metrics 已启用且 ServiceMonitor 已启用）。
- `api/v1alpha1/maxscale_types.go`：新增 `MaxScale.IsServiceMonitorEnabled()`。
- `internal/controller/mariadb_controller_metrics.go`、`maxscale_controller_metrics.go`：ServiceMonitor 被禁用时，跳过 `Discovery.ServiceMonitorExist()` 检查和 `reconcileServiceMonitor`。exporter 的 config、Deployment、Service 照常协调。
- `docs/metrics.md`：在 ServiceMonitor 一节补充说明和 yaml 示例，并说明 MaxScale 同样适用。
- 生成文件（通过 make 重新生成，没有手改）：`zz_generated.deepcopy.go`、`config/crd/bases/*mariadbs*`/`*maxscales*`、`deploy/crds/crds.yaml`、`deploy/charts/mariadb-operator-crds/templates/crds.yaml`、`docs/api_reference.md`。
- 测试：`api/v1alpha1/mariadb_types_test.go`、`maxscale_types_test.go` 各新增一个 `IsServiceMonitorEnabled` DescribeTable，每个 5 个 Entry。

## 验证（go1.27.0，GOFLAGS=-p=2）
- 代码生成：`make manifests code manifests-crds helm-crds docs-api`，产物只有上面列出的文件。`make crd-size` 的结果是 784 KB，低于 900 KB 上限。
  - 没有跑完整的 `make gen`：VERSION=26.10.1 不是 dev 版本，会额外执行 embed-entrypoint、helm-docs、examples、docs-docker。这些步骤与本改动无关，而且需要访问外网、可能带来无关 diff。CI 的 Artifacts job 会比对生成结果，提交者可以在本地跑一次 `make gen`，确认没有新的 diff。
- Red：
  1. 只保留测试、还原 API 类型改动后执行 `make test KUBEBUILDER_ASSETS=<envtest 1.36.2> TEST_ARGS='--focus=IsServiceMonitorEnabled'`，结果是编译失败（`unknown field Enabled in struct literal of type ServiceMonitor`，`IsServiceMonitorEnabled undefined`）。
  2. 语义层面的 red：保留字段，把 `IsServiceMonitorEnabled()` 临时改成 `return m.AreMetricsEnabled()`（相当于修复前 controller 的判定），再执行同一命令。结果 `8 Passed | 2 Failed`，失败的是 MariaDB 和 MaxScale 的 `metrics enabled, serviceMonitor.enabled false` 两条。
- Green：恢复实现后执行 `PATH=$PWD/bin:$PATH make test KUBEBUILDER_ASSETS=$PWD/bin/k8s/k8s/1.36.2-linux-amd64`，37 个 suite 全部通过（API Suite 184/184，Webhook Suite 222/222）。
  - 注意：helmtest 需要 `helm` 在 PATH 里。不加 `bin/` 时，helmtest 会因为 `exec: "helm": executable file not found` 失败。这是环境问题，与改动无关。
- Lint：`GOTOOLCHAIN=go1.27.0 go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@v2.13.2`，然后运行 `golangci-lint run ./...`，结果 0 issues。（用 go1.26 构建的 golangci-lint 会报 "Go language version lower than targeted 1.27.0"，所以必须用 1.27 构建。）
- `go build ./...` 和 `go vet ./api/... ./internal/controller/...` 都通过。
- **没有运行**：`make test-int-basic` 等集成测试，因为它们需要 KIND、MetalLB 和 `make net`。controller 的改动只有在两处调用外加 if 判断，已经通过编译、vet 和 lint 覆盖。

## 需要提交者注意
- 把 `enabled` 从 true 改成 false 时，不会删除已经创建的 ServiceMonitor（与 `metrics.enabled: false` 的现有行为一致；MariaDB 被删除时它仍会被级联回收）。PR 正文已说明，并表示维护者需要的话可以补清理逻辑。
- 仓库没有 PR 模板、DCO、CLA、changelog，也不要求 AI trailer。AGENTS.md 对 AI 友好。
- 提交前建议在本地跑一次 `make gen && git diff --exit-code`，确认没有其他生成文件需要更新。
- commit 标题沿用仓库常见的祈使句风格（浅克隆里只能看到最近 1 个 commit，没法核对更多历史）。

## 独立复核（2026-10-01）
- `git apply --check` 到干净的 `main`@b04f95f：通过；patch 作者 `anyingiit <49945850+anyingiit@users.noreply.github.com>`，无 AI 模型名。
- 复现 red→green：`KUBEBUILDER_ASSETS=<envtest 1.36.2> go test ./api/v1alpha1/ -count=1 -ginkgo.focus=IsServiceMonitorEnabled`，修复后 10/10 通过；把 `ServiceMonitor.IsEnabled()` 临时改为 `return true`（即忽略新字段）后 `8 Passed | 2 Failed`（MariaDB/MaxScale 的 `serviceMonitor.enabled false`），还原后再次通过。
- 重新执行 `make manifests code manifests-crds helm-crds docs-api`：工作区无 diff，生成文件与提交一致。`gofmt -l` 对改动文件无输出（仅既有的 `pkg/builder/pod_builder.go` 与本改动无关）；`go vet ./api/... ./internal/controller/` 通过。
- 确认 controller 未对 `ServiceMonitor` 做 `Owns()`/watch，CRD 缺失时 `enabled: false` 路径不会因 informer 失败。
- 重复 PR 复查：issue 仍 open、无评论/assignee；`pulls?q=servicemonitor` 无相关 open PR。
- 结论：无需修改，保持 ✅ ready。

## 如何提交
```bash
git clone https://github.com/mariadb-operator/mariadb-operator && cd mariadb-operator
git checkout -b feat/servicemonitor-enabled origin/main
git am /home/user/Playground/contributions/109-mariadb-operator-mariadb-operator-1828/0001-Add-metrics.serviceMonitor.enabled-to-allow-skipping.patch
make gen && git diff --exit-code && make lint && make test
git push -u <your-fork> feat/servicemonitor-enabled
```
或者：
```bash
tools/submit_pr.sh contributions/109-mariadb-operator-mariadb-operator-1828 mariadb-operator/mariadb-operator main feat/servicemonitor-enabled contributions/109-mariadb-operator-mariadb-operator-1828/pr_title.txt contributions/109-mariadb-operator-mariadb-operator-1828/pr_body.md
```
本地工作副本：`/home/user/work/mariadb-operator`（分支 `feat/servicemonitor-enabled`，commit 9e2ce9f）。

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
