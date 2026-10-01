# sds/overcommit#822 — TextWidth should not fail on long URL lines

| 项 | 值 |
|---|---|
| Issue | https://github.com/sds/overcommit/issues/822 |
| Tier | 自由 |
| Labels | enhancement, help wanted |
| Status | ✅ ready — patch + PR 文本完成（2026-10-01） |
| 重复 PR 检查 | 2026-10-01：`/pulls?q=is:pr 822` 0 条；`/pulls?q=is:pr TextWidth` 只有 2014–2018 年的无关 PR；issue 无 assignee、无评论认领 |
| Base | `main` @ c06c0f5 (Cut version 0.73.0) |

## 问题理解
`CommitMsg::TextWidth` 对正文中每一行超过 `max_body_width`(默认 72) 的都报 warning，包括整行只有一个 URL 的情况。URL 无法折行，所以这种警告不可修复。Issue 请求：只含 URL 的行允许超长。

## 合理性判断
维护者打了 `help wanted`；CONTRIBUTING 欢迎 feature PR，要求加测试并通过 `bundle exec rspec` 和 `bundle exec overcommit --run`。仓库没有 AI 贡献禁令（grep LLM/AI-generated/Copilot/ChatGPT 无结果），不需要 DCO，也不需要 AI trailer。

## 改动
- `lib/overcommit/hook/commit_msg/text_width.rb`：新增 `URL_ONLY_LINE` 正则（`[label]: ` 可选前缀 + `scheme://\S+`，整行 strip 后匹配）和 `url_only_line?`；正文检查时跳过这类行。URL 加其他文字的行仍报错。subject 检查不变，没有新配置项。
- `spec/.../text_width_spec.rb`：新增 3 个 context（纯 URL 行 pass、`[1]: url` pass、URL+文字仍 warn）。

## 验证
- Red：仅加 spec，`bundle exec rspec spec/overcommit/hook/commit_msg/text_width_spec.rb` → 2 个新用例失败。
- Green：加修复后 → 19 examples, 0 failures。
- `bundle exec rubocop <两个文件>` → no offenses。
- 全量 `bundle exec rspec` → 1647 examples, 5 failures（author_email_spec ×3、author_name_spec ×1、committing_spec ×1）；`git stash` 回 base 后这 3 个文件同样 5 failures，是本环境 git 配置导致，与改动无关。
- `bundle exec overcommit --sign pre-commit && bundle exec overcommit --run` → All pre-commit hooks passed。

## 需要提交者注意
- 提交作者为 anyingiit <49945850+anyingiit@users.noreply.github.com>；仓库不要求 DCO / AI trailer，所以 commit 里都没有。
- 没有改 CHANGELOG：该仓库的 CHANGELOG 只有已发布版本的条目、没有 unreleased 段，看起来是维护者在发版时写的。PR checklist 里说明了，可按维护者要求再补。
- 设计取舍：豁免默认开启、没有加配置开关；如果维护者想要可配置（例如 `allow_long_urls`），后续再加。
- CI 在 Ruby 2.6–4.0 上跑；用到的 `Regexp#match?` 从 2.4 起就有。

## 如何提交
```bash
git clone https://github.com/sds/overcommit && cd overcommit
git checkout -b text-width-allow-long-urls origin/main
git am /path/to/0001-Allow-URL-only-lines-to-exceed-TextWidth-body-limit.patch
# 或使用工具脚本（在 Playground 根目录）：
tools/submit_pr.sh contributions/450-sds-overcommit-822 sds/overcommit main text-width-allow-long-urls contributions/450-sds-overcommit-822/pr_title.txt contributions/450-sds-overcommit-822/pr_body.md
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。
