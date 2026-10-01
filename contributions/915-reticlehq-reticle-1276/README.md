# reticlehq/reticle#1276 — `init` detects a Vinext app as Next.js

| Issue | Tier | Labels | Status | 重复 PR 检查 |
|---|---|---|---|---|
| https://github.com/reticlehq/reticle/issues/1276 | 新锐 | P2, agent-reported, area/init, bug, fw/next, fw/vite, good first issue, hacktoberfest | ✅ ready（patch + PR 文本已就绪） | 无：`is:pr 1276`、`is:pr vinext` 均 0 结果；issue 无 assignee、无评论（2026-10-01 核实） |

## 问题理解
Vinext 应用依赖 `next`（只用它的 API），但用 Vite 构建。`init/src/detect/detect.ts` 中 `DETECTION_ORDER` 把 NEXT 放在 VITE 前，于是被识别为 Next，`init` 把 `withReticle` 写进 Vinext 根本不执行的 `next.config`，应用永远连不上。issue 给出的验收标准：`{ next, vinext, vite }` 的 fixture 被识别为 Vite（或独立条目但应用 Vite 插件），并附测试。

## 合理性判断
维护者标了 bug + good first issue，验收标准清晰；仓库已有同类先例（Nuxt/SvelteKit/Remix 等都靠检测顺序或 `configsUnless` 排除），改动符合现有设计。

## 改动
- `FrameworkSignals` 新增可选 `depsUnless`：出现这些依赖时，该框架的依赖信号和配置文件信号都不算。
- `Framework.NEXT` 声明 `depsUnless: ['vinext']`，`detectFramework` 循环开头检查并 `continue`。这样即使项目保留 `next.config.ts` 也会落到 Vite。
- 新增回归测试（detect.test.ts）和 changelog 片段 `.changes/1276-vinext-detected-as-next.md`（仓库要求，不改 CHANGELOG.md）。

## 验证
- 安装：`pnpm install --frozen-lockfile --ignore-scripts`；为 lint 先 `npx turbo run build --filter=@reticlehq/eslint-plugin`（否则 eslint.config.mjs 找不到 dist，属环境问题）。
- RED：修复前 `cd init && npx vitest run src/detect/detect.test.ts` → `1 failed | 41 passed`（Expected "vite", Received "next"）。
- GREEN：修复后 → `42 passed`。
- `npx turbo run lint typecheck test:unit --filter=@reticlehq/init` → 5/5 成功，91 个测试文件 / 1060 个测试全部通过。
- `node scripts/check-boundaries.mjs`、`node scripts/check-lossy-transforms.mjs`、`npx prettier --check .` 全部通过。
- 未运行：整个 monorepo 的 `pnpm test:unit`、`pnpm gate:install`、e2e（耗时长/需网络与 fixtures）。

## 需要提交者注意
- **DCO 必须**：CI 会检查 `Signed-off-by`。patch 已带 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`，与 commit 作者一致；如果你用其他邮箱提交，请 `git commit --amend -s --reset-author` 重新签名。
- **AI 贡献政策**（CONTRIBUTING “AI-assisted contributions”）：允许，条件是测试在去掉修复后必须失败，并在 PR 描述里说明已检查过——pr_body.md 的 “How it was verified” 已写明。
- 认领规则：CONTRIBUTING 说“在 issue 下评论认领”。提交前可先在 issue 留一句评论（可选），并再检查一下是否已有人开 PR。
- PR 模板中的 `pnpm gate:install` 涉及 init，本地未跑，PR 中已注明交给 CI。
- 用 rebase 更新分支，不要 merge main（仓库使用 merge queue）。
- 设计取舍：按 issue 的验收标准，Vinext 走通用 Vite 路径（Vite 插件的 `transformIndexHtml` 注入）。如果维护者认为 Vinext 的 SSR 页面需要像 Remix/TanStack Start 那样走 client-entry 注入，可能需要后续单独的 Framework 条目——如果 review 中提到，再跟进。

## 如何提交
```bash
git clone https://github.com/anyingiit/reticle && cd reticle   # 先在 GitHub 上 fork reticlehq/reticle
git remote add upstream https://github.com/reticlehq/reticle && git fetch upstream
git checkout -b fix/init-vinext-detection upstream/main
git am /path/to/0001-fix-init-detect-a-Vinext-app-as-Vite-not-Next.js.patch
git push -u origin fix/init-vinext-detection
gh pr create --repo reticlehq/reticle --base main --head anyingiit:fix/init-vinext-detection \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```
基础分支：`main`（基于 14085e6，v3.5.0）。

## PR title
见 `pr_title.txt`：`fix(init): detect a Vinext app as Vite, not Next.js`

## PR body
见 `pr_body.md`（已按仓库 `.github/PULL_REQUEST_TEMPLATE.md` 结构填写，并包含 motivation/disclosure 段落）。
