# ColeMurray/background-agents #2044 — feat(slack-bot): allow choosing the Claude Agent harness for Slack

| 项 | 值 |
|---|---|
| Issue | https://github.com/ColeMurray/background-agents/issues/2044 |
| Tier | 新锐 |
| Labels | enhancement, good first issue, help wanted |
| Status | ✅ ready — patch + PR 文案已完成 |
| 重复 PR 检查 | 2026-10-01：issue 无 assignee、无评论、无 linked PR；搜索 `is:pr 2044` 和 `harness slack` 都没有相关 PR |
| Base | `main` @ b98a378 |

## 问题理解
Slack 触发的会话固定跑在 OpenCode 上：slack-bot 创建会话时不传 `harness`，Slack integration settings 也没有 harness 字段。issue 要求：
- 管理员可以在工作区层面选择 Claude Agent，未设置时保持 OpenCode
- 已有线程（包括过期后恢复的线程）保留原 harness
- 模型和 harness 不匹配时给出清晰的报错
- 设置页拒绝不兼容的组合，并同步更新文档

## 合理性判断
- issue 由维护者写成详细规格，带 good first issue / help wanted 标签。
- web composer、automation、child session 已经支持 harness，共享的 `checkHarnessCompatibility` 也已存在，这次只是把 Slack 接入同一套机制，属于合理需求。

## 改动（21 个文件，单个 commit）
- **shared**：`slackGlobalSettingsSchema` 新增 `harness: harnessIdSchema.optional()`。
- **control-plane**：`validateSlackSettings` 只允许在 global 层设置 `harness`，拒绝未知 id，拒绝 harness 跑不了的默认模型。
- **slack-bot**
  - `slack-settings` 读取 harness，值无效时回退到默认。
  - launcher 按「恢复计划 → Slack 设置 → 默认」的顺序决定 harness，在创建会话前校验会话默认模型和首条 prompt 的模型；不兼容就在线程里回复原因。只有非默认 harness 才发送 `harness` 字段，并把 harness 写入线程映射。
  - stale 恢复沿用线程原来的 harness；旧映射没有这个字段，按 OpenCode 处理。
  - 已有线程里的 `!model` 覆盖如果与线程 harness 不兼容，直接报错，不再发送。
- **web**：Slack 设置页新增 Agent harness 选择器，模型列表按 harness 过滤；组合不兼容时显示错误并禁用 Save。
- **docs**：更新 `docs/CLAUDE_AGENT.md`（新增 Slack 小节）、docs 站 slack.mdx 与 agent-harnesses.mdx、CHANGELOG（Unreleased › Added）。

## 验证
环境：Node 22（CI 用 24），`CI=1 npm ci --ignore-scripts`，`npm run build -w @open-inspect/shared`。

| 命令 | 结果 |
|---|---|
| `packages/slack-bot: npx vitest run` | 523 passed |
| `packages/shared: npx vitest run` | 1082 passed |
| `packages/web: npx vitest run --maxWorkers=3` | 2676 passed |
| `packages/docs: npx vitest run` | 44 passed |
| `packages/control-plane: npx vitest run` | 6114 passed / 2 failed（见下） |
| `npm run typecheck -w` shared / control-plane / slack-bot / web | 通过 |
| `npx eslint .` | 通过 |
| `npx prettier --check <changed files>` | 通过 |

control-plane 的 2 个失败用例都在 `src/routes/environments-catalog.test.ts`（"conceals and audits nonmember or missing team …"）。stash 掉本改动后在 base 上运行，同样 2 failed / 16 passed，与本改动无关。

**Red → green**：只回退源码、保留测试时，以下新增测试全部失败，恢复源码后全部通过。
- control-plane：2 个失败
- slack-bot：13 个失败（新增的 launcher、index 流程、client、store、settings 测试，以及因 `buildThreadSession` 多了 harness 参数而更新的断言）
- web：3 个失败

未运行：control-plane integration tests（需要 workerd/D1）、Python 测试（本次没有改动 Python）。

## 需要提交者注意
- 仓库没有 AI 贡献禁令（CONTRIBUTING / AGENTS.md / CLAUDE.md / labels 都查过）；PR 描述里已有披露段落。
- 不要求 DCO / Signed-off-by。commit 格式为 Conventional Commits（`feat(slack-bot): …`）。
- 本地 Node 是 22，CI 是 Node 24，以 PR 上的 CI 结果为准。
- 这是一个功能型改动（约 580 行，大部分是测试）。维护者可能对 UI 文案或「App Home 模型列表是否也按 harness 过滤」有自己的想法；这次刻意没改 App Home，不兼容的情况在发起会话时报错。如果维护者要求，可以再补上。
- 文档里关于 Slack 会话认证的说法（Claude Agent 下使用安装默认 Claude 账号，否则用 API key）是根据 `provider-account-resolution.ts` 推断的，没有在真实部署上验证。

## 如何提交
```bash
git clone https://github.com/ColeMurray/background-agents && cd background-agents
git checkout -b feat/slack-claude-agent-harness origin/main
git am /path/to/0001-feat-slack-bot-allow-choosing-the-Claude-Agent-harne.patch
git push <your-fork> feat/slack-claude-agent-harness
gh pr create --repo ColeMurray/background-agents --head anyingiit:feat/slack-claude-agent-harness \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
见 `pr_title.txt`：`feat(slack-bot): allow choosing the Claude Agent harness for Slack`

## PR body
见 `pr_body.md`。
