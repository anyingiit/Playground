# getsotto/sotto#696: invitation expiry blames renewal even when the response deadline passed first

| 项 | 值 |
|---|---|
| Issue | https://github.com/getsotto/sotto/issues/696 |
| Tier | 自由（getsotto/sotto；009 已合并过 #400） |
| Labels | bug, good first issue, help wanted |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 19:25 UTC：`repo:getsotto/sotto 696` → 0；`is:open invitation expiry` → 0；issue 无 assignee、无评论（只有一条被成员删除的 github-actions 评论）、无关联 PR |
| AI 政策 | CONTRIBUTING / .github / docs 无 AI 限制（AGENT-WORKFLOWS.md 是产品功能文档，与贡献无关）；issue 未提 AI |
| Base | `main` @ 88b204b |
| DCO / CLA / changeset | **需要 DCO**：commit 已带 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`（owner 规则允许代签）。无 CLA、无 changelog 片段 |
| 需先认领 | 否（issue 未要求） |

## 问题理解
`PayerTransferInbox` 在 `min(consentExpiresAtEpoch, effectiveFrom)` 处把 open invitation 视为过期（正确），但 `stateCopy` 只收到布尔值，永远显示 "expired at the renewal boundary"。当响应截止早于续费日时这句话是错的。

## 改动
- `web/src/PayerTransferInbox.tsx`：新增 `InvitationExpiry = "response_deadline" | "renewal"`；渲染时 `consentExpiresAtEpoch < effectiveFrom` → response_deadline，否则 renewal（相等算 renewal）；`stateCopy` 对两种情况给不同文案。计算、定时器、按钮移除逻辑不变。英式英语（项目要求）——新文案无拼写差异词。
- `web/src/__tests__/PayerTransferJourneys.test.tsx`：改现有定时器测试断言新文案；新增“续费先到仍显示 renewal 文案”和“加载时已过响应截止（未到续费）显示截止文案”两个测试。

## 验证
- 红：回退 `PayerTransferInbox.tsx` 后 `npx vitest run src/__tests__/PayerTransferJourneys.test.tsx` → 2 failed（定时器测试 + 加载已过截止测试）/ 15 passed
- 绿：恢复后 → 17 passed
- 全量 `npx vitest run` → 260 passed，2 failed 均为 `wasmLoader.test.tsx`（缺 wasm-pack 产物 `src/wasm/sotto_wasm.js`，base 上同样失败）
- `tsc -p tsconfig.json` → 仅报缺 wasm 模块（base 相同）
- 未跑：wasm-pack 构建、playwright e2e、Rust 部分

## 需要提交者注意
- PR 模板是 Summary / Closes / Tests / DCO 勾选，pr_body.md 已按模板写并附 Description 与披露段。
- commit 已含 Signed-off-by，DCO 检查应能通过。

## 如何提交
```
tools/submit_pr.sh contributions/242-getsotto-sotto-696 getsotto/sotto main fix-invitation-expiry-copy contributions/242-getsotto-sotto-696/pr_title.txt contributions/242-getsotto-sotto-696/pr_body.md
```
（手动：fork → `git checkout -b fix-invitation-expiry-copy origin/main` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR）

## 独立复核（2026-10-22 19:50 UTC）
- 上游：#696 仍 open、无 assignee、无认领；`repo:getsotto/sotto 696` → 0 PR；关键词搜索只命中无关的 #651 及已关闭 #630/#502。
- 新浅克隆 main@88b204b，`git am` 干净；作者与 Signed-off-by 均为 anyingiit noreply。
- 红→绿：回退 Inbox.tsx → 2 failed；打补丁 → 17/17。全量 vitest 260 passed + 2 个 wasmLoader（main 同样失败）；tsc 仅缺 wasm 模块（main 相同）。
- 代码审阅：`<` 严格比较，同一秒算 renewal（此时续费确已到达，文案正确）；加载即过期场景每次渲染计算并有测试；计算/定时器/按钮不变。英式英语、文案清晰；PR 正文符合模板，数字与复核一致。
- 结论：PASS
