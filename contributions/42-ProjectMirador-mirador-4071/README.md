# ProjectMirador/mirador#4071 — canvasIndex should override manifest startCanvas

| Item | Value |
|---|---|
| Issue | https://github.com/ProjectMirador/mirador/issues/4071 |
| Tier | 自由 |
| Repo | ProjectMirador/mirador (~620 stars, JS, Apache-2.0; maintainers from Stanford etc. merge outside PRs) |
| Labels | audit-2026, good first issue, ready for dev |
| Status | ✅ done — patch + PR text ready |
| Duplicate-PR check | 2026-09-24 (start and again before finishing): no open/closed PR for #4071; no open PR touches `setWindowStartingCanvas`. Related-but-different open PR #4528 (`preserveInitialCanvasOnSearch`, changes `setCanvasOfFirstSearchResult` only) — may need a trivial rebase in `__tests__/src/sagas/windows.test.js` if it lands first. Issue unassigned, 0 comments. |
| Base | `main` @ b4602a7 |
| Patch | `0001-Let-a-configured-canvasIndex-override-the-manifest-s.patch` |

## 需要提交者注意

- CONTRIBUTING.md 有 **AI Policy**：允许 AI 辅助，但提交者必须完全理解并对改动负责，**用自己的话**回复 review（不要直接粘贴 AI 回复）。PR 正文已包含披露段落；请在提交前通读改动。
- 无 CLA/DCO 要求；提交信息风格为普通祈使句（无 Conventional Commits）；无 CHANGELOG 文件、无 PR 模板。
- 开 PR 前请确认 #4528 是否已合并（若已合并，`git am` 可能在测试文件同一位置产生冲突，手动保留两边新增的测试即可）。

## 问题理解

`src/state/sagas/windows.js` 的 `setWindowStartingCanvas` 在窗口没有显式 `canvasId` 时计算起始画布：

```js
miradorManifest.startCanvas || miradorManifest.canvasAt(canvasIndex || 0) || miradorManifest.canvasAt(0)
```

只要 manifest 带 `startCanvas`（IIIF v2）/ `start`（IIIF v3），用户在窗口配置里写的 `canvasIndex` 就被无视，无法覆盖。Issue 作者给出的建议写法是 `canvasIndex ? canvasAt(canvasIndex) : startCanvas || canvasAt(0)`。

## 合理性判断

- 维护者已打 `ready for dev` + `good first issue`，并纳入 audit-2026 项目；`canvasIndex` 是窗口级的显式用户配置，而 `startCanvas` 是 manifest 默认值，显式配置优先符合直觉，也与 `canvasId`（已优先于 startCanvas）的行为一致。
- 当前 main 仍是旧逻辑，未修复。

## 改动

- `canvasIndex != null && canvasAt(canvasIndex)` 优先；否则回退到 `startCanvas`，再回退到第一个画布。
- 相比 issue 中的建议做了两点改进（PR 中已说明）：
  1. `canvasIndex: 0` 也视为显式覆盖（issue 写法中 0 是 falsy，会被忽略）；
  2. 越界/无效 index 不会导致 `startCanvas` 变成 `undefined`（issue 写法会让窗口不设置画布），而是回退到 manifest start canvas。
- `!= null` 与代码库中 `OpenSeadragonComponent.jsx` 的写法一致，并保持以前 `canvasAt("2")` 这种字符串 index 仍可用。
- 新增 3 个 saga 测试（`__tests__/src/sagas/windows.test.js`）。

## 验证

环境：Node 22.22.2，npm 10.9.7，`npm ci --ignore-scripts`。

| 命令 | 结果 |
|---|---|
| 未修复源码 + 新测试：`npx vitest run __tests__/src/sagas/windows.test.js` | ❌ 2 failed / 28 passed（"prefers an explicitly configured canvasIndex…"、"treats a canvasIndex of 0…"；越界回退测试在旧代码下也通过——它是防回归护栏） |
| 修复后：同上 | ✅ 30 passed |
| `npm run build` | ✅ |
| `npm run lint`（eslint + i18n + container lint） | ✅（i18n-lint 打印的 missing keys 是既有输出，不影响退出码） |
| `npm run size` | ✅ 567.29 kB gzipped / limit 732 kB |
| `npx prettier --check` 改动文件 | ✅（全仓 `prettier --check .` 仅报既有的 `src/config/css-ns.js`，base 上同样） |
| 单元测试全集 `npx vitest run --exclude '__tests__/integration/**'` | ✅ 1239 passed / 5 skipped（4 次运行中有 1 次出现 1 个随机失败的测试，vitest 开启了 shuffle；其余 3 次全绿，与本改动无关） |
| 完整 `npm test`（CI 命令） | build/lint/size 通过；vitest 1251 passed，**7 failed 均为 `__tests__/integration/**`** |
| 集成测试在 **base (main)** 上：`npx vitest run __tests__/integration` | 10 failed / 9 passed（补丁分支上 9 failed）——集成测试需要访问 purl.stanford.edu 等真实 IIIF 服务器以及 `localhost:4444` dev server，本沙箱中超时 / ECONNREFUSED，属环境问题，与改动无关 |

## 如何提交

```bash
git clone https://github.com/ProjectMirador/mirador.git && cd mirador
git checkout -b 4071-canvasindex-over-startcanvas origin/main
git am /path/to/0001-Let-a-configured-canvasIndex-override-the-manifest-s.patch
npm ci && npx vitest run __tests__/src/sagas/windows.test.js
git push <your-fork> 4071-canvasindex-over-startcanvas   # 然后对 main 开 PR
```

## PR title

Let a configured canvasIndex override the manifest start canvas

## PR body

```markdown
## Description

When a window has no explicit `canvasId`, `setWindowStartingCanvas` picked the starting canvas as
`startCanvas || canvasAt(canvasIndex || 0) || canvasAt(0)`, so as soon as a manifest declares a
`startCanvas` (IIIF v2) / `start` (IIIF v3), a `canvasIndex` set in the window config is silently ignored.

This changes the precedence to: explicitly configured `canvasIndex` → manifest start canvas → first canvas.

Two small differences from the snippet suggested in the issue:

- `canvasIndex: 0` counts as an explicit choice (with `canvasIndex ? ... : ...` a configured `0` would be
  ignored and the manifest start canvas would win again).
- If `canvasIndex` doesn't match a canvas (e.g. out of range), we fall back to the manifest start canvas /
  first canvas instead of ending up with no starting canvas at all.

Tests added in `__tests__/src/sagas/windows.test.js` for: `canvasIndex` beating the manifest `start`,
`canvasIndex: 0`, and an out-of-range `canvasIndex` falling back to `start`. The first two fail on `main`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #4071

## Checklist

- [x] Tests pass locally (`npx vitest run __tests__/src/sagas/windows.test.js`: 30 passed, 2 of the new tests fail without the fix; `npm run build`, `npm run lint`, `npm run size` pass; unit suite `npx vitest run --exclude '__tests__/integration/**'`: 1239 passed / 5 skipped. The `__tests__/integration` tests couldn't run in my sandbox — no access to the remote IIIF servers — and fail the same way on `main` there)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog file
- [ ] Documentation is updated (if applicable) — n/a, no docs describe the old precedence
```
