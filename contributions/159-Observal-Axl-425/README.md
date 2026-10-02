# Observal/Axl#425 — Vim mode: add cw and cc

Status: ✅ ready — 独立复核通过；提交前需登录看 issue 的 1 条评论并按 AI_POLICY 人工审阅（未提交）

| 项 | 值 |
|---|---|
| Issue | https://github.com/Observal/Axl/issues/425 |
| Tier | 新锐（约 1 个月的新项目，~1.2k stars，增长快） |
| Labels | client:tui, good first issue, help wanted |
| Status | ✅ ready — patch + PR text done (not submitted) |
| Base | `main` @ 02cb573 (2026-09-25) |
| Duplicate-PR check (2026-10-01 23:1x UTC) | issue OPEN、无 assignee、Development 无关联分支/PR；`is:pr 425` 0 条、`is:pr cw` 0 条；`is:pr vim` 仅 #463（D/C，对应 #424）、#431（文档）、#6（已合并的基础 TUI），均不涉及 cw/cc |

## 问题理解

TUI 的可选 Vim 模式（`/vim` 开关）在 `packages/tui/src/vim-mode.ts` 里已有 `dw`、`dd`、`f<x>`，靠 `pending` 字段实现两键命令。Issue 要求：
- 把 `c` 加为 pending 键；
- `cw`：用 `editor.deleteWordForward()` 删掉一个词，再进入 insert 模式；
- `cc`：清空当前行文本但保留这一行（不同于 `dd` 删除整行），再进入 insert 模式；
- `c` 后接其它键：取消，不改动；
- 测试放在 `productivity.test.ts` 现有 Vim 测试旁边。

## 合理性判断

- Issue 由项目成员开出（Lokesh7025），带 good first issue / help wanted 标签，步骤和验收标准都写得很具体；与仓库现状吻合（`pending` 机制已存在）。
- AI 政策：`AI_POLICY.md` 明确 “AI tools are welcome… Unreviewed output is not.” 允许 AI 辅助，但有条件（见下文“需要提交者注意”）。标签描述中没有 AI/人类限定。
- 未在 main 上实现（vim-mode.ts 无 `c` 处理）。

## 改动

- `packages/tui/src/vim-mode.ts`：新增 `pending === "c"` 分支；`cc` → `editor.clearCurrentLine()`，`cw` → `editor.deleteWordForward()`，两者之后 `this.current = "insert"`；其它字符只清空 pending、不改文本、保持 normal。`c` 加入可进入 pending 的键列表。
- `packages/tui/src/editor.ts`：新增 `LineEditor.clearCurrentLine()`，用已有的 `kill(lineStart, lineEnd)`（保留换行；与 `dd` 一样可 undo、进 kill ring）。
- `packages/tui/test/productivity.test.ts`：新增测试 `Vim cw and cc change text and enter insert mode`（cw、在三行中间行做 cc 并输入、c+z 取消后 w 只是移动）。
- 三个文件按 CONTRIBUTING 的 SPDX 规则各加一行 `SPDX-FileCopyrightText: 2026 anyingiit`。
- Commit：`feat(tui): add Vim cw and cc commands`（Conventional Commits），带 DCO `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`（仓库强制 DCO）。

## 验证

环境：Node v22.22.0，pnpm 11.25.0，`pnpm install --frozen-lockfile`，`npx tsc -b packages/*/tsconfig.build.json packages/extensions/*/tsconfig.build.json`（tui 测试依赖其它包的 dist）。

| 命令 | 结果 |
|---|---|
| 仅加测试、未改 src：`cd packages/tui && node --test --test-name-pattern=Vim test/productivity.test.ts` | **red**：1 pass / 1 fail（`expected: 'two'`, `actual: 'one two'`） |
| 加入修复后同一命令 | **green**：2 pass / 0 fail |
| `cd packages/tui && node --test test/*.test.ts` | 228 pass / 0 fail |
| `pnpm format:check` / `pnpm lint` | 通过（457 files, no fixes） |
| `pnpm typecheck`（含 @axl/ui、@axl/web） | 通过 |
| `pnpm check:boundaries` / `pnpm check:generated` | 通过 |
| `uvx reuse==6.2.0 lint` | compliant，632/632 |
| 根目录全量测试（不含 web 生产构建）：`node --test --test-concurrency=1 --test-timeout=30000 packages/*/test/*.test.ts packages/extensions/*/test/*.test.ts scripts/*.test.ts` | 1073 tests：1050 pass / 0 fail / 21 skipped / 2 cancelled（30s 文件级超时）。被取消的是 `packages/cli/test/unsafe-cli.test.ts`（单独运行：修复前 14/14 pass、修复后 14/14 pass，属机器负载导致超时）和 `scripts/build-release-package.test.ts`（内部执行完整 `pnpm build` 含 web 构建，太重未重跑）。两者都与 TUI 无关。 |

未运行：`pnpm build` 中的 `@axl/web` 生产构建（本改动不涉及 web）。

## 需要提交者注意

1. **Issue 有 1 条评论无法读取**：issue 列表显示 1 comment，但 issue 页面（未登录抓取）中看不到任何评论。提交前请登录查看这条评论，确认没人认领（如有人说 “I'm working on this”，请不要提交）。Issue 的 Getting Started 还要求先 “Comment to indicate you're working on this”，建议先评论再开 PR。
2. **AI_POLICY.md 条件**（必须遵守）：
   - 由你本人审阅并理解完整 diff，能解释每一行；PR 模板里的 “I reviewed the complete diff.” 和 “I manually reviewed, understood, and tested the generated work.” 两个框我故意没勾，请自己审完后再勾。
   - PR 必须写出 AI 工具和模型/版本：pr_body.md 已写 “Claude Code (Claude Opus 5.5)”。commit 里没有模型名。
   - 规则说 “An unattended agent may not choose work and publish a contribution on its own”，需要由你本人决定并发布。
   - 界面改动需在 PR 附截图（不要提交进仓库）。这是纯按键行为，没有视觉变化；如维护者要求可补一张 `/vim` 下操作的截图。
3. **DCO**：仓库要求每个 commit 有与作者一致的 `Signed-off-by`。patch 已带 `anyingiit <49945850+anyingiit@users.noreply.github.com>` 的 sign-off；如你想用别的邮箱，请 `git commit --amend --reset-author -s` 并保证作者与 sign-off 一致。
4. **SPDX**：CONTRIBUTING 要求修改文件时为自己加 `SPDX-FileCopyrightText` 行；已加 “2026 anyingiit”，如要用真名请自行修改。
5. **行为说明**：按 issue 要求 `cw` 复用 `deleteWordForward()`，因此会连同词后的空格一起删（和 `dw` 一样）；真正的 Vim 中 `cw` 等价于 `ce`，会保留空格。PR 描述里已说明并表示可改。
6. 与开放 PR #463（D/C）改的是同一个 `handle()` 方法的不同位置，谁先合并另一方都只需简单 rebase。
7. 仓库要求 PR 模板格式（Purpose / Fixes / Approach / How was this tested / Checklist / AI assistance），pr_body.md 已按该模板写，并包含 Motivation/disclosure 段落。

## 如何提交

```bash
git clone https://github.com/Observal/Axl && cd Axl
git checkout -b feat/vim-cw-cc origin/main
git am /path/to/0001-feat-tui-add-Vim-cw-and-cc-commands.patch
pnpm install --frozen-lockfile && pnpm check   # 可选：完整检查
git push <your-fork> feat/vim-cw-cc            # PR 目标分支: main
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。审阅用的 clone 在 `/home/user/work/Axl-425`（分支 `feat/vim-cw-cc`）。

## 独立复核

复核时间 2026-10-01 23:35–23:45 UTC（独立复核 agent）：

- **Issue 状态**：WebFetch issue 页面：仍 OPEN、无 assignee、Development 无关联 PR/分支；未登录页面仍看不到那 1 条评论（`gh api` 在本会话中对该仓库不可用），**提交者仍需登录查看**。PR 搜索 `is:pr cw OR cc OR 425` 0 条；`is:pr vim` 仅 #463（D/C）、#431（文档）、#6（已合并），无竞争 PR。
- **对照 issue**：`c` 进入 pending；`cw` → `deleteWordForward()` + insert；`cc` → `clearCurrentLine()`（`kill(lineStart, lineEnd)`，保留换行，可 undo）+ insert；`c`+其它键只清 pending、不改文本、留在 normal；Escape 已有清 pending 逻辑。测试放在 `productivity.test.ts` 的 Vim 测试旁。完全覆盖 issue 的验收点。
- **边界情况**：空行上 `cc`：`kill` 对空区间直接返回，光标已在该行，进入 insert，正确。最后一行/首行 `cc` 不涉及换行，正确。`dd`/`dw` 行为未改。`cw` 会连带删除词后空格（与真 Vim 不同），README 第 5 点与 PR 正文已说明，属 issue 指定做法。
- **red→green（本人重跑）**：重新 `pnpm install --frozen-lockfile` + `tsc -b` 后，把 `src/editor.ts`、`src/vim-mode.ts` 还原到 HEAD~1，仅保留新测试：`node --test --test-name-pattern=Vim test/productivity.test.ts` → 1 pass / 1 fail（`expected: 'two'`, `actual: 'one two'`）；恢复修复后 → 2 pass / 0 fail。
- **TUI 全量测试**：`node --test test/*.test.ts` → 228/228 pass。
- **检查**：`pnpm format:check`、`pnpm lint` 通过（457 files）；`tsc --noEmit` 通过；三个改动文件 `biome check` 无问题。
- **仓库约定**：无 CHANGELOG/changeset 机制，无需新闻片段；Conventional Commit 标题；DCO sign-off 与作者一致；SPDX 行已加；PR 正文按 `.github/pull_request_template.md` 结构。仓库内没有其它列出 Vim 键的文档需同步（文档由开放 PR #431 处理）。
- **交付物**：`0001-*.patch` 与 workdir 提交 `9aebe78` 逐字一致；作者 `anyingiit <49945850+anyingiit@users.noreply.github.com>`；patch 中无 AI 模型名（模型名只出现在 pr_body.md 的 AI assistance 部分，这是 AI_POLICY 要求的披露）。pr_title.txt、pr_body.md（英文，含 Motivation/disclosure 段落，`Fixes #425`——GitHub 关闭关键字，与 `Closes` 等效，按 PR 模板的 “Fixes” 小节保留）、AUDIT.md 齐全。
- 唯一改动：pr_body.md 补上 PR 模板中的 `## Learning` 小节（N/A），使结构与模板完全一致。commit 未改动。

Status: ✅ ready — 独立复核通过（red→green 复现、TUI 228/228、format/lint/typecheck 通过）；提交前需登录看 issue 的 1 条评论并完成 AI_POLICY 要求的人工审阅
