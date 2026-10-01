# glebm/i18n-tasks#746 — Prism reports offenses in comments

| 项 | 值 |
|---|---|
| Issue | https://github.com/glebm/i18n-tasks/issues/746 |
| Tier | 自由 |
| Labels | 无 |
| Status | ✅ ready — patch + PR text written, red→green verified, full suite + rubocop run |
| 重复 PR 检查 | 2026-10-01 查看 /pulls：唯一 open PR 为 #756（OrcaRouter backend，无关）；issue 无评论、无 assignee |
| Base | `main` @ cf103f2 |

## 问题理解
Prism ERB 扫描器 `ErbAstScanner#process_comments` 把 `<%# ... %>` 的内容当 Ruby 代码解析（只把 `i18n-tasks-use ` 替换成 `#i18n-tasks-use `），
所以注释掉的 `<%# Foo.human_attribute_name(:x) %>`、`<%# t('k') %>` 会被当成使用的 key → 报 missing。Parser 扫描器则只把它当注释、仅读取 magic comment。

## 合理性判断
ERB 注释不会执行，报告其中的 key 明显是 bug（与 Parser 扫描器行为不一致）。仓库无 AGENTS/CLAUDE/CONTRIBUTING 文件，labels 无 AI 相关规定，未发现禁止 AI 贡献的政策。

## 改动
- `lib/i18n/tasks/scanners/erb_ast_scanner.rb`：注释内容逐行去掉前导空白/`#` 后加 `#`，整体变成 Ruby 注释，只由现有 magic comment 逻辑处理。
- fixture `comments.html.erb` 末尾加 3 个注释掉的调用（`t`、`human_attribute_name`、多行）；`spec/used_keys_erb_prism_spec.rb` 断言它们不被报告。
- `CHANGES.md` Unreleased 加一条。

## 验证（Ruby 3.3.6，`LANG=C.UTF-8`，否则 fixture 中的 `×` 会因 US-ASCII 报错——环境问题，与本改动无关）
- Red（无修复）：`bundle exec rspec spec/used_keys_erb_prism_spec.rb:316` → `expected: 8, got: 11`；`not_to include` 断言亦失败（列出 3 个 commented_out key）。
- Green：`bundle exec rspec spec/used_keys_erb_prism_spec.rb spec/used_keys_erb_spec.rb` → 11 examples, 0 failures。
- 全量：`RUBYOPT="--enable-frozen-string-literal --debug-frozen-string-literal" bundle exec rake` → 286 examples, 0 failures, 5 pending（Google Translate 无 API key）。
- `bundle exec rubocop` → 5 offenses（`spec/used_keys_erb_spec.rb` 的 Lint/InterpolationCheck），在 base 上同样存在，非本改动引入。

## 需要提交者注意
- 无 DCO、无 AI trailer 要求；commit 作者 anyingiit（noreply 邮箱），无 Signed-off-by。
- PR body 含 Claude Code 披露段落。
- CI 的 rubocop job 若在 main 上已因那 5 个 offense 失败，与本 PR 无关（可在 PR 中说明）。
- 行为变化：`<%# foo i18n-tasks-use t('x') %>`（magic comment 不在行首）不再被识别；Parser 扫描器原本也不识别，属一致化。

## 如何提交
```bash
git clone https://github.com/glebm/i18n-tasks && cd i18n-tasks
git checkout -b fix-erb-comment-prism origin/main
git am /path/to/0001-Prism-Do-not-scan-code-inside-ERB-comments.patch
# 或者用脚本（在 Playground 根目录）：
tools/submit_pr.sh contributions/451-glebm-i18n-tasks-746 glebm/i18n-tasks main fix-erb-comment-prism contributions/451-glebm-i18n-tasks-746/pr_title.txt contributions/451-glebm-i18n-tasks-746/pr_body.md
```

## PR
- Title: 见 `pr_title.txt`
- Body: 见 `pr_body.md`
