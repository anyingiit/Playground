# denoland/std#3964 — expect: implement `toThrowErrorMatchingSnapshot()`

| Item | Value |
|---|---|
| Issue | https://github.com/denoland/std/issues/3964 (tracking: complete `std/expect`; "please submit one PR per API") |
| Tier | 高活跃高Star (denoland/std, TypeScript, release 2026.09.24 cut today) |
| Labels | PR welcome, enhancement, expect, good first issue |
| Status | ✅ ready — patch + PR text written |
| Duplicate-PR check | PR search `toThrowErrorMatching` / `toThrowErrorMatchingSnapshot` → none (only #3814, the 2023 PR that created std/expect). Re-checked 2026-09-24 before finishing. Issue unassigned, no comments claiming the API. |
| Base | `main` @ 2958335 (`chore: release 2026.09.24 (#7330)`) |
| Patch | `0001-feat-expect-unstable-implement-toThrowErrorMatchingS.patch` |

## 问题理解

#3964 是 `@std/expect` 的跟踪 issue，列出尚未实现的 Jest API，并要求“一个 API 一个 PR”。当前 main 上 `expect/mod.ts` 的模块文档写明只剩两个没实现：
`toThrowErrorMatchingSnapshot`、`toThrowErrorMatchingInlineSnapshot`（`toMatchSnapshot` / `toMatchInlineSnapshot` 已在 #7003 等 PR 中实现）。
本补丁只实现 `toThrowErrorMatchingSnapshot()`，inline 版本留给后续 PR（符合 “one PR per API”）。

Jest 语义：调用被测函数，捕获抛出的错误，把 `error.message` 与快照比较；函数未抛出时报 “Received function did not throw”；和 `.rejects` 一起用时比较 rejection reason 的 message；不支持 `.not`。

## 合理性判断

- 维护者在 issue 里明确欢迎（`PR welcome` + `good first issue`），mod.ts 中仍列为“still not available”，属于未完成工作。
- 没有 AI 禁令：`AGENTS.md` 是给 agent 的编码规范，`.github/CONTRIBUTING.md` 无 AI 条款，也无 PR 模板。
- 仓库非常活跃（今天刚发布 2026.09.24），toMatchSnapshot 的前例 PR 标题为 `feat(expect/unstable): ...`，因此沿用 `/unstable` scope（按 CONTRIBUTING，unstable API 的变更须带 `/unstable` 后缀，只触发 patch 版本）。

## 改动

- `expect/_matchers.ts`
  - 把 `toMatchSnapshot` 里“确定测试文件/测试名 → 生成 key → 比较/更新快照”的逻辑抽成私有 `matchSnapshot(matcherName, getValue, hint)`；`toMatchSnapshot` 行为不变（仍先检查 state、再计数、再应用 property matchers，顺序与原来相同；错误信息前缀改成用 matcherName 拼接，对 toMatchSnapshot 结果文字完全一致）。
  - 新增 `toThrowErrorMatchingSnapshot(context, hint?)`（`@experimental`）：拒绝 `.not`；若值是函数则调用并捕获，未抛出时抛 `AssertionError("Received function did not throw")`（支持 customMessage 前缀）；否则（`.rejects` 场景）直接把值当作错误；对有 `message` 属性的对象取 message，否则用抛出的值本身；然后走共享的快照逻辑（与 `toMatchSnapshot` 共享同一计数器与 `-- --update` 流程）。
- `expect/expect.ts`：注册 matcher。
- `expect/_types.ts`：`Expected` 接口新增 `toThrowErrorMatchingSnapshot(hint?: string): void`，含 JSDoc 与示例（与 toMatchSnapshot 一样用 `ts ignore`，因为需要快照文件）。
- `expect/mod.ts`：把它移入已支持列表，“still not available” 只剩 `toThrowErrorMatchingInlineSnapshot`。
- 新测试 `expect/_to_throw_error_matching_snapshot_test.ts`（9 个用例）：匹配、不匹配、hint、与 toMatchSnapshot 共享计数、缺失快照、函数未抛出、`.rejects`（匹配 + 不匹配）、`.not` 报错、缺少 currentTestName 时错误信息带正确 matcher 名。

## 验证

环境：Deno 2.9.7（官方 release zip，放在 work 目录），`DENO_DIR` 指向 work 目录。

| 命令 | 结果 |
|---|---|
| 基线（源码回退到 HEAD~1，只保留新测试）`deno test -A --no-check expect/_to_throw_error_matching_snapshot_test.ts` | **0 passed / 9 failed**（`matcher not found: toThrowErrorMatchingSnapshot`）；不加 `--no-check` 时类型检查即失败 → red |
| 修复后 `deno test -A expect/_to_throw_error_matching_snapshot_test.ts` | **9 passed / 0 failed** → green |
| `deno test -A --doc --parallel --trace-leaks expect/`（含 doc tests） | 237 passed (8 steps) / 0 failed |
| `deno lint`（全仓库，含自定义 lint 插件） | Checked 1172 files, 0 problems |
| `deno fmt --check` | Checked 1249 files, ok |
| `deno check expect/` | ok |
| `deno task lint:mod-exports` / `lint:export-names` / `lint:unstable-deps` / `lint:docs` / `lint:circular` | 全部通过（exit 0；“No unstable module is used in stable modules.”，“No circular dependencies found.”） |
| `deno task test:browser` | exit 0 |
| 手工端到端：临时测试文件 `-- --update` 生成快照 → 再跑通过 → 改错误信息后跑出 “Snapshot does not match” diff | 符合预期（临时文件已删除） |

未运行：全仓库 `deno task test`（只跑了受影响的 `expect/` 包及其 doc tests）、`test:node` / `test:bun`（需要 npm/bun 安装）、`typos`（本机无 typos 二进制）。

## 如何提交

```bash
git clone https://github.com/<you>/std.git && cd std
git checkout -b expect-to-throw-error-matching-snapshot origin/main
git am /path/to/0001-feat-expect-unstable-implement-toThrowErrorMatchingS.patch
deno task ok   # 或至少: deno test -A --doc expect/ && deno lint && deno fmt --check
git push -u origin expect-to-throw-error-matching-snapshot
```

需要提交者注意：
- PR 会被 squash merge，**PR 标题**就是 commit subject，决定版本号；保持 `feat(expect/unstable): implement toThrowErrorMatchingSnapshot()`（与 #7003 toMatchSnapshot 的前例一致）。若维护者认为它应算稳定 API，可改为 `feat(expect): ...`。
- 仓库没有 PR 模板，也没有 DCO / AI 条款；commit 中无 AI 署名。
- 可以在 PR 里说明 inline 版本（`toThrowErrorMatchingInlineSnapshot`）将另开 PR。

## PR title

`feat(expect/unstable): implement toThrowErrorMatchingSnapshot()`

## PR body

```markdown
## Description

Implements `expect(fn).toThrowErrorMatchingSnapshot(hint?)`, one of the two APIs that `expect/mod.ts` still lists as unavailable (tracking issue #3964 asks for one PR per API, so the inline variant is left for a follow-up).

Behaviour follows Jest:
- the received function is called and the `message` of the thrown error is compared with the stored snapshot (`-- --update` writes it, exactly like `toMatchSnapshot()`);
- with `.rejects`, the rejection reason's message is used;
- if the function does not throw, it fails with `Received function did not throw`;
- `.not` is rejected with the same error as the other snapshot matchers;
- it shares the per-test snapshot counter with `toMatchSnapshot()`, so both can be mixed in one test.

To avoid duplicating the snapshot bookkeeping, the body of `toMatchSnapshot()` (test path/name lookup, key/counter, assert vs. update mode) moved into a private `matchSnapshot()` helper that both matchers call. `toMatchSnapshot()` behaves as before, including the order of its checks; only the matcher name in the "Unable to determine test file path/name" errors is now parameterised. The new matcher is marked `@experimental` like `toMatchSnapshot()`, and `mod.ts` now lists it as supported.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Part of #3964

## Checklist

- [x] Tests pass locally (`deno test -A --doc --parallel --trace-leaks expect/` → 237 passed, 0 failed; the new `expect/_to_throw_error_matching_snapshot_test.ts` has 9 tests that all fail on `main` and pass with this change; `deno lint`, `deno fmt --check`, `deno task lint:docs`, `lint:mod-exports`, `lint:export-names`, `lint:unstable-deps`, `lint:circular` and `test:browser` all pass)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, release notes are generated from the PR title
- [x] Documentation is updated (if applicable) — JSDoc on `Expected.toThrowErrorMatchingSnapshot` and the supported/unsupported list in `expect/mod.ts`
```
