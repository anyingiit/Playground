# MODSetter/SurfSense#2141 — workspace event stream 每次重试都加 abort listener 且不移除

Status: ⏭️ skipped — 已有竞争 PR #2142（DYNOSuprovo，2026-10-01 开，base dev，Fixes #2141，改动范围与本补丁完全相同），不再提交。

| 项 | 值 |
|---|---|
| Issue | https://github.com/MODSetter/SurfSense/issues/2141 |
| Tier | 高星 |
| Labels | bug, desktop, frontend, good first issue, help wanted |
| Status | ⏭️ skipped — 竞争 PR #2142 已覆盖同一修复 |
| Base | `dev` @ bbfa32a (2026-10-01, merge of #2140). **注意：默认分支 main 上还没有这个文件，PR 必须以 dev 为目标** |
| Duplicate-PR check | 2026-10-01 23:0x UTC：issue OPEN、0 评论、无 assignee；`pulls?q=is:pr 2141` 0 结果；关键词 "abort listener" 只有已合并的 #2140（记录 bug 的 docs PR）和 #2126（引入代码的 PR），无修复 PR；dev 上代码仍是旧实现 |

## 问题理解

`surfsense_local/frontend/src/features/workspaces/workspace-changes.ts` 中每个 workspace 共用一条 SSE 流，断开后 `follow()` 循环用 `wait(retry, signal)` 退避重试（1s→10s）。旧的 `wait()` 每次给 workspace 的 AbortSignal 加一个 `{ once: true }` 的 abort listener，但 timer 先触发时从不移除，导致 API 挂掉时每小时约积累 360 个 listener，直到最后一个列表退订。另外，signal 已经 aborted 时 abort 事件不会再触发，于是 `wait()` 会白白等完整个退避时间（最多 10s）才退出循环。

Issue 期望：timer 触发时移除 listener；signal 已 aborted 时立即返回；在 workspace-changes.test.ts 用 add/removeEventListener spy 加测试；删除 docs/architecture/overview.md 中的 known gap 条目。

## 合理性判断

- 维护者 MODSetter 本人提的 issue（在 #2126 review 中发现，#2140 记录到 Known gaps），标了 good first issue / help wanted，范围明确。
- AI 政策：仓库有 AGENTS.md / CLAUDE.md（symlink），CONTRIBUTING 明确写 "If you work with a coding agent, AGENTS.md gives it the same rules"；label 描述无 AI 限制；维护者自己的 commit 也带 Claude co-author trailer。允许 AI 参与。
- CONTRIBUTING：PR 目标分支是 `dev`；用 `Fixes #123` 关联；good first issue 要求"Comment on one to claim it"。

## 改动

- `workspace-changes.ts`：`wait()` 改为与 `use-studio.ts` 相同的清理模式——具名 `onAbort`，timer 回调里 `signal.removeEventListener("abort", onAbort)`；开头 `if (signal.aborted) return resolve()`。行为（resolve 而非 reject）与原来一致，`follow()` 不变。
- `workspace-changes.test.ts`：新增 `apiDown()`（fetch 一直失败）、`apiHanging()`（fetch 挂起直到 abort，像真实 fetch）两个桩，以及两个用 fake timers 的测试：
  - removes each retry's abort listener once its wait is over：API 挂 60s（约 9 次尝试），`removeEventListener` 次数 = `addEventListener` 次数 − 1（仅当前进行中的 wait 持有 listener）。
  - stops at once when the stream is closed between attempts：请求进行中退订 → 不再往已 aborted 的 signal 加 listener，且 `vi.getTimerCount() === 0`。
  - afterEach 增加 `vi.useRealTimers()`。
- `docs/architecture/overview.md`：删除该 Known gaps 条目。

## 验证

环境：Node v22.22.0（CI 用 Node 24），`surfsense_local/frontend` 下 `pnpm install --frozen-lockfile`（pnpm 11.27.1，按 packageManager）。

| 命令 | 结果 |
|---|---|
| 仅回退 `workspace-changes.ts`、保留新测试：`pnpm exec vitest run --environment jsdom src/features/workspaces/workspace-changes.test.ts` | **2 failed** / 3 passed（`removeEventListener` expected 8 times, got 0；`addEventListener` called 1 time on aborted signal）→ red |
| 打补丁后同一命令（连跑 3 次） | 5 passed ×3 → green |
| `pnpm test`（全量，CI 同命令） | 63 files / 384 tests passed |
| `pnpm typecheck`（tsc -b） | exit 0 |
| `pnpm lint` | exit 0 |
| `prettier --check` 两个改动文件 | pass |
| `pnpm translations:extract` + `git diff --exit-code translations/en.json` / `pnpm translations:verify` / `node scripts/check_translations.mjs` | 无变化 / pass / 0 problems |
| `python3 scripts/check_docs.py`（code-quality.yml 的 check-docs hook） | 111 doc files, 0 problems |

## 需要提交者注意

- **CONTRIBUTING 要求先在 issue 下评论认领**（"Comment on one to claim it"）。我们无法评论，提交前请先在 #2141 留言认领，再开 PR。
- PR **目标分支必须是 `dev`**（main 上没有该文件）。
- 仓库 PR 模板是 What / Why / Fixes # / How to test，pr_body.md 采用 chefs-pick 格式（Description / Related issue / Checklist），仓库模板的 What / Why / How to test 放在 Description 里，并含 disclosure 段。PR 中写 Closes #2141（CONTRIBUTING 示例用 Fixes，两者都能关闭 issue；commit 里用的是 Fixes #2141）。
- 无 DCO / Signed-off-by 要求，无 changelog。commit 用 Conventional Commits 风格（`fix(local): ...`），与仓库一致；未加 AI trailer（仓库不强制）。
- 勾选 "Allow edits from maintainers"（CONTRIBUTING 推荐）。

## 如何提交

```bash
git clone https://github.com/MODSetter/SurfSense && cd SurfSense
git checkout -b fix/workspace-stream-abort-listener origin/dev
git am /path/to/0001-fix-local-stop-the-workspace-stream-gathering-an-abo.patch
git push <your-fork> fix/workspace-stream-abort-listener
# 开 PR：base = dev，标题见 pr_title.txt，正文见 pr_body.md
```

工作目录（评审用）：/home/user/work/SurfSense-2141（分支 fix/workspace-stream-abort-listener，node_modules 已删除）。

## 独立复核

复核时间 2026-10-01 23:33 UTC。

- **Issue 状态**：#2141 仍为 OPEN、无 assignee。
- **竞争 PR**：GitHub 搜索 `is:pr 2141` 找到 **#2142**「fix(workspaces): clean up abort listener on retry timer and return early when aborted」（作者 DYNOSuprovo，OPEN，base `dev`，正文写 Fixes #2141）。它改的是同样三个文件：`workspace-changes.ts` 中的 `wait()` 在 timer 触发时移除 listener、signal 已 aborted 时立即返回；补了 listener 清理和立即 teardown 的测试；删掉了 docs 中 Known gaps 那条。已请求 code owner 审阅，CodeRabbit 已跑过。实现者检查时（23:0x UTC）还没有这个 PR，应是之后才开的。
- **补丁本身**：读过 diff，修复正确且完整。`onAbort` 引用 `timeout` 不会触发 TDZ（`addEventListener` 不会同步触发 abort）；做法与 `use-studio.ts` 一致；两个测试也能覆盖 issue 要求的两点。patch 作者是 anyingiit noreply，patch/标题里没有 AI 模型名，只有 pr_body 的 disclosure 段提到 Claude Code（这是有意为之）。
- **结论**：因为已有竞争 PR #2142 覆盖同一范围，且 CONTRIBUTING 要求先认领、先到者优先，所以**不提交**。本补丁只作留档。如果 #2142 被关闭且没有合并，可以重新考虑：先在 issue 下认领，再按上面的「如何提交」操作。
- 由于决定跳过，本次没有重跑 red→green 测试；实现者的验证记录见上文。
