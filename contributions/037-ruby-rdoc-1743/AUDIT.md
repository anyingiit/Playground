# Malicious-code audit — ruby/rdoc @ 4355a42f (master, 2026-09-24)

Tool: `python3 /home/user/Playground/tools/audit_repo.py rdoc-1743` (248 text files scanned)

| Hit / surface | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface (install/build/test hooks) | tool: none | benign — no hooks |
| npm lifecycle hooks | tool: none; `package.json` only has `lint:css` (stylelint) script | benign |
| Committed binaries | none | benign |
| Pattern findings | none | benign |
| `Gemfile` (manual) | rubygems.org only; dev gems rake/racc/kpeg/test-unit/rubocop/gettext/webrick; optional `prism` from github only when `PRISM_VERSION=head`; `mini_racer` for JS tests | benign (mini_racer not installed locally to save disk) |
| `Rakefile` (manual) | test tasks via Rake::TestTask; `generate`/`verify_generated` run racc/kpeg/rubocop on in-repo parser files | benign |
| `rakelib/epoch.rake` (manual) | runs `git log -1 --format=%ct` to set SOURCE_DATE_EPOCH for `build` | benign |
| `test/lib/helper.rb` (manual) | requires test-unit + core_assertions only | benign |
| `rdoc.gemspec` (manual) | runtime deps erb, tsort, prism, rbs | benign |

Verdict: **no malicious code found; safe to run the test suite.**
