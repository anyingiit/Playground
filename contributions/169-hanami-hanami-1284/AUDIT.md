# AUDIT — hanami/cli (fix target for hanami/hanami#1284)

Clone: `/home/user/work/hanami-cli` (`git clone --depth 1 https://github.com/hanami/cli`), HEAD `b97aa831df610e2cbae7ae2bc0a06fedbe46a9f4` (2026-10-01, "File sync from hanakai-rb/repo-sync").

`python3 tools/audit_repo.py /home/user/work/hanami-cli` → 181 text files scanned: no auto-executing hooks, no npm hooks, no committed binaries, no pattern findings.

| Item | Reviewed | Verdict |
|---|---|---|
| `Rakefile` | bundler gem tasks + RSpec/RuboCop rake tasks only | benign |
| `Gemfile` / `Gemfile.devtools` | gems from rubygems.org plus `github:` sources only in the hanami / dry-rb orgs (hanami, hanami-assets, -action, -db, -router, -utils, dry-system, hanami/devtools); native gems pg/mysql2/sqlite3 | benign (official org sources) |
| `hanami-cli.gemspec` | standard gemspec, no extensions / no shell-outs | benign |
| `spec/spec_helper.rb`, `spec/support/*` | `postgres.rb` / `mysql.rb` shell out to `psql`/`dropdb`/`mysql` only in `after :each, :postgres/:mysql` hooks against localhost test DBs (dropping `hanami_cli_test*` DBs); `system_call.rb` is a test double | benign; not triggered by the specs run here (no DB tags) |
| `.github/workflows/*` | CI matrix (Ruby 3.3–4.0, Rack 2/3), rubocop job; actions pinned by SHA | benign, not run locally |
| `bin/`, `exe/`, `script/` | dev console / gem executable / repo helper scripts | not executed except `exe` code via specs |

Verdict: **no malicious code found**. Safe to bundle and run the targeted specs.
