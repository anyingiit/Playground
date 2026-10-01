# github-linguist/linguist#7949 — Add Uiua

| 项 | 内容 |
|---|---|
| Issue | https://github.com/github-linguist/linguist/issues/7949 |
| Tier | 高活跃高Star |
| Labels | Add Language, Good First Issue |
| Status | ✅ 补丁 + PR 文本已就绪（提交前必须先人工确认 GitHub 搜索用量，见下） |
| 重复 PR 检查 | 2026-10-01：PR 搜索 "uiua" 0 结果；issue 无评论、无 assignee；languages.yml 中无 Uiua/.ua |
| AI 政策 | 仓库有 AGENTS.md（为 AI agent 写的指南），允许 AI 协助，但规定了 PR 必备条件（见下）；无禁止条款 |

## 问题理解
请求把 Uiua（栈式数组语言，扩展名 `.ua`）加入 Linguist。issue 未给语法 URL；官方 VS Code 扩展 uiua-lang/uiua-vscode 提供 `syntaxes/uiua.tmLanguage.json`（MIT，scope `source.uiua`）。

## 合理性判断
- 维护者已打 `Add Language` + `Good First Issue` 标签。
- `.ua` 在 Linguist 中未被其他语言占用 → 无需 heuristic。
- **关键前置条件（我无法验证）**：CONTRIBUTING/AGENTS.md 要求 `.ua` 在 GitHub code search（排除 fork、近一年索引）≥ **2000 个文件**，且分布在足够多的 user/repo 上（会用 `-user:` 排除语言作者）。code search 需要登录，本环境看不到数量。AGENTS.md 明确写 "Do not open a PR if any of the above conditions are not met"。

## 改动（单个 commit "Add Uiua"）
- `lib/linguist/languages.yml`：新增 Uiua（type programming, `.ua`, tm_scope source.uiua, ace_mode text, language_id 52486065 由 `script/update-ids` 生成；update-ids 顺手改了 LLVM TableGen 一处行尾空格，已还原以保持最小改动）。
- submodule `vendor/grammars/uiua-vscode` @ 333e5b1，`.gitmodules`、`grammars.yml`、`vendor/README.md`、`vendor/licenses/git_submodule/uiua-vscode.dep.yml`（与 `script/add-grammar` 产物一致）。
- `samples/Uiua/http_server.ua`、`samples/Uiua/markov.ua`：取自 uiua-lang/uiua@ac326eb `examples/`（MIT），非 hello world。
- 未设置 color（可选字段）。

由于本机没有 Docker 守护进程，`script/add-grammar` 无法直接运行，我手工执行了它的等价步骤：本地编译 `tools/grammars` 的 grammar-compiler（链接 vmg/pcre），`git submodule add`，`grammar-compiler add vendor/grammars/uiua-vscode` → `OK! added grammar source ... new scope: source.uiua`，`bundle exec licensed cache`（只保留新增 dep.yml，其余因 submodule 未检出被误删的文件已还原），`rake samples`、`script/sort-submodules`、`script/list-grammars`。

## 验证
- red → green：`bundle exec bin/github-linguist samples/Uiua/markov.ua` 用 base 的 languages.yml → `language:`（空）；改后 → `language: Uiua`。
- `bundle exec rake test`：改后 2051 runs / 2 failures / 15 errors；base（5fbdfcb）2049 runs / 2 failures / 15 errors，失败集合完全相同（TestRuggedRepository 因浅克隆缺历史对象；TestLanguage 的 CodeMirror 检查因 vendor/CodeMirror submodule 未检出）——均为环境问题，与本改动无关。新增的 2 个 run 为新样本的测试，通过。
- `bundle exec script/cross-validation --test` → "Number of errors (14) is within the acceptable threshold (14)"。
- 未运行：CI 中的 `rake check_grammars`（需 Docker）。

## 需要提交者注意
1. **先确认用量**：打开 https://github.com/search?type=code&q=NOT+is%3Afork+path%3A*.ua+%E2%86%90+-user%3Auiua-lang （登录状态），数量需 ≥ 2000 且分布合理；把 pr_body.md 中的 `<FILL IN ...>` 替换为实际数量；不达标就**不要提交**（按 AGENTS.md / CONTRIBUTING 会被直接关闭），在 issue 中保留即可。必要时调整 pr_body 中的搜索链接（可以去掉 `←` 关键字或再加 `-user:` 排除高占比用户）。
2. 必须使用仓库 PR 模板（pr_body.md 已按模板填写，并插入了 disclosure 段）。
3. 不需要 DCO / Signed-off-by；commit 作者 anyingiit <49945850+anyingiit@users.noreply.github.com>。
4. 补丁里包含 submodule gitlink（Subproject commit 333e5b1）。如果 `git am` 后 submodule 状态有问题，最稳妥的做法是在 Docker 可用的机器上直接 `script/add-grammar https://github.com/uiua-lang/uiua-vscode` 重做语法部分，再拷贝 samples、改 languages.yml、`script/update-ids`。
5. color 未设置；如需要可后续补充并在模板中写明理由。

## 如何提交
```bash
git clone https://github.com/anyingiit/linguist && cd linguist   # 先在 GitHub 上 fork
git remote add upstream https://github.com/github-linguist/linguist && git fetch upstream
git checkout -b add-uiua upstream/main
git am /path/to/0001-Add-Uiua.patch
git submodule update --init vendor/grammars/uiua-vscode
git push -u origin add-uiua
gh pr create --repo github-linguist/linguist --head anyingiit:add-uiua --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
Add Uiua

## PR body
见 `pr_body.md`。
