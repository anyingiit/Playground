# rjsf-team/react-jsonschema-form#3882 — Enable checkbox widget for string field with const

| 项 | 值 |
|---|---|
| Issue | https://github.com/rjsf-team/react-jsonschema-form/issues/3882 |
| Tier | 高星 |
| Labels | core, feature, help wanted |
| Status | ✅ ready — patch + PR text done (not submitted); independently reviewed 2026-10-01 |
| Base | `main` @ 7466db4 (2026-10-01, "Upgrade @x0k/json-schema-merge to 1.1.0 … (#5417)") |
| Duplicate-PR check | 2026-10-01：`pulls?q=3882` 0 结果；关键词 `checkbox const` / `const string checkbox` 搜索只命中 #5400（CheckboxesWidget realValue/焦点值，与本 issue 无关）；issue 无评论、未分配、无关联分支/PR |

## 问题理解

Issue 提出：对于 `{"type":"string","const":"foo"}` 这样的字段，希望可以 `ui:widget: "checkbox"` 渲染为复选框——勾选时值为 const，取消勾选时从数据中去掉该属性。目前 `getWidget` 的 `widgetMap.string` 中没有 `checkbox`，所以会抛 `No widget 'checkbox' for type 'string'`（文档 widgets.md 也只列 boolean 可用 checkbox）。

## 合理性判断

- 维护者标了 `feature` + `help wanted` + `core`，需求行为在 issue 中已描述清楚，无需额外设计讨论。
- 仓库有 CLAUDE.md（面向 Claude Code 的开发指南），CONTRIBUTING / PR 模板 / label 描述均无 AI 禁令。
- 遵循 CLAUDE.md：逻辑放在 core（所有主题共享），默认不写注释、仅写"为什么"的注释；changelog 追加到对应包标题下；CI 顺序 lint → knip → build → typecheck → test。

## 改动

- `packages/core/src/components/fields/StringField.tsx`：当 `ui:widget === 'checkbox'` 且 `schema.const` 为字符串时：
  - 使用 registry 的 `CheckboxWidget`（若用户注册了名为 `checkbox` 的 widget 则用它）；
  - 传给 widget 的 `value` 为 `formData === schema.const`（布尔）；
  - `onChange`/`onBlur`/`onFocus` 把布尔映射回字符串：true → const，false → `undefined`（与清空文本框相同，提交时该键被丢弃）。
  - 其它情况行为不变（无 const 的 string 仍然抛错）。
- 设计取舍：未改 `@rjsf/utils` 的 `widgetMap`（否则无 const 的字符串也能选 checkbox，值语义会错）。
- `packages/core/test/StringField.test.tsx`：新增 `describe('CheckboxWidget with const')` 共 7 个测试（渲染、选中状态、非 const 值不选中、默认 constAsDefaults 下初始选中、勾选/取消的 formData、focus/blur 值、required 校验）。
- `packages/docs/docs/usage/widgets.md`：string 小节增加 `checkbox` 说明（含 constAsDefaults 默认 `always` 导致初始勾选的说明）。
- `packages/playground/src/samples/widgets.tsx`：新增 `confirmation` 示例字段（PR 模板 "adding a new feature" 要求）。
- `CHANGELOG.md`：`# 6.11.1` 改为 `# 6.12.0`（新功能 → minor，按 changelog 顶部说明），新增 `## @rjsf/core` 条目和 `## Dev / docs / playground` 条目。

## 验证

环境：Node 22.22.0、pnpm 10.17.1；`CI=1 pnpm install --frozen-lockfile --store-dir <work>/.pnpm-store --child-concurrency 2`。

| 命令 | 结果 |
|---|---|
| 仅回退 `packages/core/src`，保留新测试：`cd packages/core && npx vitest run test/StringField.test.tsx` | **7 failed** / 154 passed（`No widget 'checkbox' for type 'string'`）→ red |
| 打补丁后同一命令 | 161 passed → green |
| `cd packages/core && npx vitest run --maxWorkers=2`（= 包内 `pnpm test`） | 36 files, 2089 passed |
| `cd packages/playground && npx vitest run --maxWorkers=2` | 10 passed |
| `cd packages/core && npx oxlint src test`；`cd packages/playground && npx oxlint src` | rc=0，只有已存在的 warning，改动文件 0 条 |
| `npx oxfmt --check <5 个改动文件>` | All matched files use the correct format |
| `pnpm run typecheck`（根 `tsc --build`，覆盖测试工程） | 通过 |
| `pnpm run knip` | 通过 |
| 临时探针（未提交）：在 `@rjsf/mui`、`@rjsf/antd` 中渲染该 schema，勾选/取消 | 通过（chakra-ui 探针因测试需 ChakraProvider 包装未跑） |
| `git am` 到干净的 7466db4 | 成功 |

未运行：全仓 `pnpm run build-serial` / 所有主题的 `pnpm test`（耗时大；改动只在 core StringField，主题未改，snapshot 测试的 schema 不含此场景）、`mkdocs build`（docs 只加一行 bullet，链接 `../api-reference/form-props.md#constasdefaults` 与已有写法一致）。

### 独立复核（2026-10-01 20:30 UTC）

- upstream `main` 仍为 7466db4；`pulls?q=checkbox const` 复查无相关新 PR，issue 仍无评论/关联 PR。
- 重新 `pnpm install` 后复跑：回退 `packages/core/src` → `npx vitest run test/StringField.test.tsx` **7 failed**（`No widget 'checkbox' for type 'string'`）；恢复后 161 passed；`packages/core` 全量 36 files / 2089 passed；`oxfmt --check` 5 个文件通过；`oxlint src test` 改动文件无 warning；`pnpm run typecheck` 通过。
- 复核要点：`required` 属性仅在字段被 `required` 时设置（CheckboxWidget 用 `schemaRequiresTrueValue(schema) && required`），可选 const 字段不会被 HTML5 校验阻止提交；`ui:widget` 为组件时不受影响；PR 正文使用仓库模板要求的 `fixes #3882` 语法。未发现需要修改的问题。

## 如何提交

```bash
git clone https://github.com/rjsf-team/react-jsonschema-form && cd react-jsonschema-form
git checkout -b fix-3882-const-string-checkbox origin/main
git am /path/to/0001-Fix-3882-render-a-checkbox-for-a-string-with-a-const.patch
git push <your-fork> fix-3882-const-string-checkbox   # PR 目标分支: main
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`（已按仓库 `PULL_REQUEST_TEMPLATE.md` 的 "Reasons for making this change" + Checklist 结构，并含 disclosure 段落）。

### 需要提交者注意
- 无 DCO、无 AI trailer 要求；提交信息沿用仓库常见的 `Fix <issue>: ...` 风格。
- CHANGELOG：仓库很活跃，`# 6.11.1`→`# 6.12.0` 的标题改动和条目位置在提交前很可能需要 rebase 解决冲突；若届时已有 `## @rjsf/core` 或 `## Dev / docs / playground` 小节，按 CLAUDE.md 规则把条目追加为该小节的最后一条。
- PR 模板中 "checked the rendering of the Markdown" 未勾选（本地没跑 mkdocs）；如有条件可本地预览后勾选。
- 行为说明：默认 `constAsDefaults: 'always'` 会把 const 作为默认值写入，所以复选框初始是勾选的；这是现有默认值机制的结果，已在文档和 PR 描述里说明，维护者可能有不同偏好。
- husky pre-commit 钩子在提交时被跳过（`core.hooksPath=/dev/null`），但已手动跑过同等的 oxlint/oxfmt。
