# helix-editor/helix#3115 — gherkin 接入 cucumber-language-server

| 项 | 值 |
|---|---|
| Issue | https://github.com/helix-editor/helix/issues/3115 |
| Tier | 高星（helix ~45k★，非常活跃） |
| Labels | A-language-support, C-enhancement, E-easy（**不是** good-first-issue 标签） |
| Status | ✅ ready（独立复核 PASS） |
| 重复 PR 检查 | 2026-10-22 20:20 UTC：`is:pr cucumber OR gherkin` 只有已合并的 #11083（高亮）和无关 #12453；issue 无 assignee、无关联 PR；2024-01 有人说"也想试试"，之后无动静 |
| AI 政策 | 仓库无 AI_POLICY / AGENTS / CONTRIBUTING 中的 AI 条款；PR 正文含披露段落 |
| Base | `master` @ ba40e54 |
| DCO / CLA / changeset | 无 |
| 需先认领 | 否 |

## 问题理解
issue 要两件事：gherkin 高亮 + LSP。高亮已由 #11083 合并（languages.toml 里已有 gherkin language/grammar），LSP 还没接。官方 `@cucumber/language-server`（VS Code Cucumber 扩展用的同一个）提供诊断（未定义步骤）、补全、跳转、格式化等。

## 合理性
维护者 the-mikedavis 在 issue 里指引按"添加语言"流程做；helix 一直在 languages.toml 里收录各语言的默认 LSP，属于常规改动。

## 改动
- `languages.toml`：在顶部按字母排序的 `[language-server]` 内联表里加 `cucumber-language-server = { command = "cucumber-language-server", args = ["--stdio"] }`（csharp-ls 与 cuelsp 之间；与 npm 包 bin 名和 nvim-lspconfig 一致），gherkin 加 `language-servers = [ "cucumber-language-server" ]`（用仓库多数的带空格写法）。
- `book/src/generated/lang-support.md`：`cargo xtask docgen` 重新生成，只变 gherkin 一行。

## 验证
- `HELIX_DISABLE_AUTO_GRAMMAR_BUILD=1 cargo xtask docgen` → 只改 gherkin 行（也证明 languages.toml 可被解析）。
- `cargo build -p helix-term`；`PATH=<cukeglobal>/bin:$PATH hx --health gherkin` → `✓ cucumber-language-server`。
- LSP 实测（脚本 scratchpad/lspprobe.py，按 helix 的行为：initialize 带 rootUri/workspaceFolders，`workspace/configuration` 回 `[null]`——见 helix-term/src/application.rs 1051 行，无 config 时返回 null）：
  - `npm install -g --prefix ... @cucumber/language-server`（1.7.0）后，对 `features/greeting.feature` + `features/step_definitions/steps.ts`：服务器请求 `cucumber` 配置 → 用默认 glob → "Found 2 step definitions"，诊断只剩没写完的 `When I eat`。
  - 注意：如果用**本地**（非 -g）安装，npm 会把 language-service 提升到顶层 node_modules，而 bin 脚本按 `../node_modules/@cucumber/language-service/dist` 找 wasm，会出现 "Parsing failed"、找不到步骤定义。这是该 npm 包自身的路径假设，`npm install -g` 正常；PR 正文里写的安装方式就是 `-g`。
- `cargo test -p helix-core -p helix-loader`：166 passed / 2 failed（`test_textobject_queries`、`test_pretty_print` 需要已编译的语法；在 master 上同样失败，原因是关闭了语法构建）。

## 需要提交者注意
- 无 AI 条款，但正文有披露段落。
- 维护者有时会让顺手在 wiki "Language Server Configurations" 页加条目，这是 wiki 不在 PR 里，可在 PR 合并后视情况补。

## 如何提交
```
D=$PWD/contributions/360-helix-editor-helix-3115
tools/submit_pr.sh $D helix-editor/helix master gherkin-cucumber-lsp $D/pr_title.txt $D/pr_body.md
```

## 独立复核（2026-10-22 20:55 UTC，独立 agent）
- issue open、无关联 PR；`cucumber`/`gherkin`/`3115` 搜 PR 只有已合并的 #11083；仓库无 AI 政策、无 PR 模板。
- 新克隆 ba40e54 上 `git am` 干净；样式与邻近条目一致；在打补丁的树上重跑 `cargo xtask docgen` 无差异。
- `hx --health gherkin` → ✓；确认 helix 无 config 时回 `[null]`，服务器走默认 glob，探测中找到 2 个步骤定义，最终只报未写完的那步。
- 意见：①"published diagnostics only…"略夸大（索引前约 3 秒会先报两步未定义）→ 已改为 "once indexing finished, reported…"；② TOML 改动无需列 cargo test → 已删除。
- 结论：PASS

## 追加修改（21:20 UTC）
361 的复核指出：helix 的 languages.toml 里约 215 个简单 LSP 都写在文件顶部按字母排序的 `[language-server]` 内联表，只有少数带复杂配置的才单独开 `[language-server.X]` 段。360 原先单独开段，已改为内联表一行（csharp-ls 与 cuelsp 之间）。重验：docgen 无差异、`hx --health gherkin` ✓、与 361 一起 `git am` 无冲突。
