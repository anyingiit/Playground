# AUDIT — valkey-io/valkey-glide-ruby @ f6225af (shallow clone)

`python3 tools/audit_repo.py /home/user/work/valkey-glide-ruby` — 146 text files scanned.

| Hit | Reviewed | Verdict |
|---|---|---|
| Auto-executing surface | none (no extconf/native ext in gemspec; Rakefile only defines native:build (cargo in submodule, not run) and test tasks) | benign |
| npm lifecycle hooks | none | n/a |
| Committed binary `.github/files/redisearch-amd64-v2.10.24.so` | Valkey module loaded by CI test server only (`test/lint/vector_search_commands.rb` expects `/tmp/modules/redisearch.so`); never loaded by us | benign (not executed here) |
| Committed binary `.github/files/librejson-v2.8.15.so` | same, CI-only server module | benign (not executed here) |
| Committed binary `.github/files/redisbloom-amd64-v2.6.12.so` | same, CI-only server module (`test/lint/module_commands.rb`) | benign (not executed here) |
| Pattern findings | none | — |

Manual review: `test/test_helper.rb`, `test/support/*` only set constants / require helpers; `bin/setup` = `bundle install`.
Native lib `libglide_ffi.so` was NOT built from the submodule; it was taken from the official RubyGems release `valkey-glide-rb-1.0.0` (x86_64-linux-gnu) to run unit tests.

Verdict: no malicious code found; safe to run unit tests + rubocop.
