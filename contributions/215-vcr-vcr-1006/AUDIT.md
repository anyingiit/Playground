# AUDIT — vcr/vcr @ a747bb6

`python3 tools/audit_repo.py` on a shallow clone: 122 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface / npm hooks / committed binaries | none reported | — |
| Pattern findings | none | — |
| `script/install-apt-deps.sh` (CI) | `apt-get install libcurl4-openssl-dev` only | benign |
| Gemfile | standard gems from rubygems.org (HTTP client libs, rspec, cucumber) | benign |

Verdict: nothing suspicious; safe to bundle install and run rspec/cucumber.
