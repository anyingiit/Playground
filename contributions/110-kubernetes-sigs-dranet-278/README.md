# kubernetes-sigs/dranet #278 — Validate host-derived network configuration before checkpointing

| 项 | 值 |
|---|---|
| Issue | https://github.com/kubernetes-sigs/dranet/issues/278 |
| Tier | 自由 |
| Labels | help wanted, triage/accepted |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue 是 open 状态，没有 assignee，评论里没人认领，也没有关联 PR。用 pulls?q=278 和 validate 关键词都没搜到相关 PR。作者 OguzPastirmaci 有一个无关的 open PR #357（`--cloud-provider-options`），也改 cloudprovider 包，要注意冲突。 |
| Base | `main` @ 5553ccc7（2026-10-01） |

## 问题理解
dranet 在 NodePrepareResources 时读取 host 上的路由、规则和邻居，然后 checkpoint（SetDeviceConfig），之后由 NRI 在 Pod netns 里应用。OKE 上有一个 agent 异步配置路由，所以有可能 checkpoint 到不完整的路由集合，比如只有 policy table 的 local 路由，缺 connected 路由；NRI 应用时也不会报错。issue 的要求：
- 给 provider 提供一个可选（opt-in）的钩子，在 SetDeviceConfig 之前校验最终的 NetworkConfig；
- 校验失败时通过 PrepareResult.Err 返回，接口留在 host 上，让 kubelet 重试；
- 不实现这个钩子的 provider，行为保持不变；
- 钩子只读，不加 host 网络恢复、固定延迟或 policy table 编号假设（遵守 #42 的职责边界）。

## 合理性判断
- issue 已经 triage/accepted，并标了 help wanted。作者在 issue 里写了期望行为，实现方式（callback、capability 等）可以讨论。
- 仓库已有可选接口的写法：`ProfileProvider` 由 `inventory.DB` 持有，driver 通过 `inventoryDB` 接口调用。本改动按同样的模式实现，driver 不直接接触 provider。
- 只做通用钩子，不实现 OKE 的具体校验，也不加 webhook capability，避免越过 provider owner 的职责，也减少和 #357 的冲突。PR 里已说明。

## 改动
- `pkg/cloudprovider/cloud.go`：新增可选接口 `NetworkConfigValidator { ValidateNetworkConfig(id DeviceIdentifiers, config *apis.NetworkConfig) error }`，注释写明必须只读，以及出错后的效果。只是追加，不改动已有代码。
- `pkg/inventory/db.go`：新增 `DB.ValidateNetworkConfig(deviceName, config)`。它对 `db.instance` 做类型断言。provider 没实现接口（包括 nil）时返回 nil；设备不在 inventory 中时返回错误；其余情况用 `getDeviceIdentifiers` 生成 identifiers，再调用 provider。
- `pkg/driver/driver.go`：`inventoryDB` 接口增加 `ValidateNetworkConfig`。
- `pkg/driver/dra_hooks.go`：在 netdev 路径上，RDMA 配置之后、eBPF unpin 和 SetDeviceConfig 之前，调用校验并传入 `&deviceCfg.NetworkInterfaceConfigInPod`。失败时返回 `device %s: provider rejected the network configuration of interface %s: %w`。此时 deviceCommitted 仍为 false，所以 defer 会释放已分配的 profile。接口这时还没被移动（移动发生在 NRI 阶段），因此留在 host 上。IB-only 路径没有 host 路由，不做校验。
- 测试：
  - `pkg/driver/driver_test.go`：fake DB 增加 `ValidateNetworkConfigFunc` 和 `validateCalls`（gofmt 重新对齐了结构体字段）。
  - `pkg/driver/dra_hooks_test.go`：`TestPrepareResourceClaim` 新增 3 个 case：校验拿到最终配置并成功持久化；校验失败时报错且不持久化；校验失败时释放 profile。
  - `pkg/inventory/db_test.go`：新增 `TestValidateNetworkConfig`，覆盖 5 种情况：没有 provider、provider 没实现接口、校验通过（检查 identifiers 和 config 指针）、校验拒绝（errors.Is）、设备不在 inventory。

## 验证（Go 1.26.0，自动下载 toolchain）
- 环境限制：沙箱内核不支持创建 `dummy`/`ipvlan` link（netlink 返回 operation not supported），而且没有 `ip` 命令。因此 `TestPrepareResourceClaim` 等依赖 netlink 的测试在 base 上就会失败。为了跑新加的 driver case，我临时把测试文件里的 `"dummy0"` 换成 `"lo"`，并跳过 LinkAdd，只在本地验证；提交的测试文件没有这个改动。
- Red（临时去掉 dra_hooks.go 中的调用，并让 DB.ValidateNetworkConfig 直接 return nil）：
  - `CGO_ENABLED=1 go test -race -count 1 -p 2 -run 'TestPrepareResourceClaim$' -v ./pkg/driver/`：3 个新 case 失败（`ValidateNetworkConfig calls = 0, want 1`，以及 `error = <nil>, want error containing "provider rejected ..."`）。
  - `go test -count 1 -run TestValidateNetworkConfig -v ./pkg/inventory/`：accepts、rejects、device_not_in_inventory 3 个子测试失败。
- Green（恢复实现）：上面两条命令全部通过，TestPrepareResourceClaim 的 22 个 case 都通过（用的是 lo 版本）。
- 整包测试：`CGO_ENABLED=1 go test -race -count 1 -p 2 ./pkg/driver/... ./pkg/cloudprovider/... ./pkg/inventory/...`。base 和分支上都失败同样的 22 个顶层测试，全部依赖 netlink 创建 link 或真实网络，与本改动无关：TestAddLinkAttributesIP*、TestCreateSubinterfaceInNS_*、TestGetDefaultGwInterfaces、TestGetDeviceConfig、TestGetExcludedUplinkInterfaces、TestGetProfileConfig、TestIsLACPBond、TestPrepareResourceClaim、TestSubinterface_IPVlan*、Test_applyEthtoolConfig、Test_applyRoutingConfig、Test_nhNetdev、Test_nsAttach*/nsDetach*。cloudprovider/{aws,coreweave,discovery,gce,oke,webhook} 和 cloudprovider 根包都通过；alibaba 和 azure 在 base 上同样失败。
- `go build ./...`、`go vet ./...`、`gofmt -l pkg cmd`（无输出）：都通过。
- Lint：仓库的 hack/lint.sh 用 docker 跑 golangci-lint v2.9.0。本机只有 v2.5.0（用 go1.25 构建，无法加载 go1.26 项目），所以我用 `go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@v2.9.0` 装到 scratchpad，然后运行 `golangci-lint run --concurrency 2 ./...`，结果是 **0 issues**。
- patch 已在干净的 5553ccc worktree 上 `git am` 验证过，可以直接应用。

## 独立复审（2026-10-01）
- 重新核对 issue #278：仍为 open、无 assignee、无评论；`pulls?q=278` 没有相关 PR。
- 在干净的 5553ccc worktree 上 `git apply --check` 通过；patch 作者是 anyingiit，没有 AI 名称；patch 与分支 HEAD 的 `git format-patch -1` 一致。
- 亲自复现 red→green（同样把测试里的 `dummy0` 临时换成 `lo`，LinkAdd 失败只打日志）：恢复 base 的 `dra_hooks.go`/`db.go`（`DB.ValidateNetworkConfig` 换成直接 `return nil` 的桩）后，3 个新 driver case 和 inventory 的 accepts/rejects/device_not_in_inventory 失败；恢复实现后全部通过。`go vet ./pkg/...`、`gofmt -l pkg cmd` 都干净。
- 设计核对：校验用的是 `db.instance`（`--cloud-provider` 选出的 provider，比如 OKE），不是 `profProv`。所以 webhook profile provider 不会被校验，这和 PR 里写的范围一致。
- 修正：pr_body 的 Checklist 补上了 brief 要求的 “Documentation is updated” 一项（n/a，并说明理由）。

## 需要提交者注意
- 需要签 CNCF CLA（EasyCLA，由 owner 签）。不需要 DCO，也不需要 changelog 片段。
- 仓库（CONTRIBUTING/AGENTS/CLAUDE/.github）没有 AI 政策。按 Kubernetes 的通用指引，提交者要对代码负责并审阅过代码；PR 正文已写明使用了 AI。
- PR 模板要求的 /kind feature、Fixes #278 和 release-note 都已写在 pr_body.md 里（它同时包含 chefs-pick 格式的 Description/disclosure/Checklist）。
- 风险：issue 作者（Oracle）可能打算自己实现 OKE 的部分，也有 open 的 #357 在改 cloudprovider。本 PR 只追加代码，PR 正文已说明只提供通用钩子。如果维护者更想用 webhook capability 或其他形式，可能需要调整。
- 设计取舍：校验放在 eBPF unpin 之前，这样被拒绝的那次尝试不会修改 host。校验拿到的是 config 指针，接口注释要求实现方只读，没有做深拷贝。
- 本地测试替换成 lo 的做法只是为了在沙箱里验证；上游 CI 有 dummy 模块，可以直接运行。

## 如何提交
```bash
git clone https://github.com/kubernetes-sigs/dranet && cd dranet
git checkout -b validate-network-config origin/main
git am /home/user/Playground/contributions/110-kubernetes-sigs-dranet-278/0001-Validate-host-derived-network-config-before-checkpoi.patch
go test -race ./pkg/driver/... ./pkg/inventory/... ./pkg/cloudprovider/... && hack/lint.sh
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/110-kubernetes-sigs-dranet-278 kubernetes-sigs/dranet main validate-network-config contributions/110-kubernetes-sigs-dranet-278/pr_title.txt contributions/110-kubernetes-sigs-dranet-278/pr_body.md
```
工作 clone 位于 /home/user/work/dranet，分支是 `validate-network-config`，commit 是 27802a82。

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
