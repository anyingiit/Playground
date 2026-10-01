# marketcalls/openalgo#1849: Keep API keys out of persisted localStorage

| 项 | 值 |
|---|---|
| Issue | https://github.com/marketcalls/openalgo/issues/1849 |
| Tier | 自由 |
| Labels | bug, frontend, good first issue, help wanted, security |
| Status | ✅ ready: patch、测试、PR 文案都已完成 |
| 重复 PR 检查 | 搜索 `is:pr 1849` 无结果。`apiKey localStorage` 只搜到 #1865，它解决的是 #1850（no-store 响应头），没有改 authStore。issue 无 assignee、无评论（2026-10-01 核实） |
| Base | `main` @ ad2a3f5 |

## 问题理解
`frontend/src/stores/authStore.ts` 用 zustand `persist` 持久化了整个 state，`apiKey` 因此被写进了 `localStorage['openalgo-auth']`。issue 的验收标准有五条：新的写入不能包含 key；旧数据里的 key 要在 hydrate 时删掉或忽略；会话期间 key 仍然留在内存里可用；logout 要清掉内存里的 key；测试要用假 storage 和明显的假值。

## 合理性判断
- 维护者在 #1865 的 review 中明确说，加 `partialize` 不再持久化 API key 是 "the more valuable half of this work"，建议另开 PR 来做。
- `AuthSync` 包住了整个 App，每次加载页面都会先请求 `/auth/session-status` 并调用 `setApiKey`，等这一步完成后才渲染，所以不持久化 key 不会影响功能。
- AI 政策：CONTRIBUTING 承认 "many contributions today are developed with AI assistance"，要求一个 PR 只做一个 fix，并且经过仔细的测试。项目没有禁止 AI 贡献。

## 改动
- `authStore.ts`：
  - 用 `partialize` 只保存 `{user, isAuthenticated}`。
  - 设 `version: 1`，`migrate` 时去掉 v0 数据里的 `apiKey`。migrate 之后 zustand 会重写 storage，旧 key 会被一起清掉。
  - `merge` 时忽略 storage 里的 `apiKey`，避免它覆盖内存里的值。
- 新增 `authStore.persist.test.ts`，共 4 个用例。

## 验证（在 frontend/ 下执行，node 22.22，`npm ci --ignore-scripts`）
- 修复前（red）：`npx vitest run src/stores/authStore.persist.test.ts` 有 2 个失败，一个是 key 出现在 localStorage 里，另一个是 legacy key 被 hydrate 回内存。
- 修复后（green）：同一命令 4/4 通过。
- 全量 `npx vitest run --maxWorkers=3`：245 个文件、3457 个测试全部通过。
- `npm run lint`（CI 跑的就是这一步）：0 error。4 个 warning 和 2 个 info 都是已有的，不在本次改动的文件里。`npx biome check ./src/stores` 无问题。
- `npx tsc -p tsconfig.app.json --noEmit` 通过。
  - `tsconfig.test.json` 会报 TS6307（authStore 不在它的文件列表里），这是 main 上本来就有的配置问题，和本次改动无关。

## 需要提交者注意
- CONTRIBUTING 要求不要提交 `frontend/dist/`。本 patch 没有包含它。
- 不需要 DCO。commit 格式是 Conventional Commits。
- PR body 中已写明使用了 AI 辅助（disclosure 段）。
- 这个 issue 很新（label 是 good first issue / help wanted），提交前请再确认一次没有人新开 PR。

## 如何提交
```bash
git clone https://github.com/anyingiit/openalgo && cd openalgo   # 先 fork
git remote add upstream https://github.com/marketcalls/openalgo && git fetch upstream
git checkout -b fix/auth-store-no-persist-api-key upstream/main
git am /path/to/0001-fix-frontend-keep-API-key-out-of-persisted-auth-stor.patch
git push origin fix/auth-store-no-persist-api-key
gh pr create --repo marketcalls/openalgo --head anyingiit:fix/auth-store-no-persist-api-key \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
见 `pr_title.txt`

## PR body
见 `pr_body.md`
