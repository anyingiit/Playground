## Description

Multipart uploads parsed by `Rack::Multipart` create tempfiles that are only cleaned up when something runs `Rack::TempfileReaper`. Rails includes it by default, but a Grape API served directly by Rack (or by any non-Rails host) left those tempfiles on disk until GC/process exit, as described in #2487.

This adds `Rack::TempfileReaper` as the outermost middleware in `Grape::Endpoint#build_stack` (before `Rack::Head` and `Grape::Middleware::Error`), so the files are closed and unlinked once the response body is closed. Because it sits outside the error middleware, files are also reaped when the endpoint ends with `error!`/a rescued exception, and the reaper itself closes them if an exception escapes.

Notes for reviewers:

- **Mounted inside Rails (or another app that already uses the reaper):** the middleware is idempotent — it does `env['rack.tempfiles'] ||= []` and both reapers just `close!` the same tempfiles (`Tempfile#close!` on an already closed/unlinked file is a no-op). I checked this with an outer `Rack::TempfileReaper` wrapping a Grape API on Rack 3.2.7 and Rack 2.2.24: 201 response, tempfile unlinked, no error.
- The cost is one extra `Rack::BodyProxy` per request on the endpoint stack. I put it in the endpoint stack (rather than the API instance) to mirror `Rack::Head`, which already lives there; happy to move it if you prefer it elsewhere.
- The spec lives next to the existing Tempfile upload spec in `spec/grape/integration/rack_spec.rb`.
- The CHANGELOG line uses a `#XXXX` placeholder, to be amended with the real PR number as AGENTS.md describes.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #2487

## Checklist

- [x] Tests pass locally (`bundle exec rake`: RuboCop 358 files, no offenses; RSpec 3075 examples, 0 failures. Also `rspec spec --exclude-pattern=...` with `gemfiles/rack_2_2.gemfile` (3079 examples, 0 failures) and `gemfiles/rails_8_1.gemfile` (3077 examples, 0 failures). The 2 new examples in `spec/grape/integration/rack_spec.rb` fail on `master` without the change on both Rack 3.2 and Rack 2.2)
- [x] `CHANGELOG.md` is updated (if applicable) — one line under 4.1.0 Features (PR number placeholder to be filled in)
- [ ] Documentation is updated (if applicable) — n/a (no documented behavior changes; no UPGRADING entry since it is not a contract break)
