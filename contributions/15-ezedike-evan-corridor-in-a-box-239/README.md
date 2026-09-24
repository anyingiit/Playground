# ezedike-evan/corridor-in-a-box #239 — Attester: typed cooldown error code

| 项 | 值 |
|---|---|
| Issue | https://github.com/ezedike-evan/corridor-in-a-box/issues/239 |
| Tier | 自由 |
| Labels | enhancement, good first issue |
| Status | ✅ done — patch + PR text ready (not submitted) |
| Duplicate-PR check | 2026-09-24 (before and after implementing): issue open, unassigned, 0 comments, no linked PR; no open non-dependabot PRs; PR search "cooldown" → 0, "239" → only an unrelated dependabot PR |
| AI-contribution policy | No AGENTS.md / CLAUDE.md / copilot-instructions; CONTRIBUTING, PR template, .github have no AI/LLM clause → not banned |
| Base branch | `main` @ 5bc2bb5 |

## 候选评估
- corridor-in-a-box #246（canonical domain）：需要改 Soroban 合约并跑 `cargo test` / clippy / wasm 构建，磁盘预算（≤3 GB）风险大；未选。
- **corridor-in-a-box #239**：纯 TS，Size S，验收标准清楚 → 选中。
- Ciaren #194：文档任务，要求从运行中的 app 导出真实 Polars 代码，且要求先在 issue 里认领 5–10 页，无法在此环境完成认领 → 未选。
- 仓库会合并外部 PR（#71 aojomo、#72/#76 kelvinokwudili52-stack、#61/#62 Qwin B、#63/#64 royaldev、#77 等），维护者会 review/merge。

## 问题理解
合约 `contracts/attester/src/lib.rs` 的 `enum Error { NotInitialised=1, NotAnAttester=2, TooSoon=3, InvalidDomain=4 }`。
`packages/attester` 的私有 `explain()` 把 `Error(Contract, #3)` 映射成英文句子，`attest()` 以 `MANIFEST_INVALID` 返回；
`examples/attest.ts`（也是 `attest-anchors.yml` 定时任务跑的脚本）用 `message.includes("cooldown")` 决定是否让任务失败 —— 控制流依赖英文措辞。

## 合理性判断
合理：CONTRIBUTING 强调 `Outcome` 值式错误处理；改动只加类型化字段，不改变现有 `code` / message，向后兼容。
Issue 也提到 `MANIFEST_INVALID` 用词不当，但提议方案没要求改它；改 `CorridorErrorCode` 联合类型会波及 `packages/service` 的 HTTP 映射等，故保持不变并在 PR 里说明，留给维护者决定。

## 改动
- `packages/attester/src/index.ts`
  - 导出 `enum AttesterContractError`（与合约 `enum Error` 对应）；`CONTRACT_ERRORS` 以其为键。
  - 导出 `interface AttesterError extends CorridorError { contractError?: AttesterContractError | number }`；`attest()` 返回 `Outcome<AttestationRef, AttesterError>`。
  - 导出 `explain(error): { code?, message }`；即使是未知的合约错误号也会返回 `code`。
  - 模拟失败时，若 host error 是合约错误，则在错误上附 `contractError`。
- `examples/attest.ts`：`submitted.error.contractError === AttesterContractError.TooSoon` 取代 `.includes("cooldown")`（仓库中已无 `.includes("cooldown")`）。
- `tests/attester.test.ts`（新）：`explain()` 4 个用例（#3→TooSoon、所有已知码、未知码 #99、非合约错误）；`attest()` 3 个用例（stub RPC server 的 `simulateTransaction`，#3→TooSoon、#2→NotAnAttester、非合约错误→无 `contractError`）。
- `CHANGELOG.md`：Unreleased 下新增 "Changed" 条目（仓库惯例）。

## 验证
Node v22.22.2, pnpm 9（`pnpm install --frozen-lockfile`）。
- Red（只保留新测试，回退源码改动）：`pnpm exec vitest run tests/attester.test.ts` → **6 failed / 1 passed**（`explain is not a function`、`AttesterContractError` undefined 等；唯一通过的是"非合约错误时 contractError 为 undefined"，旧代码天然满足）。
- Green：同命令 → **7 passed**。
- 全量 gate（CI 同款）：
  - `pnpm lint`（eslint + prettier --check）→ 通过
  - `pnpm typecheck`（tsc --noEmit）→ 通过
  - `pnpm test` → **21 files passed / 1 skipped；252 tests passed / 13 skipped**（skipped 为需要真实 anchor / Postgres 环境变量的 integration 测试，基线同样 skip）。
- 未运行：Rust 合约 CI（`cargo test` 等）—— 本改动未触及 `contracts/`；`web/` 的 typecheck/build —— 未触及 `web/`。

## 需要提交者注意
- 仓库未发现 AI 贡献政策限制；PR 正文已含 disclosure 段。
- 不需要 DCO / Signed-off-by。Commit 采用 Conventional Commits（`feat(attester): …`）。
- PR 模板要求勾选 "Type of change"，已在下方 PR body 中保留该段。

## 如何提交
```bash
git clone https://github.com/<you>/corridor-in-a-box.git && cd corridor-in-a-box
git checkout -b feat/attester-typed-contract-error origin/main
git am /path/to/0001-feat-attester-report-contract-rejections-with-a-type.patch
pnpm install --frozen-lockfile && pnpm lint && pnpm typecheck && pnpm test
git push -u origin feat/attester-typed-contract-error   # then open PR against ezedike-evan/corridor-in-a-box:main
```

---

## PR title

feat(attester): report contract rejections with a typed error code

## PR body

```markdown
## Description

`examples/attest.ts` (the script the scheduled `attest-anchors.yml` job runs) decided whether a failed
attestation should fail the job by checking the error message for the word `"cooldown"`. That makes control
flow depend on English wording: rewording the message in `@corridor/attester` would silently turn every
cooldown hit into a job failure (or vice versa).

This PR surfaces the attester contract's own error number instead:

- `@corridor/attester` exports `AttesterContractError` (`NotInitialised = 1`, `NotAnAttester = 2`,
  `TooSoon = 3`, `InvalidDomain = 4`), mirroring `enum Error` in `contracts/attester/src/lib.rs`.
- `AnchorAttester.attest()` now returns `Outcome<AttestationRef, AttesterError>`, where
  `AttesterError extends CorridorError` with an optional `contractError`. It is set whenever the simulation
  revert is a contract error (`Error(Contract, #n)`), including numbers this client doesn't know yet.
- `explain()` is exported and returns `{ code?, message }`, as suggested in the issue.
- `examples/attest.ts` checks `submitted.error.contractError === AttesterContractError.TooSoon`. There are no
  `.includes("cooldown")` checks left.
- `CHANGELOG.md`: added an entry under Unreleased.

The error `code` (`MANIFEST_INVALID`) and the message text stay the same, so existing callers keep working.
The issue also says `MANIFEST_INVALID` is the wrong code for attestation reverts. I agree, but changing it
means adding a member to `CorridorErrorCode` and a matching entry in the service's HTTP status map, so I left it
out to keep this PR small. Happy to add it here or open a follow-up if you'd like.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #239

## Type of change

- [ ] New corridor manifest (`*.corridor.yaml` only — no engine change)
- [ ] Bug fix
- [x] Feature
- [ ] Docs
- [ ] Build / CI / chore

## Checklist

- [x] `pnpm lint && pnpm typecheck && pnpm test` pass locally (lint + prettier clean; tsc clean; vitest: 21 files passed / 1 skipped, 252 tests passed / 13 skipped (the env-gated integration tests))
- [x] Tests added/updated for any behaviour change: new `tests/attester.test.ts` (7 tests: `explain()` maps #3 → `TooSoon`, all known codes, unknown codes, non-contract errors; `attest()` with a stubbed RPC server carries `contractError`). Without the source change, 6 of the 7 fail.
- [x] No corridor-specific strings added to `packages/engine`
- [x] No dependency on the proprietary `RouteResolver` dataset added outside the `packages/router` seam
- [x] Money handled via the `Money` type — never a JS `number` (n/a, no money handling touched)
- [x] `CHANGELOG.md` updated (Unreleased → "Changed — attester rejections carry a typed contract error code")
- [x] README / relevant doc updated if a public interface changed: new exports are documented with TSDoc and in the CHANGELOG; no README section covers attester errors
- [x] No secrets, signing keys, or `.env` files committed
```
