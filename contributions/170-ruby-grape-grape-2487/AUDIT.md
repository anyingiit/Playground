# Malicious-code audit — ruby-grape/grape @ afdd3d2 (2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/ruby-grape-grape` (386 text files scanned)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (tool) | none reported | benign |
| npm lifecycle hooks | none (no package.json) | benign |
| Committed binaries | none | benign |
| Pattern findings | none | benign |
| `Rakefile` (manual) | Bundler.setup, gem tasks, RSpec + RuboCop rake tasks only | benign |
| `Gemfile` / `grape.gemspec` (manual) | gems from rubygems.org only (rubocop, rspec, rack-test, danger, simplecov...), no git/path sources, no extensions | benign |
| `spec/spec_helper.rb` + `spec/support/*.rb` (manual) | SimpleCov, Bundler.require, test helpers; grep for system/backticks/exec/Net::HTTP/open-uri/eval: only error-message strings and `instance_exec` in endpoint faker | benign |
| `.github/workflows/*.yml` | standard checkout/setup-ruby/rspec/rubocop/coveralls/danger | benign (not run locally) |

**Verdict: no malicious code found. Safe to `bundle install` and run rspec/rubocop.**
