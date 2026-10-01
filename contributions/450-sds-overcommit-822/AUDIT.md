# Malicious-code audit — sds/overcommit @ c06c0f5 (main, "Cut version 0.73.0 (#896)", 2026-09-06)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/overcommit-822` (462 text files) → no auto-executing surface, no npm hooks, no committed binaries, no pattern findings. Manual review of everything that runs on install/test anyway:

| Item | Reviewed | Verdict |
|---|---|---|
| `Gemfile` | rubygems.org source, `gemspec`, rake, rspec ~>3, simplecov 0.21, simplecov-lcov 0.8, pinned rubocop 1.77.0; no git/path sources | benign |
| `overcommit.gemspec` | metadata + deps childprocess, iniparse, rexml; no extensions / install hooks (only a post_install message string) | benign |
| `Rakefile` | only `require 'bundler/gem_tasks'` | benign |
| `spec/spec_helper.rb` + `spec/support/*` | simplecov setup, requires all hook files, git/shell/output helpers (temp git repos); no network, no downloads | benign |
| `.overcommit.yml` (used by lint CI `overcommit --run`) | built-in hooks only (BundleCheck, RuboCop, HardTabs, TrailingWhitespace, YamlSyntax, …); no custom hook scripts in repo (`.git-hooks` absent) | benign |
| `.github/workflows/*.yml` | tests: `bundle exec rspec` on Ruby 2.6–4.0; lint: `overcommit --sign` + `overcommit --run`; release: gem publish on tags (not run here) | benign |

Verdict: **no malicious code found**; safe to `bundle install` (into vendor/ inside the clone) and run rspec/rubocop.
