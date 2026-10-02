# Rohithgilla12/data-peek #273 — Export: add a Markdown table format

| 项 | 值 |
|---|---|
| Issue | https://github.com/Rohithgilla12/data-peek/issues/273 |
| Tier | 自由 |
| Labels | enhancement, good first issue, hacktoberfest |
| Status | ✅ ready（patch 和 PR 文本已就绪） |
| 重复 PR 检查 | 2026-10-01：issue 状态为 open，无人分配，没有评论，也没有关联 PR。`pulls?q=273` 只搜到无关的旧 PR，`pulls?q=markdown` 也没有相关 PR，当前没有任何 open 的 PR。main 上的 `ExportFormat` 仍然只有 csv/json/sql。 |
| Base | `main` @ 78a61878（2026-10-01） |

## 问题理解
目前导出只支持 CSV、JSON、SQL。issue 希望加一个 Markdown 表格格式，方便把结果粘贴到 PR、issue 和文档里。具体要求：pipe 转义成 `\|`，换行替换成空格；接入 `serializeExport`，并提供 `.md` 扩展名和 `text/markdown` MIME；导出菜单加一项；补测试（header、分隔行、转义、null）；更新导出文档。完成标准是生成的表格能在 GitHub 上渲染，并且复制到剪贴板可用。

## 合理性判断
- issue 由维护者开出，带 good first issue 和 hacktoberfest 标签，实现步骤也写清楚了。功能很小，没有设计争议。
- CONTRIBUTING 只要求较大的改动先开 issue 讨论，没有要求先评论认领。

## 改动
- `apps/desktop/src/renderer/src/lib/export.ts`
  - `ExportFormat` 增加 `'markdown'`。
  - 新增 `escapeMarkdownCell`：null/undefined 输出空单元格，对象序列化成 JSON（和 CSV 的处理一致），`|` 转成 `\|`，CRLF/CR/LF 替换成空格。
  - 新增 `exportToMarkdown(data)`，输出 GFM 表格。
  - `serializeExport` 增加 markdown 分支；扩展名用 `md`，MIME 用 `text/markdown`。下载和剪贴板复用原有路径。
- `apps/desktop/src/renderer/src/components/export-menu-items.tsx`：增加 Markdown 菜单项（FileText 图标）。结果工具栏和 schema explorer 的表菜单共用这个组件，所以两处都会出现。
- `apps/docs/content/docs/features/export.mdx`：补充 Markdown 格式的说明。示例代码块用的是 ```text：如果用 ```markdown，prettier 会把表格列对齐，示例就和实际输出不一致了。
- 测试：`src/renderer/src/lib/__tests__/export.test.ts` 新增 10 个用例。
- 函数签名和仓库现有的 `exportToCSV(data)` 保持一致，没有照搬 issue 草拟的 `(rows, columns, options)`。PR 正文已说明。

## 验证（Node 22，pnpm 10）
安装：`ELECTRON_SKIP_BINARY_DOWNLOAD=1 pnpm install --frozen-lockfile --ignore-scripts --filter "@data-peek/desktop..."`
- Red（只加测试，不改实现）：`cd apps/desktop && npx vitest run src/renderer/src/lib/__tests__/export.test.ts`，结果 **10 failed | 78 passed**。
- Green：同一条命令，结果 **88 passed**。
- 全量：`npx vitest run --maxWorkers=2`，结果 82 个文件通过、3 个跳过；测试 1398 passed、56 skipped。唯一失败的文件是 `src/main/__tests__/mcp-handlers.test.ts`，报错 "Electron failed to install correctly"。原因是安装时跳过了 Electron 二进制，在 base 上（git stash）同样失败，与本改动无关。
- `pnpm typecheck`（apps/desktop，node + web）：exit 0。
- `npx eslint <3 个改动的 ts/tsx 文件>`：exit 0。`npx prettier --check`（含 mdx）：全部通过。
- 没有跑 `pnpm test:e2e`（需要构建 Electron 和 Docker），也没有手动在 UI 里点过；菜单项只是在现有数组里加了一项。

## 需要提交者注意
- 仓库没有 AI 政策（CLAUDE.md、CONTRIBUTING、.github、labels 都查过）。CLAUDE.md 本身就是给 Claude Code 用的，说明接受 AI 辅助。不需要 DCO，也没有 CHANGELOG。
- 仓库没有要求先评论认领。不过这个 issue 带 hacktoberfest 标签，现在正是 10 月，可能会有人抢着认领，建议提交前再看一眼 issue 和 PR 列表。愿意的话也可以先评论一句再提。
- PR 正文按仓库 PR 模板（Summary/Changes/Type of Change/Checklist/Screenshots）补了相应内容。没有附截图，如果维护者要，可以本地 `pnpm dev` 截一张导出菜单的图。
- 剪贴板复制成功的 toast 会显示 "Copied MARKDOWN export to clipboard"（原逻辑用的是 `format.toUpperCase()`），没有改。

- 复核（2026-10-01，独立复核）：在新的浅克隆（main @ 78a6187）上 `git am` 能干净应用；只回退非测试改动时 10 failed / 78 passed，恢复后 88/88；typecheck、eslint、prettier 都通过；全量 vitest 结果一样（1398 passed，56 skipped，只有 mcp-handlers.test.ts 因为缺 Electron 二进制而失败）。重新抓取了 issue 和 PR 列表：issue 仍为 open，无人分配，0 条评论，没有相关 PR。
- 已知小边界：数据里本身就有 `\|`（反斜杠紧跟竖线）时，会输出 `\\|`，GFM 会把它当成“转义的反斜杠 + 分列符”，导致这一行多出一列。issue 只要求转义 pipe，这种数据也很少见，所以没有改。如果维护者在意，可以在转义 pipe 之前先把 `\` 转成 `\\`。

## 如何提交
```bash
git clone https://github.com/Rohithgilla12/data-peek && cd data-peek
git checkout -b feat/markdown-export origin/main
git am /home/user/Playground/contributions/709-Rohithgilla12-data-peek-273/0001-feat-export-add-Markdown-table-export-format.patch
pnpm install && cd apps/desktop && pnpm test && pnpm typecheck
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/709-Rohithgilla12-data-peek-273 Rohithgilla12/data-peek main feat/markdown-export contributions/709-Rohithgilla12-data-peek-273/pr_title.txt contributions/709-Rohithgilla12-data-peek-273/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
