# Audit — danger/danger @ c94d38b3ce68 (shallow clone, 2026-10-01)

Tool: `python3 /home/user/Playground/tools/audit_repo.py /home/user/work/danger` + manual review of Gemfile, danger.gemspec, Rakefile, bin/.

| Hit / file | Reviewed | Verdict |
|---|---|---|
| Auto-executing hooks / npm lifecycle / committed binaries | none reported | — |
| spec/fixtures/circle_build_*.json `curl … \| bash` | Recorded CircleCI API responses used as JSON test fixtures; never executed | benign |
| spec/fixtures/circle_build_*.json secret-paths | Same fixtures (CircleCI step script text) | benign |
| Gemfile | Only rubygems.org source, standard dev gems (rspec, rubocop, webmock, …); no git/path sources | benign |
| danger.gemspec | Plain metadata + runtime deps; no extensions, no post-install hooks | benign |
| Rakefile | rspec/rubocop/chandler release tasks; not run here (rspec invoked directly) | benign |
| bin/danger, bin/console | Load lib and run Danger::Runner / IRB | benign |

Verdict: nothing malicious; safe to `bundle install` (into vendor/bundle) and run rspec / rubocop.
