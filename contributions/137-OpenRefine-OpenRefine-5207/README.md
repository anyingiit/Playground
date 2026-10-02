# OpenRefine/OpenRefine#5207 — Add a new Hidden Chars facet

| 项 | 值 |
|---|---|
| Issue | https://github.com/OpenRefine/OpenRefine/issues/5207 |
| Tier | 高星 |
| Labels | Type: Feature Request, facets, help wanted |
| Status | ✅ ready（功能型 PR，设计上有可讨论点，见“需要提交者注意”） |
| Base commit | `c8d04c3c7f03f3fe321954134c468c18ae21d13e`（master, 2026-09-30） |
| 分支名建议 | `5207-hidden-chars-facet`（CONTRIBUTING 要求分支名含 issue 号） |
| 重复 PR 检查 | `pulls?q=5207` 无相关 PR；关键词 `hidden char` / `invisible` / `"hidden characters"` 只有已合并的 #5442（聚类里的转义显示，不同功能）和已关闭的 #4758、#4802；issue 无 assignee、无评论、无人认领（2026-10-01 查） |

## 问题理解

Issue（thadguidry, 2022-08-22，无评论）希望新增一个 facet：列出某列单元格中出现的“隐藏/不可见”Unicode 字符的转义码（如 `\u00A0`），字符集参考 VS Code 的 hediet/vscode-unicode-data；选中某个码即可看到含该字符的行，再用 GREL 清理。`showHiddenChars()` / `removeHiddenChars()` 是“以后可以做”的扩展，不在本 issue 必需范围内。

## 合理性判断

- 维护者本人（thadguidry）提的 Feature Request，标签 `help wanted` + `facets`，至今 open，说明项目希望有人做。
- AI 政策：仓库有 `AGENTS.md` 和 `.github/copilot-instructions.md`（面向 AI agent 的开发说明，未禁止）；CONTRIBUTING / 贡献指南无 AI 条款；论坛讨论 “How do you deal with AI generated PRs?”（2025-09 ~ 2026-05）结论是不禁止，但要求 **披露** 且认真使用（Tom Morris: “disclosed and used in a thoughtful way”），并有人提议“先被 assign 再提 PR”，但未写入贡献指南。
- 贡献指南建议“新功能先在论坛/issue 讨论”。本实现选择最小、无后端改动的做法（复用现有 GREL 函数的 customized facet），设计点都在 PR 中明确列出供维护者决定。

## 改动

1. `main/webapp/modules/core/scripts/views/data-table/menu-facets.js`：在 *Facet → Customized facets* 中 “Unicode char-code facet” 之后新增 “Hidden characters facet”（list facet），表达式：
   `forEach(value.find(/[<隐藏字符类>]/), c, c.escape('javascript'))`
   - 字符类 = VS Code 不可见字符集（U+00A0、U+00AD、U+034F、U+061C、U+115F/1160、U+17B4/17B5、U+180B–180F、U+1CBB/1CBC、U+2000–200F、U+2028–202F、U+205F–206F、U+2800、U+3000、U+3164、U+FE00–FE0F、U+FEFF、U+FFA0、U+FFF0–FFF8、U+FFFC、U+1D173–1D17A、U+E0000–E007F、U+E0100–E01EF）+ C0/C1 控制符；**不含** Tab、LF、普通空格（避免普通多词/多行单元格刷屏）。CR 包含（VS Code 也包含）。
   - `escape('javascript')`（commons-text `escapeEcmaScript`）输出 `\uXXXX` 形式；BMP 外字符显示为代理对。
   - 没有隐藏字符的行返回空数组，不出现在 facet 中（实测，无 “(blank)” 项）。
2. `main/webapp/modules/core/langs/translation-en.json`：新增 `core-views/hidden-chars-facet`（其他语言走 Weblate）。
3. 新测试 `main/tests/cypress/cypress/e2e/project/grid/column/facet/customized-facets/hidden-chars-facet.cy.js`（该目录此前只有 `.gitkeep`）：构造含 NBSP、ZWSP、BOM、Tab 的列，断言 facet 选项恰为 `\u00A0`:2、`\u200B`:1、`\uFEFF`:1，点击 `\u00A0` 后 “2 matching rows”。测试中用 `String.fromCodePoint` 构造字符（prettier 3.9 会把字符串里的 `\u` 转义改写成真实不可见字符）。

## 验证

环境：JDK 21、Maven（`-Dmaven.repo.local` 放在 work 目录）、Node 22（package.json engines 要求 24，但 yarn 4 不强制，运行正常）、yarn 4.18 via corepack、Cypress 16.1.0（electron，headless）。

```bash
./refine build                                 # exit 0
# 运行单个 spec（refine 脚本自动起服务器、跑 cypress、关服务器）
CYPRESS_SPECS=cypress/e2e/project/grid/column/facet/customized-facets/hidden-chars-facet.cy.js ./refine e2e_tests
```

- **Red**（stash 掉 menu-facets.js 与 translation-en.json，只保留测试）：`0 passing, 1 failing` — `Expected to find content: 'Hidden characters facet' within the element: <div.menu-container> but never did.`
- **Green**（带改动）：`1 passing`（commit amend 后再跑一次仍 `1 passing`）。
- 回归：facet 目录全部 spec（`hidden-chars-facet`, `facets`, `facets.numeric`, `scatterplot-facet`）→ 1 + 22 + 4 + 2 = 29 passing，1 failing：`facets.cy.js` “Test collapsing facet panels”。在 **未改动的 master** 上单独跑 `facets.cy.js` 结果相同（22 passing / 同一个 failing），属于本环境的既有问题，与本改动无关。
- Lint（CI `pull_request_e2e.yml` 中的 `yarn lint`，在 `main/tests/cypress`）：`prettier --check` 通过；`eslint` 0 errors（10 个 warnings 都在其他既有文件）。`./refine lint` / `formatter:validate` 只针对 Java，本次没有 Java 改动，未运行。
- `git am` 到 base commit 的干净 worktree 验证可应用。
- 截图：`screenshot-hidden-chars-facet.png`（Cypress 截取，选中 `\u00A0` 后的效果）。

## 如何提交

```bash
git clone https://github.com/<you>/OpenRefine.git && cd OpenRefine
git remote add upstream https://github.com/OpenRefine/OpenRefine.git && git fetch upstream
git checkout -b 5207-hidden-chars-facet upstream/master
git am /path/to/contributions/137-OpenRefine-OpenRefine-5207/0001-Add-a-hidden-characters-facet-to-the-customized-face.patch
git push origin 5207-hidden-chars-facet
# 在 GitHub 上开 PR → OpenRefine/OpenRefine:master，标题用 pr_title.txt，正文用 pr_body.md，
# 并把 screenshot-hidden-chars-facet.png 拖进正文的截图占位处。
```

## 需要提交者注意

- **AI 披露是必须的**（论坛共识：可以用，但要披露、要认真）。pr_body.md 已含披露段落，请保留。
- 有人在论坛提议“先 assign 再提 PR”，目前未成文；稳妥起见可先在 issue 下留言说明打算（由你本人发）再开 PR。
- 这是 feature 而非 bug fix，维护者可能对 **菜单位置/名称** 和 **字符集**（是否包含 CR、C0/C1 控制符；是否改成后端 GREL 函数，如 issue 提到的 `showHiddenChars()`）有不同意见，PR 正文已列出这些点。
- CONTRIBUTING 要求 UI 改动附截图：请上传 `screenshot-hidden-chars-facet.png`。
- 用户文档在另一个仓库 OpenRefine/openrefine.org（Customized facets 一节），PR 被接受后可以补一个文档 PR。
- 无 DCO / Signed-off-by 要求；commit 作者为 anyingiit。
- `facets.cy.js` “Test collapsing facet panels” 在本地 master 上也失败，若 CI 里通过则无需在意。

## 独立复核（reviewer, 2026-10-01）

- 重新 WebFetch issue 与 `pulls?q=5207`：仍 open、无 assignee、无重复 PR。
- 代码审查：GREL 正则字面量的 Scanner 原样保留反斜杠，交给 Java `Pattern`，`\uXXXX` 与 `\x{1D173}` 都被支持；用 Java 单独验证字符类：`a b\tc d\ne\r<U+E0041>‍\u0085 é 中` 只匹配 A0、0D、E0041、200D、85（Tab/LF/空格/普通非 ASCII 不匹配）。`find()` 对 null 返回空数组、对非字符串先 `toString()`，因此数字/空单元格不会产生 error 项。
- 亲自重跑：`./refine build` exit 0；红（`git checkout HEAD~1 -- menu-facets.js translation-en.json`）→ `0 passing, 1 failing`（`Expected to find content: 'Hidden characters facet'`）；绿（恢复改动）→ `1 passing`。`main/tests/cypress` 下 `yarn prettier --check .` 通过，`yarn eslint .` 0 errors，新文件无 warning。
- `git am` 到 `c8d04c3` 干净应用，作者 anyingiit，无 AI 模型名；PR 模板（`Fixes #…` + “Changes proposed”）已遵循。
- 结论：无需修改，Status 保持 ✅ ready。
