# AUDIT — crmne/ruby_llm (shallow clone @ 9cc8c5d, 2026-10-01)

`python3 tools/audit_repo.py /home/user/work/ruby_llm` — 1704 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface / npm hooks / committed binaries | none reported | benign |
| long-base64-blob (240) | all in `spec/fixtures/vcr_cassettes/*.yml` (provider `encrypted_content`, `thoughtSignature` etc. in recorded HTTP bodies) | benign: test fixtures, never executed |
| raw-ip-url `spec/docs/rails_persistence_spec.rb:40` | `169.254.169.254` metadata URL in an SSRF-rejection test, stubbed by WebMock | benign |
| secret-paths `docs/_data/provider_coverage.json` | plain prose about Ollama cloud/local | benign (false positive) |
| Gemfile / gemspec | only `source 'https://rubygems.org'`, no git/path gems | benign |
| `spec/spec_helper.rb`, `spec/support/*` (git_environment, socket_configuration, ...) | env cleanup, socket guard that forbids non-localhost connections in unit specs, VCR/simplecov config | benign |
| `.overcommit.yml` | RuboCop, Flay, archspec, rspec-queue, gitleaks; not installed here (we don't run hooks) | benign |

Verdict: nothing malicious; safe to `bundle install` and run targeted specs/RuboCop.
