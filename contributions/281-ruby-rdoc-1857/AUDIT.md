# AUDIT: ruby/rdoc @ 0b82ffd (master, 2026-10-20)

`python3 tools/audit_repo.py /home/user/work/rdoc`: 249 text files scanned; no auto-executing surface, no npm hooks, no committed binaries, no pattern findings.
Only `bundle install`, the test suite (`rake test`), rubocop and `exe/rdoc` on local sample files and on rdoc's own docs were run.

The repo has an `AGENTS.md` for AI agents. It does not forbid AI-assisted contributions, but it requires short PR descriptions (2–4 paragraphs, no "Test plan" section, **no AI attribution or session link**). pr_body.md follows that.
