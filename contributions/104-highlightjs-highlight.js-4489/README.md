# highlightjs/highlight.js #4489: CSS-like grammars remaining consistency work（切片：SCSS/Stylus `@keyframes` 的 `from`/`to`）

| 项 | 值 |
|---|---|
| Issue | https://github.com/highlightjs/highlight.js/issues/4489 |
| Tier | 高星 |
| Labels | enhancement, help welcome, language |
| Status | ✅ ready：patch 和 PR 文本已就绪（只做 issue 清单中的一项，PR 写 "Part of #4489"） |
| 重复PR检查 | 2026-10-01：issue 为 open，没有 assignee，评论里也没人认领。`pulls?q=4489` 只找到 #4497（arkgum 的 draft，只给 function 高亮加 markup 测试，不涉及 keyframes）。#4513（选择器转义字符）和 #4545（preserve-3d 数字）也都不涉及 `from`/`to`。按 `keyframes` 关键词只搜到已关闭的 #2936 和 #3301。anyingiit 在该仓库没有 PR。 |
| Base | `main` @ fc3f06392f189354eed922973635ab9e9268b983（2026-08-30） |
| 分支/提交 | `fix/scss-stylus-keyframe-positions` @ d59753b（工作副本：/home/user/work/highlight.js） |

## 问题理解
issue #4489 是 CSS 系语法（css/less/scss/stylus）一致性问题的汇总清单。其中 Sass 一项是 "At-rules highlighting differences (`@keyframes` `from` / `to`)"，Stylus 一项是 "At-rules highlighting (`@font-face`, `@keyframes`, `from`, `to`)"。
在共享测试 `test/markup/*/css_consistency.expect.txt` 中，`@keyframes important1 { from {...} to {...} }` 的 `from`/`to` 在 css 和 less 里是 `hljs-selector-tag`，在 scss 和 stylus 里没有任何标记。css.js 的做法是给顶层加 `keywords: { keyframePosition: "from to" }`，再用 `classNameAliases` 映射成 `selector-tag`。

## 合理性判断
- 维护者在 issue 里明确要求把共享的匹配规则放进 `src/languages/lib/css-shared.js`，不要复制粘贴。这次新增的 `KEYFRAME_POSITION` 就放在共享的 `MODES` 里。
- 没有照搬 css.js 的 keywords 写法。原因：keywords 的默认 `$pattern` 是 `\w+`，`&-leave-to {` 这类 SCSS 嵌套 BEM / Vue transition 选择器里的 `to` 也会被标出来；Stylus 的属性值又写在顶层（不用冒号），误标的风险更大。
- 实际写法是 multi-match：先匹配不加 scope 的前缀 `(?:^|[\s,{}])`，再匹配 `from|to`，要求后面紧跟 `{`、`,` 或行尾（lookahead）。仓库的 `.eslintrc.lang.js` 规定 ecmaVersion 为 2015，lookbehind 过不了 lint（r.js 里相关写法也因此被注释掉），所以用前缀分组代替 lookbehind。这符合 AGENTS.md 的要求：用 lookaround 或 multi-match，不用 `on:begin` 回调。新 mode 用的是 `scope`，没有写 `relevance`。
- 逐项核对过的回归点：
  - SCSS 的 `@for $i from 1 through 3`：已被 scss.js 的 `@` at-rule mode 吞掉，不受影响，测试里有覆盖。
  - `linear-gradient(to right, ...)`：处在属性值 mode 内（scss 的 `:` mode，stylus 的 attribute `starts`），而且后面不是 `{`/`,`/行尾，不受影响，测试里有覆盖。
  - `&-enter-from, &-leave-to`：前一个字符是 `-`，前缀分组不匹配，不受影响，测试里有覆盖。
  - Stylus 缩进语法里单独成行的 `from` / `to` 会被正确标出（`$` 在多行模式下匹配行尾）。

## 改动
- `src/languages/lib/css-shared.js`：`MODES` 中新增 `KEYFRAME_POSITION`（multi-match，scope `{2: 'selector-tag'}`）。
- `src/languages/scss.js`：在 selector-tag mode 后面加 `modes.KEYFRAME_POSITION`。
- `src/languages/stylus.js`：在 tags mode 后面加 `modes.KEYFRAME_POSITION`。
- `test/markup/{scss,stylus}/css_consistency.expect.txt`：`from`/`to` 两行改为与 css 版一致（已用 diff 确认与 css 的 expect 完全相同）。
- 新测试 `test/markup/{scss,stylus}/keyframes.{txt,expect.txt}`：覆盖正例和上面三类反例；stylus 版另外覆盖缩进语法。
- `CHANGES.md`：在 11.12.1（未发布版本，package.json 仍是 11.12.0）下新增 "Core Grammars:" 段，写入 `- fix(scss, stylus) highlight \`from\`/\`to\` keyframe selectors like CSS does, issue #4489 [anyingiit][]`，并在该版本的 CONTRIBUTORS 中加上 `[anyingiit]: https://github.com/anyingiit`。段落顺序与 11.12.0 一致（Core Grammars 在 Documentation 之前）。
- 没有修改 css.js/less.js，也没有碰 #4497（function）、#4513（转义）、#4545（preserve-3d）涉及的区域。

## 验证（Node，工作目录 /home/user/work/highlight.js）
```bash
npm ci
node tools/build.js -t node css less scss stylus
ONLY_LANGUAGES="css less scss stylus" npm run test-markup
```
- Red（`git checkout main -- src`，只保留新测试）：`12 passing, 4 failing`。失败的是 scss/stylus 各自的 `css_consistency` 和 `keyframes`，期望 `<span class="hljs-selector-tag">from</span>`，实际是纯文本 `from`。
- Green（恢复 src）：`16 passing`。
- 全量：`node tools/build.js -t node && npm test`，结果 `1652 passing, 3 pending`，0 failing。`npm test` 包含 markup、detect（自动识别）、api、parser，自动识别没有回归。
- Lint：`npm run lint-languages` 无输出（通过）。`npm run lint` 只有一个原本就有的 warning（`tools/vendor/jquery-2.1.1.min.js` 被忽略）。
- `git apply --check` 已在 `main` 上验证，补丁可以干净地应用。
- **没有运行**：`npm run test-browser`（需要浏览器构建和 headless 浏览器）。本改动只涉及语法定义，风险很低。

## 需要提交者注意
- AI 政策（docs/ai-contributions.md + AGENTS.md）：允许使用 AI，但必须有人工把关、不能是低质量产出（no slop），并鼓励加 `Assisted-by:` trailer。commit 和 PR body 都已写上 `Assisted-by: Claude Code`（AGENTS.md 说明只写工具名也可以；我们的规则禁止出现模型名）。该 issue 是 help welcome，不是 good first issue，所以"不得用 AI 端到端认领 good-first-issue"这条不适用。
- PR 模板里的 "I have read and followed our AI-assisted contributions policy (human review, no slop)" 这一项**故意留空**。请提交者亲自看过 diff 后再勾选。
- 仓库不要求 DCO，也不要求 CLA。
- 这次只做了 issue 清单中的一项，PR 正文写的是 "Part of #4489"，不会自动关闭 issue。如果维护者希望 css.js 也改用这个共享 mode（统一实现），可以在后续 PR 里做。本 PR 刻意不改 css.js 的行为。
- 已知的小局限：
  - 压缩成一行的 SCSS（如 `@keyframes x{from{a:b}to{a:c}}`）中 `from` 和 `to` **都不会**被标出：`from` 前的 `{` 已被 `@keyframes` at-rule mode 消费，`to` 前的 `}` 已被属性值 mode 消费，前缀分组无字符可匹配（复审时用构建产物实测确认）。这是边缘情况，PR 中没有提。
  - Stylus 的属性值/赋值写在顶层，所以 `$x = from` 这种行尾的 `from`/`to` 会被标成 `selector-tag`（复审实测）。这与 stylus 现有行为一致（如 `for i in 1..3` 里的 `i` 本来就被标成 selector-tag），属于可接受的误报。
- CHANGES.md 的条目放在 "Version 11.12.1" 下。如果维护者在合并前发版，可能需要 rebase 并把条目移到新的版本段。

## 如何提交
```bash
git clone https://github.com/highlightjs/highlight.js && cd highlight.js
git checkout -b fix/scss-stylus-keyframe-positions origin/main
git am /home/user/Playground/contributions/104-highlightjs-highlight.js-4489/0001-fix-scss-stylus-highlight-from-to-keyframe-selectors.patch
npm ci && node tools/build.js -t node && npm test && npm run lint-languages
git push -u <your-fork> fix/scss-stylus-keyframe-positions
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/104-highlightjs-highlight.js-4489 highlightjs/highlight.js main fix/scss-stylus-keyframe-positions contributions/104-highlightjs-highlight.js-4489/pr_title.txt contributions/104-highlightjs-highlight.js-4489/pr_body.md
```

## 复审记录（独立 adversarial review，2026-10-01）
- 重新 `npm ci` 后复现 red→green：`git checkout main -- src` 时 `12 passing, 4 failing`（scss/stylus 的 css_consistency 与 keyframes），恢复后 `16 passing`；全量 `node tools/build.js -t node && npm test` 为 `1652 passing, 3 pending`；`npm run lint-languages` 通过；补丁在干净的 `main` 上 `git apply --check` 通过；upstream main 仍为 fc3f063。
- 实测边缘输入：`@include m(from, to)`、`$list: from, to;`、`@each $k in from, to`、注释里的 from/to、`linear-gradient(to right…)`、Stylus `fade(from, to)` 均保持不标；`0%, to {`、`from{` 正确标出。
- 修正：README 中压缩 SCSS 局限的描述（原文称只有 `to` 漏标，实际 `from` 也漏标），补充 Stylus 误报说明；pr_body 的 Checklist 标题改为 brief 规定的 `## Checklist`。

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`（按仓库模板写了 Changes 和 Checklist，并加上 chefs-pick 格式的 Description、Motivation/disclosure 和 Related issue）
