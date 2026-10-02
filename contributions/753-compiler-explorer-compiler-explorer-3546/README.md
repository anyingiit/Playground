# compiler-explorer/compiler-explorer #3546 — Filter out `solc` successful compilation message

| 项 | 值 |
|---|---|
| Issue | https://github.com/compiler-explorer/compiler-explorer/issues/3546 |
| Tier | 高星 |
| Labels | help wanted, lang-solidity, request |
| Status | ✅ ready：patch 和 PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue 没有 assignee、评论或 linked PR。`pulls?q=3546` 无结果。`is:pr solidity` 的 23 个 PR 都没有处理这条消息。`lib/` 里 grep "Compiler run successful" 也无结果，说明还没修。anyingiit 在该仓库没有 PR。 |
| Base | `main` @ 4fac2f0d（2026-10-01） |

## 问题理解
CE 调用 solc 时传 `--combined-json ... -o contracts`。solc 写出产物后会输出一行 `Compiler run successful. Artifact(s) can be found in directory "contracts".`。前端（`static/panes/compiler.ts` 统计 stdout/stderr 行数）把它当成编译输出，于是每次编译成功都会显示输出/警告提示。需要在 `lib/compilers/solidity.ts` 里过滤掉这行。

## 合理性判断
- issue 由维护者提出，带 `help wanted` 标签，scout 也确认这条消息会显示成警告。
- issue 说的 "MSVC 的做法" 在当前代码里找不到对应实现。这里沿用仓库已有的模式：rust.ts、co2.ts、mach.ts 都通过 override `processExecutionResult` 定制输出解析，这里也一样。
- 只影响 solc。solx、resolc、solidity-zksync 直接继承 BaseCompiler，不受影响。Solidity 不支持执行，所以 `processExecutionResult` 在 runExecutable 里的调用也不会受影响。

## 改动
- `lib/compilers/solidity.ts`：新增 `processExecutionResult` override。先调用 super 完成解析，再从 stdout 和 stderr 中去掉以 `Compiler run successful` 开头的行。两个流都过滤：review 阶段核对了 solc 源码 `solc/CommandLineInterface.cpp`（v0.5.17/v0.7.6/v0.8.0/v0.8.20/develop），产物消息 `Compiler run successful. Artifact(s) ...` 走 stdout（sout）；旧版本（<0.8.x 某版）的变体 `Compiler run successful, no output requested.` 走 stderr（serr）；新版还有 `... No contracts to compile.` / `... No output generated.`（stdout）。前缀匹配可覆盖全部。v0.4.26 源码中没有这条消息。
- `test/solidity-tests.ts`（新文件，带 BSD license header）：用 `vi.spyOn(compiler, 'exec')` 打桩后调用 `runCompiler`，覆盖 3 个场景：stdout 中的消息被去掉、stderr 中的变体被去掉、真实 warning 被保留。

## 验证（node 22.23.1 / npm ci）
- Red：`git stash push lib/compilers/solidity.ts && npx vitest run test/solidity-tests.ts`，3 个测试全部失败（`expected [ Array(1) ] to deeply equal []`）。
- Green：`npx vitest run test/solidity-tests.ts`，3 passed。
- `npx biome check lib/compilers/solidity.ts test/solidity-tests.ts`：clean。
- `npm run check`（包括 ts-check 全部 4 个 tsconfig、`biome check .`、check-frontend-imports、check-license-headers，以及 `test-min`，即 SKIP_EXPENSIVE_TESTS 模式的 vitest）：exit 0，136 个测试文件通过、1 个跳过，2106 个测试通过、753 个跳过。
- 提交时 husky pre-commit hook（make prereqs、lint-staged，以及其中相关的 vitest 17 个文件 191 个测试、frontend imports、license headers）全部通过，没有使用 `--no-verify`。注意：本机自带 node 是 22.22.0，hook 要求 ≥22.23.1，所以下载了官方 node 22.23.1 并通过 `NODE_DIR` 指定。
- **没有运行**：完整的 `npm test`（含 expensive tests），以及真实的 solc 编译器。消息文本与所在流已对照 solc 源码核实（见“改动”），但没有用真实 solc 二进制跑过。
- **独立 review 复核（2026-10-01，node 22.22.0，`npm ci --ignore-scripts`）**：`npx vitest run test/solidity-tests.ts` 3 passed；把 `lib/compilers/solidity.ts` 恢复为 4fac2f0 版本后 3 个全部失败（red），恢复后再次通过（green）；`npx biome check lib/compilers/solidity.ts test/solidity-tests.ts` clean；`npm run ts-check` exit 0；在 4fac2f0 的干净 worktree 上 `git apply --check` 通过；patch 作者为 anyingiit，无 AI 模型名。

## 需要提交者注意
- 过滤规则是前缀匹配 `Compiler run successful`。如果维护者希望更严格，可以改成只过滤 stdout 或使用完整正则。
- PR 模板（只有注释）要求跑 `make check`，等同于 `npm run check`，已经通过。模板还邀请在 CONTRIBUTORS.md 加名字，这是可选项，本 patch 没有加，可以自行决定。
- 仓库不要求 DCO、CLA 或 changelog，也不要求 AI trailer。AGENTS.md 欢迎 agent 贡献。
- 不要在 commit 里放 godbolt 短链接，也不要 amend 或使用 `--no-verify`（AGENTS.md 要求）。

## 如何提交
```bash
git clone https://github.com/compiler-explorer/compiler-explorer && cd compiler-explorer
git checkout -b solidity-filter-success-message origin/main
git am /home/user/Playground/contributions/753-compiler-explorer-compiler-explorer-3546/0001-Filter-out-solc-s-successful-compilation-message.patch
npm ci && npx vitest run test/solidity-tests.ts && npm run check
gh pr create --repo compiler-explorer/compiler-explorer --head anyingiit:solidity-filter-success-message \
  --title "$(cat /home/user/Playground/contributions/753-compiler-explorer-compiler-explorer-3546/pr_title.txt)" \
  --body-file /home/user/Playground/contributions/753-compiler-explorer-compiler-explorer-3546/pr_body.md
```
开发 clone 已在 review 后删除；按上面步骤用 `git am` 重建分支即可。注意 pre-commit hook 需要 node ≥22.23.1。

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
