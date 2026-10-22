# 429 — supabase/terraform-provider-supabase#372: creating a project with instance_size = "nano" fails

| Item | Details |
|---|---|
| Issue | https://github.com/supabase/terraform-provider-supabase/issues/372 |
| Tier | High-star / up-and-coming (Supabase's official Terraform provider) |
| Labels | bug, good first issue (maintainer savme added good first issue on 2026-10-22) |
| Base branch | `main` (patch built on 3a95cbe) |
| Status | ✅ 可提交 |
| Duplicate check | 2026-10-22: the issue has no comments and no linked PR. A PR search for instance_size finds only #255, already merged. |
| AI policy | None |
| CLA/DCO | None |

## Change
- `readProject`: `instance_size` now defaults to `nano` instead of null. A selected compute_instance addon still overrides it.
- New acceptance test (gock mocks) covering create and import.

## Verification
- Red: the new test fails with exactly the "Provider produced inconsistent result after apply ... was nano, but now null" error from the issue.
- Green: it passes. Full `TF_ACC=1 go test ./internal/provider/` passes (~6 minutes).
- golangci-lint: 0 issues.
- Limitation: not verified against the real Supabase API. The PR body says so.

## How to submit
```
git clone https://github.com/supabase/terraform-provider-supabase && cd terraform-provider-supabase && git checkout -b fix-nano-instance-size origin/main
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）

- 全新克隆 supabase/terraform-provider-supabase，origin/main = 3a95cbe，`git am` 干净应用。
- 提交检查：作者为 anyingiit <49945850+anyingiit@users.noreply.github.com>，无 AI 模型名，标题 `fix(project): ...` 符合仓库 conventional commits 风格，含 `Fixes #372`。
- Red→green：仅回退 `internal/provider/project_resource.go` 后，`TestAccProjectResource_NanoInstanceSize` 失败，报错与 issue 完全一致（`.instance_size: was cty.StringVal("nano"), but now null`）。应用补丁后通过。
- 全量 `TF_ACC=1 go test ./internal/provider/ -count=1`：ok（362.8s）。`golangci-lint run ./...`：0 issues。
- 代码审查：
  - `instance_size` 为 Optional+Computed+UseStateForUnknown。未设置该字段的用户：首次 refresh 后 state 由 null 变为 `nano`，配置为 null，所以无 diff、不触发更新。
  - 付费计划项目：billing 返回 `ci_*` addon 时仍会覆盖默认值，行为不变。付费计划中从免费计划升级、仍在 Nano 上的项目没有 addon，读成 `nano` 是正确的。
  - Update 路径：nano→micro 发送 `ci_micro`，之后 state = plan，下一次 refresh 一致。micro→nano 会发送不存在的 `ci_nano`，这是原有问题，不是本补丁引入的回退，补丁也没有让它变得更糟。
  - Import：测试的 ImportStateVerify 步骤覆盖了 import，读到 `nano`。
  - 没有 project 数据源，`instance_size` 的唯一读取者是 `readProject`。
- 文档：schema 和描述未改，tfplugindocs 输出不变，无需 `go generate`。docs/resources/project.md 只写了 "Desired instance size of the project"，不涉及 null/nano 语义。
- 公开资料：supabase.com/docs/guides/platform/compute-and-disk 把 Nano 描述为免费计划的基础实例，不是 add-on，并写明 "You cannot launch Nano instances on paid plans"，支持“nano 没有 compute addon”的前提。issue 作者也指出 compute_instance 选项从 `ci_micro` 开始。
- 竞争 PR：10 个 open PR 都与 instance_size/nano 无关。#364 修改 project_resource.go，但没有改 readProject，冲突风险很低。
- pr_body.md：前两行是署名块，有 AI 披露段落，并如实说明未对真实 API 测试。小修：把 "existing tests show" 改为 "existing tests mock"（测试只是 mock，不能证明真实 API 的行为），并补充 compute 文档链接。

结论：PASS。补丁很小，修复点准确，有 red→green 测试，全量测试和 lint 都通过，没有发现回退。剩余风险只是未对真实 API 验证，PR 正文已如实说明。
