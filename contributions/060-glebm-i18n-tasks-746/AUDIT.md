# Malicious-code audit — glebm/i18n-tasks @ cf103f2 (2026-09-23)

Command: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/i18n-tasks` (193 text files)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks (install/build/test) | tool: none; gemspec has no `extensions`; Rakefile only defines rspec/irb tasks | benign |
| npm lifecycle hooks | none (no package.json) | benign |
| Committed binaries | none | benign |
| Pattern findings | none | benign |
| `spec/spec_helper.rb`, `spec/support/**` (loaded by every test run) | manual read/grep: simplecov, fixtures helpers, capture_std, tmp test-app dir; no `system`/`Open3`/network calls | benign |
| Gemfile deps (deepl-rb, ruby-openai, yandex-translator, overcommit…) | well-known public gems from rubygems.org; translator specs are skipped without API keys | benign |
| `.overcommit.yml` | only used if `overcommit --install` is run (not run) | benign |

Verdict: nothing suspicious; safe to `bundle install` and run specs/rubocop.
