# inokawa/remark-pdf#61 — Table cells in a row are not stretched to the row height

| | |
|---|---|
| Issue | https://github.com/inokawa/remark-pdf/issues/61 |
| Tier | 自由 |
| Repo | inokawa/remark-pdf (remark plugin: Markdown → PDF, TypeScript; maintainer inokawa also maintains virtua etc.) |
| Labels | `good first issue` |
| Status | ✅ 实现 + 测试通过 + PR 文案就绪 |
| 重复 PR 检查 | 无。issue 无评论/assignee，Development 栏 "No branches or pull requests"；open PR 只有 renovate 的 #68/#69/#71 和维护者自己的 #33（无关）。开工前 + 完成前各检查一次（2026-09-24） |
| AI 政策 | 仓库无 AGENTS.md / CLAUDE.md / CONTRIBUTING；grep `LLM/AI-generated/Copilot/ChatGPT/claude` 无命中 → 无禁止 |

## 问题理解
Markdown 表格里某一格文字换行时，行高取最高那格（`rowHeight`），但其它格的 `BlockBox` 仍保留各自的内容高度。
每个 table-cell 的 box 是 `border: true`，由 `paintBlockBox` 用自己的 `height` 画矩形边框 → 短格子的边框在行底之上就结束，表格网格断开（见 `before.png`）。

注意：issue 里说根因在 `src/mdast-util-to-pdf.ts`，但重构后布局代码已搬到 `src/layout.ts`（`layoutBlock` 的 `case "table"`）。

## 合理性判断
- 纯渲染 bug，issue 给出了最小复现和建议修法（算完行高后把所有 cell 拉伸到行高），维护者打了 `good first issue`。
- 当前 main（3c36bf5）仍可复现（本地渲染 before.png 确认）。
- 外部贡献者的 PR 过去被合并过（James Zetlen #13–#16、Georgios Petasis #12、Alan007BR）；近期 PR 主要来自维护者和 renovate，仓库仍活跃（2026-08 仍有提交）。

## 改动
- `src/layout.ts`：table 行的 `children` 由 `rowChildren` 改为 `rowChildren.map((c) => ({ ...c, height: rowHeight }))`（1 行 + 注释）。只改 cell 外框高度，内部文字 box 位置不变，行/表高度计算不变。
- 新增 `src/layout.spec.ts`：直接对 `layoutBlock` 做单元测试（mock `textWidth`/`textHeight`，不依赖 PDF 渲染），断言每行所有 cell 的 `y`/`height` 等于行的 `y`/`height`，且第一行因换行更高。

## 验证
环境：Node 22.22.2 / npm 10.9.7，`npm ci --ignore-scripts`。CI（`.github/workflows/check.yml`）= `npm ci && npm run tsc && npm run test && npm run build`。

| 命令 | 结果 |
|---|---|
| `npx vitest run layout.spec.ts`（未修复） | ❌ 1 failed（cell 高度 ≠ 行高）— **red** |
| `npx vitest run layout.spec.ts`（修复后） | ✅ 1 passed — **green** |
| `npm run tsc` | ✅ 无错误 |
| `npm run test`（修复后） | 14 passed / 9 failed |
| `npm run test`（base 分支，未修改） | 13 passed / 9 failed —— **同样的 9 个 e2e 图像快照失败**，且差异像素数完全相同（1/20/20/5/1/12/3/24/6 像素，≤0.005%），是本机字体栅格化与 CI 环境差异，与本改动无关 |
| `npm run build` | ✅ `created lib`（有一个既存的 TS5069 warning） |
| 手动渲染 issue 复现 Markdown | `before.png` 边框断开 → `after.png` 网格整齐 |

`fixtures/article.md` 中已有的表格每行各格等高，因此 e2e 快照不受影响（上表的差异像素数修复前后一致即证明）。

## 如何提交
```bash
git clone https://github.com/<you>/remark-pdf && cd remark-pdf
git checkout -b fix/table-cell-row-height origin/main
git am /path/to/0001-Stretch-table-cells-to-the-row-height.patch
git push -u origin HEAD   # base: main
```
PR 里可以附上 `before.png` / `after.png`（拖进 PR 描述即可）。

### 需要提交者注意
- 仓库没有 PR 模板、CHANGELOG 或 changeset；提交信息风格为简单祈使句（如 "Fix build"），已照此编写。
- 无 DCO 要求。

## PR

**Title:** `Stretch table cells to the row height`

```markdown
## Description

When one cell in a table row wraps onto several lines, the row height grows to fit it, but the other
cells in that row kept their own (shorter) content height. Since each table cell paints its own border
from its box height, the shorter cells' borders stopped above the bottom of the row and the table grid
looked broken.

`layoutBlock` already computes `rowHeight` for every row (`src/layout.ts`, `case "table"`); the row's
cell boxes are now stretched to that height before they are stored. Only the cell box height changes —
text positions and the row/table heights are unchanged, so tables whose cells already have equal heights
(e.g. the one in `fixtures/article.md`) render exactly as before.

Added `src/layout.spec.ts`, a small unit test for `layoutBlock` that checks every cell in each row has
the row's `y` and `height`. It fails without the fix and passes with it.

| Before | After |
|---|---|
| <before.png> | <after.png> |

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #61

## Checklist

- [x] Tests pass locally (`npm run tsc` clean; `npx vitest run layout.spec.ts` fails before / passes after
      the fix; `npm run build` OK. In `npm run test`, 9 e2e image snapshots differ by 1–24 pixels on my
      machine both with and without this change — same tests, same pixel counts — so that's local font
      rasterisation, not this PR)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, bug fix with no API change
```
