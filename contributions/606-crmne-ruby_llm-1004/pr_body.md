## Description

`Protocol::Streaming#process_stream_chunk` treated any network read that started with `{` and contained `"error"` as a bare JSON error body. When a read boundary falls inside an SSE event, the next read can start with a brace:

- if that fragment does not parse on its own, it was logged and dropped, so events like `response.completed` (usage, finish reason) were lost and `cost` became `nil`;
- if it does parse (the read starts right after `data: `), it was raised as a `RubyLLM::ServerError` even though the content had already streamed.

A bare JSON body replaces the whole event stream, so this change decides on the first non-blank read, the same way `MCP::HTTP::Stream#feed` does. If the body starts with `{`, reads are buffered on the stream state until the JSON parses and raised when it carries an `error` key. Every other read goes to the SSE parser, which already reassembles events split across reads. `StreamState` gains a `json_body` flag; it lives on the env like the parser, so `ErrorMiddleware` still resets it per attempt.

This answers the open question in the issue by recognising a bare JSON error only at the start of the body. A stream that starts as SSE and later switches to a raw JSON document is no longer treated as an error; I could not find a provider that does that, and in-stream errors still arrive as `event: error` or `data: {"error": ...}` events, which keep working.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code; I have reviewed and understand every line, and verified it as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

Type of change: bug fix. No API changes.

## Related issue

Closes #1004

## Checklist

- [x] Tests pass locally
  - `bundle exec rspec spec/ruby_llm/protocol/streaming_spec.rb`: 23 examples, 0 failures. The three new specs (event JSON starting a new read, event split at an inner brace, bare JSON error body split across reads) fail without the fix and pass with it.
  - `bundle exec rspec --tag ~live --tag ~generator`: 3565 examples, 0 failures
  - `bundle exec rspec spec/ruby_llm/chat_streaming_spec.rb spec/ruby_llm/speech_streaming_spec.rb` (VCR cassettes): 115 examples, 0 failures, 2 pending
  - `bundle exec rubocop` on the changed files, `flay --mass 70 lib/ruby_llm` (score 0), `bundle exec archspec check`: all clean
- [ ] `CHANGELOG.md` is updated (if applicable): n/a, release notes are written at release time
- [ ] Documentation is updated (if applicable): n/a, internal behaviour only
- [x] I used AI tools to help write this code, and I have reviewed and understand all generated code
- [x] No cassettes re-recorded: no wire request changed
