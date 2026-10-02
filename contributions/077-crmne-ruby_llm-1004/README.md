# crmne/ruby_llm #1004 — 流式 SSE 事件跨网络读取被拆分时被丢弃或误报为 ServerError

| 项 | 值 |
|---|---|
| Issue | https://github.com/crmne/ruby_llm/issues/1004 |
| Tier | 新锐 (2025 年起步, ~4.4k stars, 非常活跃) |
| Labels | bug |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | /pulls?q=1004 与 "stream chunk" 关键词检索均无相关 open/merged PR; issue 无 assignee、无认领评论 (2026-10-01) |
| AI 政策 | CONTRIBUTING 允许 AI 工具, 但要求理解提交的每一行; PR 模板有 "AI-generated code" 勾选项; AGENTS.md: 不要 Co-Authored-By / "Generated with" 页脚 |
| Base | `main` @ 9cc8c5d |

## 问题理解
`lib/ruby_llm/protocol/streaming.rb` 的 `process_stream_chunk` 用 `chunk.lstrip.start_with?('{') && chunk.include?('"error"')` 判断"裸 JSON 错误体"。
网络读取边界落在 SSE 事件中间时, 下一次读取可能以 `{` 开头:
1. 片段单独解析失败 → 被 debug 日志后丢弃 (如 Responses 的 `response.completed`, 导致 usage/finish_reason 丢失, cost 为 nil);
2. 片段恰好在 `data: ` 之后开始, 能解析, 且内部含 `"error":null` → 被当作错误抛出 `ServerError`。
OpenAI/Azure/xAI/Perplexity/DeepSeek 等共享该 SSE 路径。

## 合理性判断
明确的 bug (label: bug), issue 作者给了可复现 TCP 拆包例子和建议方案 (仅在 body 开头识别裸 JSON, 与 `MCP::HTTP::Stream#feed` 一致)。不属于新功能, 不需要先批准。

## 改动
- `StreamState` 增加 `json_body` 字段; 首个非空读取决定是否为裸 JSON body。
- 是 JSON body: 在 `state.buffer` 中累积直到能解析, Hash 且有 `error` 键则 `raise_stream_error`。
- 否: 后续所有读取交给 SSE parser (本来就能拼接跨读取的事件)。
- 删除 `json_error_payload?` / `handle_json_error_chunk`。
- spec 新增 3 个用例。

## 验证
- red: 去掉 lib 改动, `bundle exec rspec spec/ruby_llm/protocol/streaming_spec.rb` → 23 examples, 3 failures (正是 3 个新用例)
- green: 带改动 → 23 examples, 0 failures
- `bundle exec rspec --tag ~live --tag ~generator` → 3565 examples, 0 failures (~4 min)
- `bundle exec rspec spec/ruby_llm/chat_streaming_spec.rb spec/ruby_llm/speech_streaming_spec.rb` (VCR 回放) → 115 examples, 0 failures, 2 pending
- `bundle exec rubocop <改动文件>` 干净 (spec 中一处引号已 autocorrect), `flay --mass 70 lib/ruby_llm` score 0, `bundle exec archspec check` passed
- 未运行: generator specs (`--tag generator`, 慢且与改动无关)、appraisal Rails 矩阵、gitleaks 钩子、MCP conformance。

## 需要提交者注意
- 仓库**允许** AI 辅助, 但 CONTRIBUTING 要求"理解每一行"; PR 模板的 "I used AI tools" 和 "I have reviewed and understand" 两项都已在 pr_body 中勾选, 提交前请自己通读 diff (约 46 行)。
- AGENTS.md: 提交信息不要 Co-Authored-By / "Generated with" 页脚; 主题 ≤60 字符, 正文 72 列 (已遵守)。不需要 DCO, 也不需要 AI trailer。
- 账号级政策: 用户可见文字不要用 em dash (pr_body 已避免)。
- CONTRIBUTING 建议 `overcommit --install`; 本地 hooks 会跑 RuboCop/Flay/archspec/rspec-queue/gitleaks。
- 设计取舍 (issue 中维护者的开放问题): 只在 body 开头识别裸 JSON 错误; PR 描述里已说明。维护者若希望不同取舍, 可能会要求修改。

## 如何提交
```bash
git clone https://github.com/anyingiit/ruby_llm && cd ruby_llm   # 先 fork crmne/ruby_llm
git remote add upstream https://github.com/crmne/ruby_llm && git fetch upstream
git checkout -b fix-split-stream-events upstream/main
git am /path/to/077-crmne-ruby_llm-1004/0001-Keep-stream-events-split-across-reads-intact.patch
bundle install && bundle exec rspec spec/ruby_llm/protocol/streaming_spec.rb
git push origin fix-split-stream-events
# 或者使用脚本:
tools/submit_pr.sh contributions/077-crmne-ruby_llm-1004 crmne/ruby_llm main fix-split-stream-events contributions/077-crmne-ruby_llm-1004/pr_title.txt contributions/077-crmne-ruby_llm-1004/pr_body.md
```

PR title: 见 `pr_title.txt`; PR body: 见 `pr_body.md`。
