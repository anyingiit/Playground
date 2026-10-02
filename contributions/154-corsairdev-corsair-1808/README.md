# corsairdev/corsair #1808：`corsair ui --port` 校验

| 项 | 值 |
|---|---|
| Issue | https://github.com/corsairdev/corsair/issues/1808 |
| Tier | 新锐 |
| Labels | bug, cli, difficulty: easy, good first issue |
| Status | ✅ 已完成：patch、PR 文案和验证都已就绪 |
| 重复 PR 检查 | 2026-10-01 检查过：issue 是 open 状态，没有 assignee，没有评论，也没有关联 PR。用 `1808`、`port`、`studio`、`parseInt` 搜索 PR，只找到 #1787，它改的是 `corsair http` 的空白裁剪，属于另一个命令，和本 issue 不冲突 |
| Base | `main` @ 9dce172e |

## 需要提交者注意

- **Good First Issue 只留给第一次贡献的人**（见 CONTRIBUTING.md）：如果 anyingiit 已经在 corsair 合并过 PR，就**不要提交**这个 patch。
- CONTRIBUTING 建议先在 issue 下评论说明打算怎么改，等 maintainer assign 后再开 PR。建议先发一条评论，例如："I'd like to take this — plan: validate `--port` with the same digits-only 1–65535 rule as `http.command.ts`, plus tests." 等 assign 之后再提交。
- PR 模板要求**先开成 Draft**，checklist 完成后再点 Ready（Greptile 和 gate 会在点 Ready 后启动）。
- 项目不要求 DCO 或 Signed-off-by。仓库里没有禁止 AI 的规则，label 说明里也没有。PR 正文已经写明使用了 Claude Code。
- 用 Conventional Commits 格式，commit 作者是 anyingiit <49945850+anyingiit@users.noreply.github.com>。

## 问题理解

`packages/cli/src/commands/studio.command.ts` 用 `Number.parseInt(options.port, 10)` 解析端口，所以 `3000abc` 会被当成 3000，`abc` 会变成 NaN。NaN 能绕过 studio server 里的 `options.port ?? 4317`，传给 `server.listen` 后报错。`http.command.ts` 已经有正确的校验：整串都是数字，并且在 1–65535 之间。

## 合理性判断

这是 bug：label 为 bug + good first issue + difficulty: easy。修法和仓库已有的 http 命令保持一致，改动只涉及 CLI 包。

## 改动

- 在 `studio.command.ts` 里新增导出函数 `parsePortOption(raw)`：没传端口时返回 `undefined`，合法时返回端口号，非法时返回 `null`。
- `action()` 在加载 studio 之前先校验端口。非法时输出 `[#corsair]: Invalid --port "<v>". Expected an integer between 1 and 65535.` 并 `process.exit(1)`。
- 新增 `studio.command.test.ts`，共 16 个用例。

## 验证

依赖用 `pnpm install --ignore-scripts --filter @corsair-dev/cli... --frozen-lockfile` 安装。

- 红：去掉 helper 的 import 后，只跑 action 相关用例，在未修复的代码上 2 个都失败：`exits with an error for --port "3000abc"/"abc"`，console.error 里没有出现 Invalid --port。用完整测试文件跑时，会因为 `parsePortOption` 不存在而在 TS 编译阶段失败。
- 绿：`cd packages/cli && npx jest src/commands/studio.command.test.ts` → 16 passed。
- `cd packages/cli && npx jest` → 8 suites，52 tests 全部通过。
- `cd packages/cli && npx tsc --noEmit` → 无错误。
- `pnpm build`（只在 packages/cli 里跑）→ 成功。
- 仓库根目录 `npx biome check .` → 0 error。7 个 warning 在 main 上本来就有，出现在 altoviz、cincopa、gitlab、twochat、zohobigin、www，和本改动无关。
- 没跑的部分：整个 monorepo 的 test 和 build（大约 300 个插件包）。也没有端到端执行 `node dist/index.js ui --port abc`，因为这需要先构建 `corsair` core 包。

## 如何提交

```bash
gh repo fork corsairdev/corsair --clone && cd corsair
git checkout -b fix/1808-studio-port-validation origin/main
git am /path/to/0001-fix-cli-reject-invalid-port-values-for-corsair-ui.patch
pnpm install && pnpm lint && (cd packages/cli && pnpm test && pnpm typecheck)
git push -u origin fix/1808-studio-port-validation
gh pr create --repo corsairdev/corsair --draft --head anyingiit:fix/1808-studio-port-validation \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title

见 `pr_title.txt`：`fix(cli): reject invalid --port values for corsair ui`

## PR body

见 `pr_body.md`。
