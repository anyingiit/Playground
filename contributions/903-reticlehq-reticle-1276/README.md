# reticlehq/reticle#1276 — `init` detects a Vinext app as Next.js

| 项 | 值 |
|---|---|
| Issue | https://github.com/reticlehq/reticle/issues/1276 |
| Tier | 新锐 |
| Labels | bug, good first issue, area/init, fw/next, fw/vite, agent-reported, P2, hacktoberfest |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 无（PR 搜索 `1276`、`vinext` 均 0 结果；issue 无 assignee、无评论，2026-10-01 复核） |
| Base | `main` @ `14085e6` (chore(release): v3.5.0 …) |

## 需要提交者注意

- **DCO 必须**：CI 有 DCO 检查，patch 已带 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`（与 commit author 一致）。如改用其它邮箱，请 `git commit --amend --reset-author -s` 重新签。
- **AI 政策**：CONTRIBUTING「AI-assisted contributions」欢迎 AI 协助，条件是「测试在没有修复时必须失败，并在 PR 描述里说明已检查」——pr_body.md 的 *How it was verified* 已写明。commit 里没有 AI co-author trailer。
- CONTRIBUTING 要求**先在 issue 下评论认领**（"Comment on the issue to claim it"），建议提交前先评论一句。
- 用 PR 模板（What & why / How it was verified / Gates run / Checklist），已按其格式写好并加入 disclosure 段落。
- `pnpm gate:install`（模板里 touched `reticle init` 那一档）本地未跑：需要本地 registry + reticle-fixtures 真实应用，已在 PR 中如实说明。
- 设计取舍：按 issue 的验收标准把 Vinext 归为 Vite，而非新增 `Framework.VINEXT`；Vite 插件的 index.html 注入能否覆盖 Vinext 的 SSR HTML 未在真实应用上验证，PR 中已说明并提出可改为独立条目。

## 问题理解

Vinext（在 Vite 上重新实现 Next.js API）依赖 `next` 包，但构建用 Vite，不会读取 `next.config.*`。`init/src/detect/detect.ts` 的 `DETECTION_ORDER` 中 `NEXT` 排第一，`next` 依赖一出现就判为 Next，于是计划把 `withReticle` 写进一个永远不执行的配置，应用无法连接。

## 合理性判断

维护者打了 bug + good first issue，并给出明确验收标准（`{ next, vinext, vite }` 应识别为 Vite 或独立条目，并加测试）。代码中已有同类机制 `configsUnless`（SvelteKit），本改动是对称扩展。

## 改动

- `FrameworkSignals` 新增可选 `depsUnless`：出现这些依赖时，该框架的 deps 与 configs 两种信号都失效，继续沿链匹配。
- `Framework.NEXT` 设置 `depsUnless: ['vinext']`（命名常量 `VINEXT_DEP`）。
- `detectFramework` 循环开头检查 `depsUnless`。
- 新测试：`detect.test.ts` 中 `{ next, vinext, vite }` + `next.config.ts` + `vite.config.ts` → `Framework.VITE`。
- 新增 `.changes/1276-vinext-detected-as-next.md`（`### Fixed`），符合 `.changes/README.md`。

## 验证

依赖安装：`pnpm install --frozen-lockfile --ignore-scripts`（未执行任何 lifecycle 脚本），`pnpm turbo run build --filter=@reticlehq/eslint-plugin... --filter=@reticlehq/init...`。

| 命令 | 结果 |
|---|---|
| (无修复) `cd init && npx vitest run src/detect/detect.test.ts` | ❌ `1 failed \| 41 passed`，`expected 'next' to be 'vite'` |
| (有修复) 同上 | ✅ `42 passed` |
| `pnpm turbo run lint typecheck test:unit --filter=@reticlehq/init` | ✅ 5/5 tasks；91 files / 1060 tests passed |
| `npx prettier --check .` | ✅ |
| `node scripts/check-boundaries.mjs` / `check-lossy-transforms.mjs` | ✅ OK |

未跑：其他包的 test:unit、`pnpm test:e2e`、`pnpm gate:install`（改动仅在 init 的纯检测函数）。

## 如何提交

```bash
gh repo fork reticlehq/reticle --clone && cd reticle
git checkout -b fix/1276-vinext-detected-as-next origin/main
git am /path/to/0001-fix-init-detect-a-Vinext-app-as-Vite-not-Next.js.patch
# 若 main 已前进：git rebase --signoff origin/main
git push -u origin fix/1276-vinext-detected-as-next
gh pr create --repo reticlehq/reticle --head anyingiit:fix/1276-vinext-detected-as-next \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。
