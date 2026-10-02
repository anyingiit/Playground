### Summary

Follow-up for #309. The main fix for that issue (`blocking: true` on `create_client_from_uri`, so `Valkey.new` releases the GVL while glide-core connects/retries) already landed in #316. This PR takes care of the two loose ends: it removes the unused `create_client` binding the issue suggested dropping, and adds a regression test so the GVL release can't silently go away again.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

### Issue link

- Closes [(ffi): Set blocking: true on create_client_from_uri ffi](https://github.com/valkey-io/valkey-glide-ruby/issues/309)

### Changes

- `lib/valkey/bindings.rb`: removed the `attach_function :create_client` (byte/protobuf-request variant). Nothing in `lib/` or `test/` calls it, because clients are only created through `create_client_from_uri`. Also added a short comment explaining why `create_client_from_uri` is `blocking: true`.
- `test/unit/connection_gvl_test.rb` (new, no server needed): opens a local `TCPServer` that completes the TCP handshake but never answers, then calls `Valkey.new(..., connect_timeout: 0.5)` while a ticker thread runs. It asserts that the connect really waited (≥ 0.2 s) and that the ticker ran at least 10 iterations during it.
- `CHANGELOG.md`: one line next to the existing #316 entry.

### Limitations

The test leaves out `reconnect_attempts: 0` because of the known #117 behaviour, so it uses the default retry strategy and depends only on `connect_timeout`.

### Testing

- Red → green: with `blocking: true` temporarily removed from `create_client_from_uri`, the new test fails with `only 0 ticker iterations ran during a 0.5s connect; create_client_from_uri appears to hold the GVL`. With the flag restored, it passes. Ran it 5 more times in a row and it passed every time (~0.55 s each).
- `bundle exec rake test:unit` → `460 tests, 1169 assertions, 0 failures, 0 errors, 0 skips`
- `bundle exec rubocop` → `129 files inspected, no offenses detected`
- Integration suites (`test:standalone` / `test:cluster`) not run locally: no Valkey server in my environment. This change doesn't touch any command path.
- Run on Ruby 3.3.6 / ffi 1.17.4 / Linux x86_64, using the `libglide_ffi.so` from the published `valkey-glide-rb` 1.0.0 gem.

### Checklist

Before submitting the PR make sure the following are checked:

- [x] This Pull Request is related to an issue.
- [x] Commit message describe your changes
- [x] Commits are signed off (`git commit -s`) per the DCO.
- [x] Tests are added or updated.
- [x] CHANGELOG.md and documentation files are updated.
- [x] Linters have been run (`bundle exec rubocop`) and pass.
- [x] Destination branch is correct - main.
