# OpsiMate/OpsiMate #1041 — Add unit tests for mute-policy and enrichment GET/PUT/DELETE by id

| 项 | 值 |
|---|---|
| Issue | https://github.com/OpsiMate/OpsiMate/issues/1041 |
| Tier | 新锐 |
| Labels | DevOps, Server, Test, bug, documentation, good first issue, hacktoberfest |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue 是 open 状态，没有 assignee，也没有评论。`pulls?q=1041` 只搜到不相关的 #598、#571。关键词搜索（mute enrichment test）没有找到同主题的 open 或 merged PR。main 上已有的 `idParams.test.ts` 只覆盖了两个资源 GET 的 400 情况。 |
| Base | `main` @ 7593155（2026-09-30） |

## 问题理解
维护者希望新增 `apps/server/tests/rulesById.test.ts`，参照 `tests/tags.test.ts` 的写法，为 `/api/v1/mute-policies/:id` 和 `/api/v1/enrichments/:id` 补测试：GET 已有资源、未知 id 返回 404（GET/PUT/DELETE）、非数字 id 返回 400（zod）、缺少 Authorization 返回 401、PUT `{}` 时资源不变。提交前需要跑 Prettier。evaluator 不在范围内。

## 合理性判断
- issue 由维护者开出，写明了文件名、参照文件和要覆盖的场景，属于纯测试补充，不需要设计讨论。
- main 上没有这个文件，也没有覆盖这些场景的测试（`idParams.test.ts` 只覆盖 GET 的 400）。

## 改动
只新增 `apps/server/tests/rulesById.test.ts`（约 150 行），用 `describe.each` 让两个资源跑同一组 7 个用例，共 14 个测试。每个用例的 `beforeEach` 先清空对应的表（`alert_mute_policies` / `alert_enrichments`），再通过 POST 创建一条记录。PUT `{}` 的用例比较返回值时忽略 `updatedAt`。

## 验证（Node 22.22.0，pnpm 9.12.0；CI 用的是 Node 24）
- 安装依赖：`pnpm install --frozen-lockfile`，然后 `pnpm --filter @OpsiMate/shared --filter @OpsiMate/custom-actions run build`（CI 也是先 build；不 build 的话 snapshotWorker 测试和 eslint 会因为找不到 shared/dist 而失败，base 上同样如此）。
- 新测试：`cd apps/server && pnpm exec vitest run tests/rulesById.test.ts`，14 个全部通过。
- 这是纯测试改动，所以 red→green 的做法是逐个改坏被测代码，确认对应测试变红，测完全部还原：
  - M1：mute-policy controller 去掉 `!mutePolicy` 的 404 判断，`404 for an unknown id` 和 `DELETE removes the resource` 失败
  - M2：enrichment deleteHandler 去掉 `!existing` 判断，enrichments 的 404 用例失败
  - M3：mute-policy controller 不再把 zod 错误映射为 400，400 用例失败
  - M4：mute-policy updateHandler 在请求没传 reason 时写入 `reason: null`，"PUT 空 body 不变"用例失败
  - M5：把 `/enrichments` 路由挂到 `authenticateJWT` 之前，401 用例失败
- 完整 server 测试：`pnpm exec vitest run --maxWorkers=2`，46 个文件、610 个测试全部通过。
- `pnpm run format`（prettier --check .）和 `pnpm run lint`（eslint src --max-warnings=0）都通过。
- `tsc --noEmit -p .`：新文件没有类型错误。仓库现有的 TS6059（tests 不在 rootDir 下）对所有测试文件都会报，与本改动无关。

## 需要提交者注意
- issue 底部写着："New contributors: one open PR on a good-first-issue at a time, and please run the tests ... before opening it"。如果你在 OpsiMate 已经有一个 open 的 good-first-issue PR，请等它处理完再提交这个。最好先在 issue 下评论认领（例如 "I'd like to take this"），再开 PR。
- CONTRIBUTING 要求 PR 标题必须是 `[FEAT]: ...` 或 `[FIX]: ...`，这里用的是 `[FEAT]:`。CI 的标题检查也接受 TEST 前缀，如果维护者更习惯 `[TEST]:`，可以改。
- 仓库没有 AI 相关政策（CONTRIBUTING、.github、labels 都查过），不需要 DCO，也没有 CHANGELOG。PR 正文已按仓库模板的 Issue Reference / What Was Changed / Why Was It Changed / Screenshots 几项写进 Description。
- `git am` 会把 patch 主题里的 `[FEAT]:` 当成方括号前缀去掉，所以本地 commit 主题会变成 "Add tests for ..."（`tools/submit_pr.sh` 也一样）。上游一般 squash 合并、用 PR 标题作为提交信息（如 `[FEAT]: ... (#1074)`），所以影响不大；如果想保留前缀，可以在 `git am` 之后用 `git commit --amend` 把主题改回 `pr_title.txt` 的内容。
- 仓库的 pre-commit hook 会对暂存文件跑 Prettier。新文件已经是 Prettier 格式，hook 不会改动它。

## 如何提交
```bash
git clone https://github.com/OpsiMate/OpsiMate && cd OpsiMate
git checkout -b test/rules-by-id origin/main
git am /home/user/Playground/contributions/706-OpsiMate-OpsiMate-1041/0001-FEAT-Add-tests-for-mute-policy-and-enrichment-GET-PU.patch
pnpm install --frozen-lockfile && pnpm --filter @OpsiMate/shared --filter @OpsiMate/custom-actions run build && pnpm --filter @OpsiMate/server test
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/706-OpsiMate-OpsiMate-1041 OpsiMate/OpsiMate main test/rules-by-id contributions/706-OpsiMate-OpsiMate-1041/pr_title.txt contributions/706-OpsiMate-OpsiMate-1041/pr_body.md
```

## 复核（独立 reviewer，2026-10-01）
- 在新的 shallow clone（main @ 7593155）上 `git am` 干净应用；新测试 14/14 通过。
- 独立做了 3 个不同于实现者的改坏实验，均被对应用例捕获后还原：enrichment updateHandler 去掉 404 判断 → 404 用例失败；enrichment deleteHandler 不再映射 zod 错误 → 400 用例失败；`v1.ts` 去掉 `router.use(authenticateJWT)` → 两个资源的 401 用例均失败。
- 完整 server 测试 46 文件 / 610 测试通过；`pnpm run format`、`pnpm run lint` 通过；`tsc` 对新文件无新增错误（仅既有 TS6059）。
- 注：直接对 tests 目录跑 eslint 会报 `no-unsafe-member-access`，但仓库 lint 只检查 `src`，现有 `tests/tags.test.ts` 同样有这些报错，不属于本改动的问题。

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
