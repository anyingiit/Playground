# conventional-changelog/commitlint #3294 — start-case 拒绝含句点/数字的 subject

| 项 | 值 |
|---|---|
| Issue | https://github.com/conventional-changelog/commitlint/issues/3294 |
| Tier | 高星 |
| Labels | bug, help wanted |
| Status | ✅ ready（已独立复审）— 两个 patch（test + fix）和 PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：`pulls?q=3294` 结果为 0。`pulls?q=is:pr+start-case` 只有 #5010（已关闭，它处理的是 #3501）和 #4962（已合并，只改了错误信息）。当前 open PR 共 4 个，都不涉及 ensure。issue 无人分配。 |
| Base | `master` @ 0737aba（2026-10-01） |

## 问题理解
配置 `'subject-case': [2, 'always', 'start-case']` 时，`feat: Add Module 1.0.0` 会报错。原因是 `@commitlint/ensure/src/case.ts` 用 `toCase(input, target) === input` 做比较，而 start-case 对应 es-toolkit 的 `startCase()`，它会在句点和数字处拆词：`Add Module 1.0.0` 变成 `Add Module 1 0 0`，`Add Core.js` 变成 `Add Core Js`。目前唯一的绕过办法是把版本号加引号（引号里的内容会被先剔除）。

## 合理性判断
- issue 带 bug 和 help wanted 标签，没有人认领，也没有已有的 PR。
- 避开了 #5010 的坑：escapedcat 关闭 #5010 的原因是它让原本能通过的提交变成失败。本改动只放宽 start-case，规则是：
  - 所有原来能通过 start-case 的单词仍然通过，因为每个单词先走 `startCase(word) === word`。
  - 单词 `fix: Typo`、`chore: Release` 仍然通过，测试里有覆盖。
  - sentence-case 及其他 case 的行为完全不变。
  - `toCase()` 没有改，所以 prompt 和 cz-commitlint 的强制大小写也不受影响。
- 依然拒绝的情况，测试里都写明了：
  - 小写词：`module`、`core.js`、`v1.0.0`
  - 驼峰：`FooBar.js`
  - 含 `_` 或 `-` 的词：`Foo_bar`、`Foo-bar`、`Foo_bar.js`、`foo_bar`
  - 连续两个空格：`Add  Module 1.0.0`（与原行为一致）

## 改动
- `@commitlint/ensure/src/case.ts`：
  - 原有的提前返回（结果为空或以数字开头时直接通过）保持不变。
  - target 为 `start-case` 时，改为按空格（`split(" ")`）逐词检查 `isStartCaseWord`：
    1. `startCase(word) === word` 时通过，与原逻辑一致；
    2. 否则，如果单词满足 `^(\p{L}*)[\d.][\p{L}\d.]*$`（第一个句点或数字之前是纯字母，之后只有字母、数字、句点），那么前缀为空时要求单词以数字开头，前缀非空时要求前缀本身是 start case。
  - 连续两个空格会产生空词；`isStartCaseWord("")` 显式返回 false，所以 `Foo  Bar` 仍然失败，与原行为一致（复审时修正：初版会放行双空格）。tab 等其他空白字符也仍然失败。
- `@commitlint/ensure/src/case.test.ts`：新增 13 条 start-case 用例（含双空格回归用例）。
- `@commitlint/rules/src/subject-case.test.ts`：新增 rule 级用例 `feat: Add Module 1.0.0`。
- 文档没有改：docs/reference/rules.md 只列了 case 名称，没有细节。CHANGELOG 由 lerna 自动生成。

## 验证（Node 22.22.0，pnpm 12.8.0）
```bash
cd /home/user/work/commitlint
pnpm install --frozen-lockfile --ignore-scripts --store-dir ./.pnpm-store
pnpm build   # tsc -b；rules 用的是 ensure 的 lib 产物，改完要先 build
pnpm vitest run --maxWorkers=2 @commitlint/ensure/src/case.test.ts @commitlint/rules/src/subject-case.test.ts
```
- Red（第一个 commit `32f159f`，只有测试；复审时另外把 fix commit 的 case.ts 还原后重新 build 验证）：4 个用例在断言上失败，其余 143 个通过。失败的是：
  - `true for Add Module 1.0.0 on start-case`
  - `true for Add Core.js on start-case`
  - `true for Support Node.js 22 And Es2015 on start-case`
  - `with startcase subject containing a version should succeed for "always startcase"`
- Green（第二个 commit `c3ca87d`）：147 个全部通过。
- `pnpm vitest run --maxWorkers=2`（全仓库）：91 个文件、1273 个测试全部通过。
- `pnpm format`（oxfmt --check）和 `pnpm lint`（oxlint）：都通过。
- CLI 验证，配置为 `subject-case: [2,'always','start-case']`：
  - `feat: Add Module 1.0.0` 退出码 0
  - `feat: Add Core.js` 退出码 0
  - `fix: Typo` 退出码 0
  - `feat: Add module 1.0.0` 退出码 1
- `node @commitlint/cli/lib/cli.js --from 0737aba --to HEAD`：两个 commit message 都通过。

## 需要提交者注意
- CONTRIBUTING 要求 bug fix 的 PR 按两个 commit 提交，所以这里有两个 patch，必须两个都 `git am`：先 `0001-test…`（失败的测试），再 `0002-fix…`（实现）。
- **`tools/submit_pr.sh` 目前只会 am `0001-*.patch`**，直接用它会漏掉 fix commit。请按下面的手动步骤提交；或者先让脚本支持 `000*-*.patch`。另外脚本里的 `--amend --reset-author` 只作用于最后一个 commit，第一个 commit 的作者本来就是 anyingiit，所以不受影响。
- 复审：两个 patch 在 `0737aba` 的干净 worktree 上 `git am` 成功，结果与分支一致；patch 中无 AI 模型名，author/committer 均为 anyingiit。
- 行为变化：配置了 `never start-case` 的项目里，`Add Core.js`、`Add Module 1.0.0` 这类 subject 现在会被认定为 start case，因此会被拒绝。这与 always 的判定一致，但在边界上是行为变化，PR 正文里已经说明。
- `Add Module v1.0.0`（小写 v）仍然失败。这是有意的，因为 `v` 是小写开头的词。如果维护者希望放行，再单独讨论。
- 仓库没有 AI 政策，不需要 DCO 或 AI trailer（PR 正文里已有 Claude Code 披露段落）。issue 带 help wanted 且无人分配，CONTRIBUTING 未要求先认领，可直接开 PR。commit 身份是 anyingiit。

## 如何提交
```bash
git clone https://github.com/conventional-changelog/commitlint && cd commitlint
git checkout -b fix/start-case-periods-numbers origin/master
git -c user.name=anyingiit -c user.email=49945850+anyingiit@users.noreply.github.com am \
  /home/user/Playground/contributions/115-conventional-changelog-commitlint-3294/0001-test-ensure-cover-start-case-words-with-periods-and-.patch \
  /home/user/Playground/contributions/115-conventional-changelog-commitlint-3294/0002-fix-ensure-allow-periods-and-numbers-in-start-case-w.patch
pnpm install && pnpm build && pnpm vitest run @commitlint/ensure @commitlint/rules
git push <anyingiit fork> fix/start-case-periods-numbers
gh pr create --repo conventional-changelog/commitlint --head anyingiit:fix/start-case-periods-numbers \
  --title "$(cat .../pr_title.txt)" --body-file .../pr_body.md
```
如果改好了 submit_pr.sh，让它能 am 全部 patch，也可以运行：
```bash
tools/submit_pr.sh contributions/115-conventional-changelog-commitlint-3294 conventional-changelog/commitlint master fix/start-case-periods-numbers contributions/115-conventional-changelog-commitlint-3294/pr_title.txt contributions/115-conventional-changelog-commitlint-3294/pr_body.md
```
（脚本当前版本只会 am 0001，见上文"需要提交者注意"。）

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
