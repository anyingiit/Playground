Fixes #126.

`Hsts#preload_ready?` still checked the old 18-week minimum `max-age` (10,886,400 seconds). The [HSTS preload list](https://hstspreload.org/#submission-requirements) now requires at least 31,536,000 seconds (one year), so `hsts_preload_ready` could be `true` for domains the list would reject.

### Changes

- New constant `Hsts::PRELOAD_MIN_MAX_AGE = 31_536_000`, used by `preload_ready?`. The comment above the method now describes the preload list's requirements instead of "Google's minimum max-age for automatic preloading".
- Specs:
  - "knows if it's preload ready" now uses a one-year `max-age` and also covers a missing `includeSubDomains`, not only a missing `preload`.
  - A new example checks values above (two years) and just below (31,535,999) the threshold, plus the old 18-week value, which no longer qualifies. It's split from the first example to stay within RuboCop's `RSpec/ExampleLength` and `RSpec/MultipleExpectations` limits.
  - "knows if it's enabled" stubbed `max-age: 0` but asserted `preload?`. It now asserts `enabled?`, which is what the example is about.
- `CHANGELOG.md`: a line under `## 4.0.0` / `### Fixed`, next to the #127 HSTS entry.

### Testing

- `bundle exec rspec`: 191 examples, 0 failures (6 pending, as on `main`). Without the change in `hsts.rb`, the new threshold example fails.
- `bundle exec rubocop`: no offenses.
- `gem build site-inspector.gemspec`: builds.

I ran the specs with a UTF-8 locale (`LANG=C.UTF-8`). Under a US-ASCII locale, the domain parser raises `Encoding::CompatibilityError` on `main` as well, which is unrelated to this change.

### Motivation and disclosure

This is a `good first issue` with a clear description of the fix and the tests. I prepared it with help from an AI coding assistant (Claude Code), reviewed the change myself, and ran the specs and RuboCop listed above.
