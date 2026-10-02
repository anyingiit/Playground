# github-linguist/linguist#7949 — Add Uiua

| 项 | 值 |
|---|---|
| Issue | https://github.com/github-linguist/linguist/issues/7949 |
| Tier | 高活跃高Star |
| Labels | Add Language, Good First Issue |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01：`is:pr uiua`（含已关闭）0 结果；issue 无评论、无 assignee、无关联 PR |
| AI 政策 | CONTRIBUTING / .github / AGENTS.md / CLAUDE.md 中无 AI/LLM 限制 |
| Base | `main` @ 5fbdfcb8133be2bed88bf3ce62b2335f50474525 |

## 问题理解
Issue 请求为 Uiua（https://www.uiua.org/ ，扩展名 `.ua`）添加语言支持。维护者打了 `Add Language` + `Good First Issue` 标签（linguist 惯例：确认用量达标后才打此标签）。

## 合理性判断
- 符合 CONTRIBUTING「Adding a language」流程；`.ua` 目前未被任何语言占用，无需 heuristics。
- 有官方 MIT 许可的 TextMate grammar：uiua-lang/uiua-vscode（scope `source.uiua`）。
- 样例取自官方仓库 uiua-lang/uiua（MIT）`examples/`，属真实程序（非 hello world）。

## 改动（单 commit `Add Uiua`）
- `lib/linguist/languages.yml`：新增 Uiua（color `#c87dff`，`language_id: 52486065` 由 `script/update-ids` 生成）
- `.gitmodules` / `vendor/grammars/uiua-vscode`（submodule @ 333e5b12b27a9981f3e9028e7ebd5165b178e60a）
- `grammars.yml`、`vendor/README.md`（`script/list-grammars` 生成）
- `vendor/licenses/git_submodule/uiua-vscode.dep.yml`（`licensed cache` 生成）
- `samples/Uiua/{n-body,markov,http_server}.ua`

## 验证
环境无 Docker daemon，因此没有用 `script/add-grammar`（依赖 docker），而是手动执行其中每一步：
`git submodule add` → 本地 `go build` 的 `tools/grammars/cmd/grammar-compiler add vendor/grammars/uiua-vscode`（输出 `OK! added grammar source ... new scope: source.uiua`，需 libpcre3-dev）→ `licensed cache`（用临时 cache_path 只缓存新模块后拷入，避免浅克隆下误删其他记录）→ `script/list-grammars` → `script/update-ids`。

- red→green（临时测试 `uiua_check_test.rb`，断言 `Language["Uiua"]` 存在、`find_by_extension("foo.ua") == [Uiua]`、官方 3 个示例被分类为 Uiua）：
  - base：`1 runs, 1 assertions, 1 failures`（Uiua language missing）
  - 修复后：`1 runs, 5 assertions, 0 failures, 0 errors`
  - linguist 本身没有逐语言的单元测试惯例，新语言的覆盖由 `test_samples` / `test_grammars` / `test_language`（颜色、id、scope、样例）自动完成，故未提交单独测试文件。
- `bundle exec rake samples && bundle exec rake test`（已 init `vendor/CodeMirror`）：`2051 runs, 41087 assertions, 0 failures, 14 errors, 1 skips`。14 个 error 全部是 `TestRuggedRepository`（浅克隆缺历史 commit，`Rugged::OdbError`），base 上 `test/test_repository.rb` 同样 `14 errors`。
- `script/check-regex-compatibility`：`Checked 607 regexes ... (0 allowlisted failures)`
- `licensed status`：uiua-vscode 通过（CodeMirror 报错仅因临时 cache 目录）。

## 需要提交者注意
- **用量证明**：PR 模板要求附 GitHub code search 链接证明 `.ua` 用于数百个仓库。我无法登录搜索核实数量，请提交前打开 pr_body 中的链接（`path:*.ua ←`）确认结果数量足够（linguist 要求 ≥200 个不同 user/repo）；若关键词不理想可改为其他 Uiua 特有字符。
- **颜色** `#c87dff` 是随意选的紫色，PR 中已如实说明；可改为 Uiua 官方 logo 的颜色。
- 本 patch 含 submodule（gitlink）。`git am` 后需 `git submodule update --init vendor/grammars/uiua-vscode` 才会拉取 grammar 内容（gitlink 已固定 commit 333e5b1）。
- 维护者会关注 PR 模板是否填写完整；pr_body 已按 linguist 模板填写，仅保留相关段落。
- 无需 DCO / Signed-off-by。commit 作者为 anyingiit noreply 邮箱。
- PR 正文已包含 AI 辅助披露段落。

## 如何提交
```bash
git clone https://github.com/anyingiit/linguist && cd linguist   # 先 fork github-linguist/linguist
git remote add upstream https://github.com/github-linguist/linguist && git fetch upstream
git checkout -b add-uiua upstream/main
git am /path/to/0001-Add-Uiua.patch
git submodule update --init vendor/grammars/uiua-vscode
git push origin add-uiua
gh pr create --repo github-linguist/linguist --head anyingiit:add-uiua --title "$(cat pr_title.txt)" --body-file pr_body.md
```
