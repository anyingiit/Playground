# benbalter/jekyll-remote-theme#109 — README example theme 404

| 项 | 值 |
|---|---|
| Issue | https://github.com/benbalter/jekyll-remote-theme/issues/109 （good first issue，维护者 10/5 给出修法） |
| Tier | 高星（jekyll-remote-theme ~700★，GitHub Pages 官方支持的插件；benbalter 最近合并外部 PR 很快） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 ~22:20 UTC：无 assignee（Copilot 2025 年被分配，10/5 已取消）；没有 PR 涉及 109/retlab；最大 PR 号 #173 |
| AI 政策 | 仓库有 CLAUDE.md（只限制 agent 发版/打 tag），无 AI 禁令；保留 disclosure 段 |
| Base | `main` @ c6b7497 |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 改动
README 的示例从已归档、且没有 `v1.0.0` tag 的 `benbalter/retlab` 换成 `pages-themes/cayman`：`@v0.2.0`（tag）、`@master`（分支）、`@latest`（Latest release 是 v0.2.0）。Enterprise URL 和带斜杠分支这两个纯语法示例改为 `OWNER/REPOSITORY` 占位符。其余措辞不变。HISTORY.md 的 Unreleased > Fixes 加了一行。

## 验证
- 纯文档改动，没有可写的红→绿测试。
- `git ls-remote` 确认所有 ref 都存在；releases 页确认 v0.2.0 是 Latest。
- 沙箱代理拦截了 codeload（403），没能 `curl -sI`，正文里已请维护者顺手确认。

## 如何提交
```
tools/submit_pr.sh contributions/286-benbalter-jekyll-remote-theme-109 benbalter/jekyll-remote-theme main readme-example-theme contributions/286-benbalter-jekyll-remote-theme-109/pr_title.txt contributions/286-benbalter-jekyll-remote-theme-109/pr_body.md
```
（CLAUDE.md 要求推分支时不带 tag；submit_pr.sh 只推 `HEAD:refs/heads/<branch>`，不受影响。）

## 独立复核（2026-10-22，独立 agent）
- PASS：干净应用；全仓库不再有 retlab；cayman 公开、未归档，有 _layouts 等；gem 拼出的 codeload URL `/zip/v0.2.0`、`/zip/master` 有效；`@latest` 走 Releases API。
- 采纳：加了 HISTORY.md 条目；把正文里无法证实的"没有公开主题有对应 ref"改成准确说法。
- 保留：带斜杠分支用占位符（cayman 没有这种分支，正文已解释）。
