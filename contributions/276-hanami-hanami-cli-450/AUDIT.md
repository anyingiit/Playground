# AUDIT: hanami/hanami-cli @ 47075b2 (main)

`python3 tools/audit_repo.py /home/user/work/hanami-cli`: 183 text files scanned; no auto-executing surface, no npm hooks, no committed binaries, no pattern findings.
Only `bundle install` (via a temporary Gemfile copy without `mysql2`, which needs native MySQL headers) and rspec/rubocop were run. The temporary Gemfile was deleted before committing and is not in the patch.
