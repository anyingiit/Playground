# ColeMurray/background-agents#2044 — feat(slack-bot): allow choosing the Claude Agent harness for Slack

| 项 | 值 |
|---|---|
| Issue | https://github.com/ColeMurray/background-agents/issues/2044 |
| Tier | 新锐 |
| Labels | enhancement, good first issue, help wanted |
| Status | ✅ ready（patch、PR 文本都已写好，还没提交） |
| 重复 PR 检查 | 2026-10-01：PR 搜索 "2044" 结果为 0；"harness slack" 搜到的 open PR（#2195 Slack 回复续接、#2183 团队边界、#2045 Discord、#2017）都与本 issue 无关；issue 没有 assignee，也没有评论。姊妹 issue #2034（Linear）同样没人认领 |
| Base | `main` @ b98a378 (2026-10-01) |
| 分支 | `feat/slack-claude-agent-harness` |

## 问题理解

Slack bot 的 `createSession()` 从不传 `harness`，所以 control plane 一律用默认的 OpenCode 建会话。web composer、automations、child sessions 已经可以选 Claude Agent。issue 要求：

- 在 Slack 设置里加 harness 选项，不配置时行为不变（仍是 OpenCode）；
- 按 automations 的方式校验 model 与 harness 是否兼容，不兼容时给出清楚的报错；
- 处理所有模型来源（环境变量 `DEFAULT_MODEL`、workspace 默认模型、用户 App Home 偏好、`!model` 内联 flag），并考虑两种 harness 在 provider 认证上的差异；
- 必须使用 `packages/shared/src/harnesses.ts` 里的共享 helper；
- 更新文档并补测试。

## 合理性判断

- issue 是维护者自己提的（带 good first issue / help wanted），写得很细。
- 与 #2034（Linear 的同类需求）配套。
- 仓库已有完整的 harness 基础设施（#1851/#1853/#1856），control plane 的 `POST /sessions` 已接受 `harness` 字段，并在创建时用 `checkHarnessCompatibility` 校验。所以 Slack 侧只需要把设置贯通下来，加上友好报错，需求合理。
- AI 政策：CONTRIBUTING.md、AGENTS.md / CLAUDE.md（两者内容相同）、labels 页面都没有禁止 AI 贡献的规定。

## 改动（21 个文件，+509/−8）

- **shared** `types/integrations.ts`：`slackGlobalSettingsSchema` 新增可选字段 `harness: harnessIdSchema`。
- **control-plane** `db/integration-settings.ts`：
  - `harness` 只允许在 global 级别设置，per-repo 级别会被拒绝；非法 id 会被拒绝；
  - 同时设置了 model 时用 `checkHarnessCompatibility` 校验，与 automation 保存时的逻辑一致；
  - 新增 4 个测试。
- **slack-bot**：
  - 新增 `src/harness.ts` 的 `slackHarnessModelError()`：在共享规则的报错后面附上 Slack 场景的提示（"This session runs on Claude Agent. It runs Anthropic models only. Choose a supported model with `!model` or in the App Home tab."）；
  - `slack-settings.ts` 读取 `harness`，非法值通过 `.catch(undefined)` 回落到默认值，不会把其他设置一起丢掉；
  - `control-plane-client.ts` 只有在配置了 harness 时才把它放进请求体；
  - `session-launcher.ts` 在所有模型来源都解析完之后、创建会话之前，校验 session model 和首条 prompt 的 model。不兼容就在 thread 里回复原因，不创建会话；
  - thread mapping 只在设置了 harness 时写入它（`ThreadSession.harness`），`message-handler.ts` 用它校验 follow-up 的 `!model` 覆盖；
  - provider 认证由 control plane 的 `resolveSessionProviderAuth({ harness })` 处理，bot 侧不需要改。
- **web** `slack-integration-settings.tsx`：
  - Defaults 卡片里新增 "Agent harness" 下拉框，默认模型列表按 harness 过滤；
  - 切到 Claude Agent 时会清掉不兼容的默认模型；
  - 选 OpenCode 时不写入这个 key；Reset 时恢复为 OpenCode。
- **docs/CHANGELOG**：改了 `docs/integrations/SLACK.md`、`docs/CLAUDE_AGENT.md`、`packages/docs/content/docs/integrations/slack.mdx`、`models/agent-harnesses.mdx`，并在 `CHANGELOG.md` 的 Unreleased 下加了 `### Added`。

## 验证

环境：Node 22.22（仓库 CI 用 Node 24），安装命令 `npm ci --ignore-scripts`，然后 `npm run build -w @open-inspect/shared`。

**red → green**：把所有非测试源码改动 stash 掉、只保留新测试来跑，结果如下：

- slack-bot（`npx vitest run src/sessions src/slack-settings.test.ts src/index.test.ts`）：6 failed / 106 passed。失败的是：
  - sends the configured harness…
  - returns the configured harness
  - creates the session on the harness chosen in Slack settings
  - rejects a model the configured harness cannot run before creating a session
  - rejects a first-prompt override…
  - rejects a follow-up model override the thread's harness cannot run
- control-plane（`npx vitest run src/db/integration-settings.test.ts`）：2 failed / 136 passed。
- web（`npx vitest run src/components/settings/integrations/slack-integration-settings.test.tsx`）：3 failed / 31 passed。

恢复改动后以上全部通过。

**全量检查**：

| 命令 | 结果 |
|---|---|
| `npm test -w @open-inspect/slack-bot`（vitest） | 520/520 |
| `npm test -w @open-inspect/web` | 2676/2676 |
| `npm test -w @open-inspect/shared` | 1082/1082 |
| `npm test -w @open-inspect/linear-bot` | 267/267 |
| `npm test -w @open-inspect/docs` | 44/44 |
| `npm test -w @open-inspect/control-plane` | 6114 passed，2 failed |
| `tsc --noEmit`（shared, control-plane, slack-bot, web, linear-bot, github-bot, docs） | 全部 0 错误 |
| `npm run lint`、`npm run format:check` | 通过 |
| `npm run lint:complexity` | 只出报告、不影响退出码：`message-handler` 的 handler 复杂度从 60 到 61，它本来就是热点 |

control-plane 的 2 个失败在 `src/routes/environments-catalog.test.ts`（"conceals and audits nonmember or missing team …"）。在未修改的 base 上同样失败，与本改动无关。

**未运行**：control-plane `test:integration`（workerd/Miniflare）、web/docs 的 Next.js build、knip。

## 需要提交者注意

- 仓库没有 DCO 要求，也不需要 `Signed-off-by`。提交规范是 Conventional Commits，subject 少于 72 字符（已满足）。
- 仓库没有 PR 模板，pr_body 用的是 brief 规定的格式。
- 这是功能 PR，体量中等（+509 行，其中约一半是测试）。如果维护者更想拆分，可以拆成 "settings + bot" 和 "web UI" 两个 PR。
- 设计选择：模型与 harness 不兼容时直接报错，不静默回落（与 `docs/CLAUDE_AGENT.md` 里 composer 的规则一致）。PR 描述里已说明，并给出了改成回落的位置，方便维护者选择。
- UI 的提示文案写死了 "runs Anthropic models only"。目前只有 claude 这一种非默认 harness，所以没问题；以后如果 catalog 新增 harness，需要改成按 capabilities 生成。
- 提交前可以先看看 #2034（Linear 版）有没有人提交了 PR，两边的实现风格最好保持一致。
- 本地用的是 Node 22，CI 用 Node 24。

## 如何提交

```bash
git clone https://github.com/anyingiit/background-agents && cd background-agents   # 先在 GitHub 上 fork
git remote add upstream https://github.com/ColeMurray/background-agents && git fetch upstream
git checkout -b feat/slack-claude-agent-harness upstream/main
git am /path/to/0001-feat-slack-bot-allow-choosing-the-Claude-Agent-harne.patch
npm ci && npm run build -w @open-inspect/shared && npm test -w @open-inspect/slack-bot
git push origin feat/slack-claude-agent-harness
gh pr create --repo ColeMurray/background-agents --head anyingiit:feat/slack-claude-agent-harness \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title

feat(slack-bot): allow choosing the Claude Agent harness for Slack

## PR body

见 `pr_body.md`。
