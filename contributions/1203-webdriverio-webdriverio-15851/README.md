# webdriverio/webdriverio#15851 — 在 multi-remote 下，custom$ / react$ / shadow$（以及对应的 $$）不返回 multi-remote 结果

| 项 | 值 |
|---|---|
| Issue | https://github.com/webdriverio/webdriverio/issues/15851 |
| Tier | 高星 |
| Labels | Bug 🐛, good first pick, help wanted, multi remote, v10（milestone v10） |
| Status | ✅ ready：已独立复核，patch 和 PR 文案就绪，尚未提交 |
| Base | **`v10` 分支** @ 7423b42（2026-10-01）。注意不是 `main`：`main` 是 v9 |
| Duplicate-PR check | 2026-10-01 23:13 和 23:41 UTC 各查了一次。`pulls?q=is:pr 15851` 结果为 0；关键词 `multiremote custom$/react$/shadow$`、`shadow$ multiremote` 搜到的都是别的 PR（#15843、#15674、#15768 等）。issue 没有评论，没有 assignee，Development 一栏也没有关联的分支或 PR |

## 问题理解

在 multi-remote browser 上，`multiRemote.ts` 里的 `commandWrapper` 只对 `$`（`elementWrapper`）和 `$$`（`ElementArray.fromAsyncCallback`，按 index 做 zip）做了包装。`custom$`、`react$`、`elem.shadow$` 以及对应的 `$$` 版本都走默认分支，直接返回每个实例各自的原始结果，也就是 `[Element, Element]` 或 `[ElementArray, ElementArray]`。这样一来：
- 返回值和类型声明不一致（`custom$`、`react$` 的类型本来就写的是 `MultiRemoteElement`）；
- 结果上没有 `isMultiRemote`、`getInstance()`、`select()`，也不能直接在上面调用元素命令；
- 列表上缺少 `selector`、`foundWith`、`parent`、`props`，expect-webdriverio 的 matcher 无法在重试时重新查询。

## 合理性判断

- issue 被打上 Bug、good first pick、help wanted 和 v10 milestone，正文里已经指出了根因（只处理了 `$` 和 `$$`），属于明确的 bug。
- v10 分支上已经有 `MultiRemoteElementArray`（#15674）。这次是把同一套处理推广到其他查询命令，方向和维护者的设计一致。
- AI 政策：v10 分支上有 `AGENTS.md`、`CLAUDE.md`，CONTRIBUTING 明确写了 "If you are an AI coding agent (Cursor, Claude Code, Copilot, Codex, …), start with AGENTS.md"。也就是说它欢迎 AI agent，没有禁止。label 说明里也没有 human-only 之类的限制。
- **踩坑记录**：scout 以为改动应基于 `main`，最初也确实在 main 上做了一版。后来发现 issue 提到的 `multiRemote.ts`（大写 R）只存在于 `v10` 分支，main 上是 `multiremote.ts`（v9 代码）。所以最终 patch 基于 `v10`。main 版本留作 `alt-main-v9-0001-*.patch`，只在维护者要求 backport 到 v9 时才用，**默认不要提交它**。

## 改动（v10 patch：`0001-fix-webdriverio-return-multi-remote-results-from-cus.patch`）

- `packages/webdriverio/src/multiRemote.ts`
  - 新增 `SINGLE_ELEMENT_QUERIES = {$, custom$, react$, shadow$}` 和 `MULTI_ELEMENT_QUERIES = {$$, custom$$, react$$, shadow$$}`，前者走 `elementWrapper`，后者走 `ElementArray.fromAsyncCallback` + zip。
  - `$$` 各变体的 `foundWith` 改为命令名本身，`props` 和单实例版本保持一致（`custom$$` 是 strategyArguments，`react$$` 是 `[props, state]`，其余为 `[]`），由新函数 `elementListProps()` 生成。
  - `custom$$` 的第一个参数是 strategy 名而不是 selector，所以它的元素沿用各自找到时的 selector。
- `packages/webdriverio/src/types.ts`：`custom$$`、`react$$` 改为返回 `MultiRemoteElementArray`（并删掉原来那段说它们"不 zip"的注释）；为 `MultiRemoteElement` 新增 `shadow$` / `shadow$$` 的 multi-remote 类型（之前被映射成"每个实例的结果数组"）。
- `packages/webdriverio/tests/multiRemote.test.ts`：新增 describe `element queries other than $ and $$ (#15851)`，共 6 个测试，覆盖 6 个命令，也检查列表的 metadata。
- `tests/typings/webdriverio/async.ts`：新增 7 行 `expectType`（webdriverio 的 AGENTS.md 要求公开类型变化时在这里加用例）。
- 文档：`website/docs/Multiremote.md`、`website/docs/v10Migration.md`、`.agents/skills/wdio-v10-migration/SKILL.md` 里都写着"custom$$/react$$ 不 zip"，现已同步修改（AGENTS.md 要求 v10Migration 和这个 skill 一起改）。

## 验证（v10，Node 22.22.0，pnpm 11.27.1，通过 shim 调用）

```sh
cd /home/user/work/webdriverio-15851        # 分支 fix-multiremote-element-queries-15851
pnpm install --frozen-lockfile --ignore-scripts
pnpm run compile:all
npx vitest --run packages/webdriverio/tests/multiRemote.test.ts
```

| 命令 | 结果 |
|---|---|
| 去掉 src 改动、保留新测试：`npx vitest --run packages/webdriverio/tests/multiRemote.test.ts` | **6 failed** / 21 passed → red |
| 加上修复后同一命令 | 27 passed → green |
| `pnpm run test:package webdriverio` | 189 files，1539 passed，2 skipped，Type Errors: none |
| 去掉 src 改动并重新 build webdriverio 后：`cd tests/typings/webdriverio && npx tsc --skipLibCheck` | **5 errors**（例如 `Property 'isMultiRemote' does not exist on type 'MultiRemoteElement[]'`）→ red |
| 加上修复并重新 build 后，`test:typings:{webdriver,webdriverio,mocha,jasmine,cucumber}` | 全部 exit 0 → green |
| `npx oxlint <4 个改动的 ts 文件>` | 0 问题 |
| `npx tsc --noEmit -p packages/webdriverio/tsconfig.json` | exit 0 |
| `pnpm run test:smoke multiRemote` | All smoke tests passed（只是回归检查，这个 suite 不调用这些查询命令） |
| AGENTS.md 里的 multi-remote 命名检查（git grep `[Mm]ultiremote`） | 本次 diff 没有引入命中；输出里只有 v10 原有的几处（shim.ts、multiRemote.ts:411、multiRemoteMock.test.ts、docs），不是本 PR 造成的 |
| `git am` 到干净的 `origin/v10` worktree | 能干净地应用 |

没跑：真实浏览器的 example script。AGENTS 的 verify-webdriverio 要求用户可见的改动用它验证，但本机没有浏览器和 driver。PR 文案里已经说明。

main（v9）版本的备用 patch 也做过 red/green：在 `fix-15851-main` 分支上，9 failed → 21 passed；webdriverio 包全部单测 1386 passed；typings 和 eslint 均通过。

## 需要提交者注意

- **PR 的 base 分支必须选 `v10`**，不是 `main`。PR 模板（v10 版）有 "How you tested"、"Types of changes"、"Checklist"、"Backport Request" 几节，pr_body.md 已经按模板填好，并加入了 disclosure 段落。
- 仓库对 AI 友好（AGENTS.md / CLAUDE.md），没有 AI co-author trailer 的要求。提交信息遵循 Conventional Commits（`fix(webdriverio): ...`），符合 AGENTS.md。
- 不需要 DCO 或 Signed-off-by。仓库有 "Awaiting CLA Signature" label，**首次 PR 可能需要签 OpenJS 的 CLA（EasyCLA）**，请按机器人提示用自己的账号签。
- CHANGELOG 由发布流程生成，AGENTS.md 规定不要手改。
- 行为变化：multi-remote 下 `custom$$`、`react$$`、`shadow$$` 的返回值，从"每实例一个列表"变成了一个 zip 后的 `MultiRemoteElementArray`。issue 要的就是这个，而且 v10 是大版本，所以没有加开关。如果维护者希望写进 v10Migration 的"breaking"小节，可以按 review 意见再补。
- 仓库目录里的 `alt-main-v9-*.patch` 是给 main/v9 的备用版本（需要 `WDIO_ENABLE_MULTI_REMOTE_ELEMENT_ARRAY` 才能拿到 array metadata）。只在维护者要求 backport 时使用。

## 如何提交

```bash
git clone https://github.com/webdriverio/webdriverio && cd webdriverio
git checkout -b fix-multiremote-element-queries-15851 origin/v10
git am /path/to/0001-fix-webdriverio-return-multi-remote-results-from-cus.patch
git push <your-fork> fix-multiremote-element-queries-15851
# 在 GitHub 上开 PR，base 选 v10；标题见 pr_title.txt，正文见 pr_body.md
```

工作目录 `/home/user/work/webdriverio-15851` 保留了下来（分支 `fix-multiremote-element-queries-15851` 基于 v10，`fix-15851-main` 基于 main），里面有 node_modules 和已编译的 build，方便 reviewer 复现。

## 独立复核（2026-10-01 23:45 UTC）

- issue 仍为 open，没有 assignee，Development 一栏没有关联 PR；`is:pr 15851` 搜索结果为 0，没有竞争 PR。
- 读了 v10 上的 diff。`custom$/react$/shadow$` 改为走 `elementWrapper`，`$$` 各变体改为走 zip 后的 `ElementArray`。`foundWith`/`props` 和单实例版本（`custom$$.ts`、`react$$.ts`、`shadow$$.ts`）一致。`array.ts` 的越界 refetch 逻辑（`parent[foundWith](selector)`）对多实例同样适用，和单实例的行为一致。没有发现回归。
- red/green：在 workdir 把 `packages/webdriverio/src` 还原到 HEAD~1 后跑 `multiRemote.test.ts`，6 个新测试全部失败；恢复修复后 27/27 通过。
- `npx oxlint`（4 个改动文件）0 问题；`tsc --noEmit -p packages/webdriverio/tsconfig.json` exit 0。
- `0001-*.patch` 与 workdir 的提交内容一致，作者是 anyingiit，patch 中没有 AI 模型名或 co-author。pr_body 为英文，包含 disclosure 段和 `Closes #15851`。
- 没有需要修改的地方。

Status: ✅ ready
