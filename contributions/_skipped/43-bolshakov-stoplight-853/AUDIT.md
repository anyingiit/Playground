# Malicious-code audit — bolshakov/stoplight @ e3b9807 (develop)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/stoplight-853` (287 text files) + manual review.

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| audit tool: auto-exec surface / npm hooks / binaries / pattern findings | none reported | benign |
| `Gemfile` / `Gemfile.lock` | only `rubygems.org` + local `PATH` (the gem itself); no git sources | benign |
| `stoplight.gemspec` | static metadata; deps zeitwerk, concurrent-ruby; no extensions | benign |
| `Rakefile` | bundler gem tasks, RSpec + RuboCop tasks only | benign |
| `.rspec` / `spec/spec_helper.rb` | loads simplecov, support files, `spec/dummy` Rails app; `before`/`after` hooks only `DEL stoplight:test_now_ms_stack` on local Redis | benign |
| `spec/support/database_cleaner.rb` | deletes `stoplight:*` keys on `redis://127.0.0.1:6379/0` (or `STOPLIGHT_REDIS_URL`) | benign (local test DB only) |
| `spec/dummy/` | stock Rails skeleton used by generator specs | benign |
| `bin/ci.rb` | reads `.github/ci-versions.yml`, emits CI matrices JSON; not run by tests except its own unit spec | benign |
| `.claude/settings.json` + `.claude/hooks/session-start.sh` | only fire when Claude Code is opened with this repo as project dir (not done here); script just prints a SKILL.md as JSON context; other hooks run `standardrb`/`steep` | benign |

Verdict: **no malicious code found**; safe to `bundle install` and run specs (Redis started locally on 127.0.0.1:6379).
