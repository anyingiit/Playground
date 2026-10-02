# marketcalls/openalgo#1849 — Keep API keys out of persisted localStorage

| 项 | 值 |
|---|---|
| Issue | https://github.com/marketcalls/openalgo/issues/1849 |
| Tier | 自由 |
| Labels | bug, frontend, good first issue, help wanted, security |
| Status | 完成 — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue 开放、无 assignee、无评论、无关联 PR；PR 列表搜索 `1849` / `apiKey` / `localStorage` / `authStore` 均无相关 PR（#1865/#1915/#1920/#1941 是后端 no-store 头，不同问题） |
| Base | `main` @ ad2a3f5 |

## 问题理解
`frontend/src/stores/authStore.ts` 用 Zustand `persist` 持久化整个 store（含 `apiKey`）到 `localStorage["openalgo-auth"]`。issue 要求：新写入不含 key；旧数据在 hydration 时被移除/忽略；会话中 key 仍在内存可用；logout 清空；测试用假 storage + 明显假值。

## 合理性判断
合理的安全加固，维护者自己打了 good first issue / help wanted。`AuthSync` 在每次加载时都会从 `/auth/session-status` 重新获取 `api_key`，且检查完成前不渲染子组件，所以 key 不需要持久化。

AI 政策：CONTRIBUTING.md 明确承认 "many contributions today are developed with AI assistance"，只要求一次一个 fix、充分测试，没有禁止。CLAUDE.md 要求 Conventional Commits，且 **任何地方都不能有 icon/emoji（包括 PR 描述）**，所以 PR body 里去掉了披露段落末尾的笑脸。

## 改动
- `authStore.ts`：`partialize` 只持久化 `user`、`isAuthenticated`；`version: 1` + `migrate` 重写旧条目（去掉 key 并回写 localStorage）；`merge` 永不从 storage 取 `apiKey`。
- 新增 `authStore.persist.test.ts`（4 个测试）。

## 验证（frontend/，`npm ci --ignore-scripts`，Node 22）
- red：仅还原 `authStore.ts` 后 `npx vitest run src/stores/authStore.persist.test.ts` → 2 failed | 2 passed（写入含 key、旧 key 被加载）
- green：同命令 → 4 passed
- `npx vitest run`（= `npm run test:run`）→ 245 files / 3457 tests passed
- `npm run lint` → 0 errors（4 warnings / 2 infos 为既有）；`npx biome check` 改动文件 → clean
- `npx tsc -b` → clean
- 未运行：Python 后端测试、Playwright e2e、`npm run build`（与改动无关；tsc 已覆盖类型）

## 需要提交者注意
- 提交者身份：anyingiit <49945850+anyingiit@users.noreply.github.com>；仓库不要求 DCO。
- 仓库规则：PR 标题/描述/commit 中不要用 emoji；一个 PR 只做一个 fix。
- `frontend/dist/` 由 CI 在 main 上构建，PR 不需要也不应提交 dist。
- 行为差异（已在 PR 描述说明）：若加载时 `/auth/session-status` 网络错误，`apiKey` 保持 null（以前会用 localStorage 里的旧 key）。
- 未添加 CHANGELOG（`docs/CHANGELOG.md` 在发版时写）。

## 如何提交
```bash
git clone https://github.com/anyingiit/openalgo.git && cd openalgo   # 先在 GitHub fork marketcalls/openalgo
git remote add upstream https://github.com/marketcalls/openalgo.git && git fetch upstream
git checkout -b fix/auth-store-no-persisted-apikey upstream/main
git am /path/to/0001-fix-frontend-keep-the-API-key-out-of-persisted-local.patch
cd frontend && npm ci && npx vitest run src/stores/authStore.persist.test.ts && cd ..
git push -u origin fix/auth-store-no-persisted-apikey
gh pr create --repo marketcalls/openalgo --head anyingiit:fix/auth-store-no-persisted-apikey \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
见 `pr_title.txt`：`fix(frontend): keep the API key out of persisted localStorage`

## PR body
见 `pr_body.md`。
