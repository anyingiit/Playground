# ruby/rdoc#1743 — Broken HTML when crossref matches `#<` without linking `<`

| Item | Value |
|---|---|
| Issue | https://github.com/ruby/rdoc/issues/1743 |
| Tier | 自由 |
| Labels | (none) |
| Status | ✅ ready — patch + PR text done (2026-09-24) |
| Duplicate-PR check | `is:pr 1743` → 0; `is:pr crossref` / `is:pr snippet` → no open PR touching this; issue open, unassigned, no comments (re-checked right before finishing) |
| Base | `master` @ 4355a42f |
| Patch | `0001-Escape-unlinked-cross-references-in-HTML-snippets.patch` |

## 问题理解
Issue 说 CROSSREF 正则匹配到 ` #<`（如 `[#<Encoding:ISO-8859-1>, #<Encoding:UTF-8>]`），`<` 没有被链接，却被当作“已转换的 HTML”原样输出，导致浏览器把 `<Encoding:UTF-8>` 当成标签，HTML 被破坏（Ruby 官方文档 Encoding::Converter#convpath 实例）。

在当前 master 上复现：
- 正文页面（`ToHtmlCrossref`）已经正确转义（未解析时走 `convert_string`；如果上下文里有 `<` 方法，会生成 `<a><code>&lt;</code></a>` 链接，HTML 合法）。
- **仍然出错的是 `RDoc::Markup::ToHtmlSnippet`**：它的 `handle_regexp_CROSSREF` 只去掉前导反斜杠就 `return text`，而 `apply_regexp_handling`（formatter.rb，issue 指出的位置）把返回值当作已转换 HTML，`handle_REGEXP_HANDLING_TEXT` 原样 emit → 原始 `<` 进入输出。
- `ToHtmlSnippet` 用于 `search_snippet`（Aliki 搜索结果 / Darkfish `search_index.js` 的 snippet，前端以 HTML 渲染）。e2e 验证：用 issue 的文字生成 aliki / darkfish 文档，修复前 search index 里是 `[#&lt;Encoding:ISO-8859-1&gt;, #<Encoding:UTF-8&gt;]`，修复后为全转义。

## 合理性判断
明确的 HTML 注入/损坏 bug，维护者活跃并合并外部 PR（近期有多个外部贡献者 PR 合并）。修复是一行、与同文件 `ToHtml#handle_regexp_SUPPRESSED_CROSSREF`（`convert_string(text.delete_prefix('\\'))`）一致。

## 改动
- `lib/rdoc/markup/to_html_snippet.rb`：`handle_regexp_CROSSREF` 改为 `convert_string(text.delete_prefix('\\'))`（snippet 不生成链接，所以直接转义）。
- `test/rdoc/markup/to_html_snippet_test.rb`：新增 `test_convert_CROSSREF_escapes_html`（覆盖 `#<...>` 与 `Foo::<bar>`）。

## 验证
环境：Ruby 3.3.6，`bundle install`（用未提交的本地 Gemfile 副本去掉了 `mini_racer`，节省磁盘）。
- Red（未修复）：`bundle exec ruby -Ilib -Itest test/rdoc/markup/to_html_snippet_test.rb` → 76 tests, 1 failure（输出 `#<Encoding:UTF-8&gt;` / `Foo::<bar&gt;`）
- Green（修复后）：同命令 → 76 tests, 0 failures
- 全量 `bundle exec rake normal_test` → 2459 tests, 5997 assertions, **1 failure**：`RDocParserTest#test_class_for_forbidden`——在未修复的 base 上同样失败（容器以 root 运行，`chmod 0000` 不阻止读取；另外两个同类测试以 "assumes that euid is not root" omit）。
- `bundle exec rake rubygems_test` → 21 tests, 0 failures, 2 omissions
- `bundle exec rubocop <changed files>` → no offenses
- 未运行：依赖 `mini_racer` 的 JS 测试（searcher/search/highlight_bash，未安装时自动跳过）；`verify_generated`（未改 parser 源）。
- e2e：`exe/rdoc -f aliki|darkfish` 生成文档，search index snippet 修复前含原始 `<`，修复后全转义。

## 需要提交者注意
- 仓库 `AGENTS.md` 明确欢迎 AI agent，但规定 PR 描述：**简洁、2–4 段，不要 “Test plan” 小节，不要附 Claude Code session 链接或任何 AI attribution**。下面 PR 正文遵守简洁要求；brief 要求的 motivation/disclosure 段保留了，但它与 “no AI attribution” 有冲突——提交时可自行决定是否删除该段（commit 里没有任何 AI 署名/trailer）。
- 仓库用 squash merge，标题风格为普通句子；无 CHANGELOG 需要维护（History.rdoc 不随 PR 更新）。
- 无 DCO 要求。

## 如何提交
```bash
git clone https://github.com/ruby/rdoc && cd rdoc
git checkout -b fix-snippet-crossref-escape origin/master
git am /path/to/0001-Escape-unlinked-cross-references-in-HTML-snippets.patch
git push <your-fork> fix-snippet-crossref-escape
```

## PR title
Escape unlinked cross-references in HTML snippets

## PR body
```markdown
## Description

`RDoc::Markup::ToHtmlSnippet` doesn't link cross-references, but its `handle_regexp_CROSSREF` returned the matched text unchanged. `apply_regexp_handling` treats a handler's return value as already-converted HTML, so a CROSSREF match such as `#<` in `[#<Encoding:ISO-8859-1>, #<Encoding:UTF-8>]` was emitted with a raw `<`. The resulting search snippets (Aliki search results, Darkfish `search_index.js`) contained `#<Encoding:UTF-8&gt;`, which the browser parses as a tag.

The handler now escapes the text with `convert_string`, the same way `ToHtml#handle_regexp_SUPPRESSED_CROSSREF` does. On current master the regular page output (`ToHtmlCrossref`) already escapes this case, so the snippet formatter was the remaining path; I checked by generating aliki and darkfish docs for the example from the issue, before and after.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1743

## Checklist

- [x] Tests pass locally (`bundle exec rake normal_test`: 2459 tests, 1 failure `RDocParserTest#test_class_for_forbidden`, which also fails on master because the environment runs as root; `bundle exec rake rubygems_test`: 0 failures; new `test_convert_CROSSREF_escapes_html` fails without the fix and passes with it; `rubocop` clean on changed files)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (release notes are generated from PRs)
- [ ] Documentation is updated (if applicable) — n/a
```
