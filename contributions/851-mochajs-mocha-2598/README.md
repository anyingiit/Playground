# mochajs/mocha#2598 — done(circularObj) 报 "Converting circular structure to JSON"

| 项 | 值 |
|---|---|
| Issue | https://github.com/mochajs/mocha/issues/2598 |
| Tier | 高星 |
| Labels | area: reporters, status: accepting prs, type: bug（Milestone: Backlog） |
| Status | ✅ ready — patch + PR text done (not submitted)；PR 描述需提交者本人审阅/改写（见下）。独立复审 2026-10-01：重新 npm ci 后复跑 red(55/1)->green(56)、test-node:unit 1289 passing、tsc、prettier/eslint 均通过；PR 模板中的 `fixes #2598` 即关闭关键字 |
| Base | `main` @ 79db2ee (2026-10-01, mocha 12.0.3) |
| Duplicate-PR check | 2026-10-01：`pulls?q=2598` 0 结果；关键词 `circular`、`"non-Error"` 搜索无针对本 issue 的 open/merged PR（#6227 是另一个 issue #5641 的 cyclic toStringTag，已关闭）；issue 无评论、无 assignee、无关联 PR |

## 问题理解

`it(..., function (done) { ... done(obj) })` 中若 `obj` 是普通对象（`[object Object]`），`lib/runnable.js` 的 `callFnAsync` 会构造
`new Error("done() invoked with non-Error: " + JSON.stringify(err))`。当对象含循环引用时 `JSON.stringify` 自己抛
`TypeError: Converting circular structure to JSON`，用户只能看到这个 TypeError，看不到真正的失败原因（"done() 被传入非 Error"）。
在 12.0.3 上复现：

```
1) circular:
   TypeError: Converting circular structure to JSON
   --> starting at object with constructor 'Object'
     at JSON.stringify (<anonymous>)
     at file:///.../lib/runnable.js:398:58
```

## 合理性判断

- 维护者标了 `status: accepting prs` + `type: bug`，问题在当前 main 仍可复现，需求明确，无需设计讨论。
- AI 政策：`.github/CONTRIBUTING.md` 的 “🤖 AI-Generated Code” 一节允许 AI 辅助，条件：全部自动检查通过、人工审查、**PR/issue 描述要简短**（“AI-generated PR descriptions tend to be verbose and low-quality”）、提交者对代码负责。仓库有 `AGENTS.md`（已遵循：最小改动、不改生成的 `mocha.js`、跑 tsc/smoke/对应 test-node 套件）。
- runner.js 中对抛出的非 Error 值已经用 `utils.stringify`（`thrown2Error`），本修复与之一致。

## 改动

- `lib/runnable.js`：新增私有函数 `safeStringify(value)`：先 `JSON.stringify`，抛异常时回退到 `utils.stringify`（会把循环引用标成 `[Circular]`，也能处理 BigInt 等）。非循环对象的输出与原来**完全一致**（现有测试 `'done() invoked with non-Error: {"error":"Test error"}'` 不变），保持兼容。
- `test/unit/runnable.spec.cjs`：新增 “when done() is invoked with a circular non-Error object” 测试，断言得到 Error、消息以 `done() invoked with non-Error: ` 开头并包含 `"error": "Test error"` 与 `"self": [Circular]`。
- 修复后输出：
  ```
  Error: done() invoked with non-Error: {
    "b": [Circular]
  }
  ```
- 不需要 CHANGELOG（release-please 根据 Conventional Commit 自动生成）；无文档改动。

## 验证

环境：Node v22.22.0，`npm ci --ignore-scripts`（与 CI 相同）。

| 命令 | 结果 |
|---|---|
| 复现：`node bin/mocha.js --no-config circ.spec.cjs`（done(循环对象)） | 修复前 TypeError: Converting circular structure to JSON；修复后 `Error: done() invoked with non-Error: {"b": [Circular]}` |
| 仅回退 `lib/runnable.js`，`node bin/mocha.js test/unit/runnable.spec.cjs` | **55 passing, 1 failing**（新测试：`expected 'Converting circular structure to'... to begin with 'done() invoked with non-Error: '`）→ red |
| 打补丁后同命令 | 56 passing → green |
| `npm run test-node:unit` | 1289 passing, 3 pending |
| `npm run test-node:interfaces` | 全部 passing（7/3/2/2） |
| `npm run test-node:reporters` | 158 passing |
| `npm run test-node:integration -- --jobs 2`（限制并行） | 385 passing, 1 pending, 0 failing |
| `npm run test-smoke` | 1 passing |
| `npm run tsc` | 通过 |
| `npm run format:check` | All matched files use Prettier code style |
| `npm run lint:code`（eslint --max-warnings 0） | 通过 |
| `npm run lint:knip` | exit 0（仅一条既有的 configuration hint，与本改动无关） |
| `npm run build` | 成功（随后 `npm run clean`） |

未运行：`npm run test-browser`（需要 Playwright + Chromium `--with-deps`，此环境不安装）；`test-node:jsapi`、`test-node:requires`、`test-node:only`、`lint:installed-check`、`lint:knip-docs`（与改动无关）。改动是纯 JS 逻辑，浏览器 bundle 可正常构建。

## 如何提交

```bash
git clone https://github.com/mochajs/mocha && cd mocha
git checkout -b fix-done-circular-non-error origin/main
git am /path/to/0001-fix-handle-circular-objects-passed-to-done.patch
git push <your-fork> fix-done-circular-non-error   # PR 目标分支: main
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`（已按 mocha 的 PR 模板：PR Checklist + Overview）。

### 需要提交者注意
- **CONTRIBUTING 要求 PR 描述简短、经人工审阅**：`pr_body.md` 已刻意写短（未使用 chefs-pick 模板的长段落，只保留一句披露），提交前请本人审阅/按自己的话改写。
- 需签署 **CLA**（OpenJS Foundation EasyCLA，机器人会提示）；无 DCO，不要加 Signed-off-by。
- 提交信息用 Conventional Commits（`fix: ...`），CHANGELOG 由 release-please 生成，无需手改。
- 维护者曾关闭新贡献者同时开的多个 PR（#6227 评论：“Please wait for us to review your first PR before opening more”）——如对 mocha 还有其他 PR 在等审核，建议先等那个处理后再提这个。
- Codecov 覆盖率下降视为失败：新增分支（catch 回退）已被新测试覆盖。
