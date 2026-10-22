# AUDIT: dry-rb/dry-schema @ 4e19e0f (main, 2026-10-01)

`python3 tools/audit_repo.py dry-schema` (266 text files): no auto-executing surface, no npm hooks, no committed binaries, no pattern findings.

| Surface | Reviewed | Verdict |
|---|---|---|
| `Gemfile` / `Gemfile.devtools` | rake, rspec deps, dry-* gems, i18n, json_schemer, super_diff, transproc, simplecov, rubocop; all public rubygems.org gems | benign |
| `dry-schema.gemspec` | standard gemspec, no extensions / install hooks | benign |
| `spec/spec_helper.rb`, `spec/support/*` | warning filters, simplecov, test types; no network/shell | benign |
| `Rakefile` | rspec task only | benign |

Gems installed into a private `BUNDLE_PATH` (benchmarks group excluded). Verdict: safe to run rspec / rubocop.
