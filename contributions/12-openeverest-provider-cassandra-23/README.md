# openeverest/provider-cassandra#23: softPodAntiAffinity for dev/test clusters

Status: ✅ ready to submit (patch + PR text done; submitter must add DCO sign-off)

| Item | Value |
|---|---|
| Issue | https://github.com/openeverest/provider-cassandra/issues/23 |
| Tier | 新锐 |
| Labels | area/topology, enhancement, good first issue, roadmap (milestone 0.2) |
| Status | open, no assignee, no comments (opened 2026-09-24 by maintainer @spron-in) |
| Duplicate-PR check | Open PRs are #28 "Test/lifecycle e2e" and #14 "Update Backup CR related change". Neither touches anti-affinity. No PR references #23. |
| Base branch | `main` @ `b6ffbbf` |

## 为什么属于「新锐」

- OpenEverest v2 生态（Percona Everest 的后继项目）中的 Apache Cassandra provider，基于 k8ssandra-operator。仓库 Star 很少，但项目本身有实际价值。
- 有真人维护：Sergey Pronin（@spron-in）负责 review 并合并 PR；外部贡献者 @huynt0812 的 PR #5/#6/#7/#10/#11/#13 在 8–9 月陆续合并；#17 于 2026-09-24 合并；#28 于当天开启。
- 这个 issue 是维护者当天从 ROADMAP 0.2 拆出来、标了 `good first issue` 的任务，不是自动生成的 issue farm。

## 需要提交者注意

- **必须 DCO**：OpenEverest 的 CONTRIBUTING 要求每个 commit 都带 `Signed-off-by`。patch 里**没有**加，请用 `git am --signoff` 或 `git commit --amend -s` 加上你自己的 sign-off。
- **AI 政策**（openeverest/openeverest CONTRIBUTING「AI-assisted contributions」）：允许使用 AI，条件有三：(1) 提交者本人要理解改动，能在 review 里为它辩护；(2) 不能把没有实际观察到的输出当作观察结果；(3) 如果改动主要由 AI 生成，需要说明。PR 正文已包含披露段，并明确写了**没有**在真实 k3d 集群上跑验收标准。review 前请先读懂下文「改动」一节。
- provider 仓库本身没有 CONTRIBUTING、AGENTS.md 或 PR 模板。commit 风格是 Conventional Commits（`feat:` / `fix:`）。

## 问题理解

cass-operator 默认每个 Kubernetes 节点只调度一个 Cassandra pod，所以 3 副本的 Instance 在单节点 k3d/kind 上永远到不了 Ready。issue 提出的方案：
1. 在 `CassandraParameters` 上加可选布尔字段 `softPodAntiAffinity`；
2. 映射到 K8ssandraCluster 的 softPodAntiAffinity 字段；
3. 在 UI 的 Advanced 区展示，并附带生产环境警告；
4. 运行 `make generate`。

验收标准：打开开关后 3 节点 Instance 在单节点 k3d 上能到 Ready；默认行为不变。

## 合理性判断

需求合理：issue 属于 ROADMAP 0.2，由维护者提出，也符合现有模式（#13 heap size 走的是同一路径：parameters → provider.go → UI Advanced）。阅读上游代码时发现 3 个坑，issue 里没有提到，不处理的话验收标准达不到：

1. **k8ssandra-operator webhook**：如果 DC 级别设置了 `softPodAntiAffinity=true`，要求 DC 级别的 `Resources` 非空（`ErrNoResourcesSet`）。本 provider 的 resources 设在 cluster 级别，所以照 issue 字面写到 `datacenters[]` 会被拒绝。**改为设在 cluster 级 `DatacenterOptions`**，k8ssandra-operator 的 `MergeCRs` 会把它合并进 DC，最终得到 `AllowMultipleNodesPerWorker`。
2. **cass-operator webhook**：`allowMultipleNodesPerWorker` 要求 cpu 和 memory 的 requests、limits 四项都非零。但 UI 只设置 limits，默认资源不设 cpu limit，示例文件只设置 requests。因此开启后按 Kubernetes 语义补全：缺 request 用 limit 补，缺 limit 用 request 补（0 视为缺失）。两者都没有的资源在 Validate 阶段直接报错。
3. **cass-operator webhook 禁止修改 `allowMultipleNodesPerWorker`**：已有集群一旦切换，之后每次 apply 都会被拒，reconcile 会静默卡住（provider 里 DC 改名的注释描述过同一类问题）。因此在 Sync 中对比 live 值，不一致就返回明确错误；UI 开关在 edit/restore 模式下禁用（同 storageClass）。

## 改动（commit `feat: allow soft pod anti-affinity for dev and test clusters`）

- `definition/components/types.go`：新增 `SoftPodAntiAffinity bool` 字段（`omitempty`），附文档注释。
- `internal/provider/provider.go`：
  - 抽出 `decodeEngineParameters`，`resolveJvmOptions` 改为复用它。
  - 新增 `resolveSoftPodAntiAffinity(enabled, existing)`：开启时返回 `ptr.To(true)`，关闭时返回 nil，即字段完全不出现，默认输出与之前逐字节一致。live 集群上的值被修改时报错。
  - 新增 `softPodAntiAffinityResources`：对 resources 做 DeepCopy 后补全，不修改调用方的对象。
  - `Validate`：开启且显式给了 resources 时，缺 cpu 或 memory 就报错。
  - `buildCassandra`：在 cluster 级 `DatacenterOptions` 上设置 `SoftPodAntiAffinity`，并使用补全后的 resources。
- `definition/topologies/singleDatacenter/topology.yaml`：Advanced 区新增 `uiType: toggle`（openeverest `release-2.0`/`main` 的 UI generator 支持该类型），带 `helperText` 生产警告，edit/restore 下禁用；更新 `componentsOrder`。
- `charts/provider-cassandra/generated/provider-spec.yaml`：由 `make generate` 重新生成。
- `README.md` 参数表新增一行；`examples/instance-example.yaml` 增加注释示例。
- `internal/provider/provider_test.go`：新增 `TestSoftPodAntiAffinityResources`（7 例）、`TestResolveSoftPodAntiAffinity`（7 例）、`TestBuildCassandraSoftPodAntiAffinity`（3 例，fake client 端到端），`TestValidate` 新增 3 例。

## 验证

环境：go1.26.4（GOTOOLCHAIN=auto），私有 GOMODCACHE/GOCACHE。

| 命令 | 结果 |
|---|---|
| 先写测试，再在未改实现的代码上跑 `go test ./internal/provider/` | 🔴 FAIL：编译失败，`undefined: softPodAntiAffinityResources` / `undefined: resolveSoftPodAntiAffinity` |
| 实现后 `go test ./internal/provider/` | 🟢 `ok … internal/provider` |
| `make test-unit`（`go test -race ./... -coverprofile cover.out`，与 CI 相同） | 🟢 `ok … internal/provider 2.604s coverage: 59.9%` |
| `go build -o /dev/null ./cmd/provider`（CI Build job） | 🟢 ok |
| `make lint`（golangci-lint v2.11.3，与 CI 版本一致；使用官方 release 二进制，sha256 已校验） | 🟢 `0 issues.` |
| `make verify`（CI 的 generated-files 检查） | 🟢 `Generated files are up-to-date.` |
| `go vet ./...` | 🟢 ok |
| `gofmt -l internal` | 干净。`definition/topologies/singleDatacenter/types.go` 在 base 上本来就没 gofmt，未改动 |

**未运行**：`helm lint`（本机没有 helm，本次也没改 chart 模板，只改了 generated spec）；chainsaw 集成测试和 k3d 上的 3 节点 Ready 验收（需要 docker/k3d + OpenEverest 控制器镜像，本环境不具备）。验收标准的依据是阅读 k8ssandra-operator v1.32.7 和 cass-operator v1.31.0 的 webhook 与 `MergeCRs` 代码得出的推断，PR 中已如实说明。

## 如何提交

```bash
git clone https://github.com/<you>/provider-cassandra && cd provider-cassandra   # fork of openeverest/provider-cassandra
git checkout -b feat/soft-pod-anti-affinity origin/main
git am --signoff /path/to/0001-feat-allow-soft-pod-anti-affinity-for-dev-and-test-c.patch   # --signoff = DCO
make test-unit && make verify
git push -u origin feat/soft-pod-anti-affinity   # then open PR against openeverest/provider-cassandra:main
```

---

## PR title

feat: allow soft pod anti-affinity for dev and test clusters

## PR body

```markdown
## Description

Adds an optional `softPodAntiAffinity` boolean to the engine component's parameters (`CassandraParameters`) so a multi-replica Instance can run on a single-node dev/test cluster (k3d, kind). It maps to k8ssandra-operator's `softPodAntiAffinity`, which becomes cass-operator's `allowMultipleNodesPerWorker`. When the field is left unset it is omitted entirely, so defaults and existing clusters are unchanged.

While reading the upstream webhooks I found three things the issue doesn't mention. Each of them would otherwise stop the cluster from ever reaching Ready:

1. **Placement.** The issue suggests `datacenters[].softPodAntiAffinity`. However, k8ssandra-operator's webhook rejects a datacenter-level `softPodAntiAffinity: true` unless `resources` are also set on that datacenter (`ErrNoResourcesSet`), and this provider sets resources at the cluster level. So the field goes on the cluster-level `DatacenterOptions`, next to `Resources`. k8ssandra-operator merges it into the datacenter (`MergeCRs` → `dcConfig.SoftPodAntiAffinity`).
2. **Resources.** cass-operator's webhook rejects `allowMultipleNodesPerWorker` unless cpu **and** memory have both a request and a limit. The UI only sets `limits`, `defaultEngineResources()` leaves CPU unlimited, and `examples/instance-example.yaml` only sets `requests`. When the option is on, `softPodAntiAffinityResources` returns a copy where a missing (or zero) request is filled from its limit and vice versa. A resource with neither is rejected in `Validate` with a clear error.
3. **Immutability.** cass-operator rejects any change to `allowMultipleNodesPerWorker` on an existing datacenter. If the flag were toggled on a live cluster, every later apply would be refused by the webhook. `resolveSoftPodAntiAffinity` compares against the live K8ssandraCluster and fails `Sync` with `"engine" softPodAntiAffinity cannot be changed after the instance is created`. The UI toggle is disabled in edit/restore mode, the same as `storageClass`.

UI: a `toggle` field in the Advanced section, with a production warning in `helperText`. The provider spec is regenerated with `make generate`. I also added a README parameter-table row and a commented example in `examples/instance-example.yaml`.

`decodeEngineParameters` was extracted from `resolveJvmOptions`, so both parameters share the same decoding.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

**What I did not run:** I did not have a k3d cluster with the OpenEverest controller, so I have **not** observed a 3-node Instance reaching `Ready` on single-node k3d, and I did not run the chainsaw integration suite. Points 1–3 come from reading the k8ssandra-operator v1.32.7 and cass-operator v1.31.0 webhook and merge code pinned in `go.mod`, not from an observed run. A quick check on `make dev-up` with `softPodAntiAffinity: true` would be very welcome.

## Related issue

Closes #23

## Checklist

- [x] Tests pass locally: `make test-unit` → `ok github.com/openeverest/provider-cassandra/internal/provider` (new `TestSoftPodAntiAffinityResources`, `TestResolveSoftPodAntiAffinity`, `TestBuildCassandraSoftPodAntiAffinity`, 3 new `TestValidate` cases; before the implementation they fail to compile); `make lint` (golangci-lint v2.11.3) → `0 issues.`; `make verify` → `Generated files are up-to-date.`; `go build ./cmd/provider` → ok
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog (release notes are generated from PRs)
- [x] Documentation is updated (if applicable) — README parameter table, `examples/instance-example.yaml`, field doc comment, UI helper text
```
