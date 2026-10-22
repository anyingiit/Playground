<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KPKpHzfAxy5KoBhHBfd3QVb)_

Fixes #1006

`Cassette#initialize` merged the cassette's options into `VCR.configuration.default_cassette_options` without copying the default values. A cassette that didn't set `match_requests_on` therefore shared the *same* array object as the configuration, so `cassette.match_requests_on << :body` silently changed the default for every cassette inserted afterwards in the same process (the intermittent matching failures described in the issue).

The same happened inside VCR itself with tags: with a default `tags: [...]`, `assign_tags` appends e.g. `:preserve_exact_body_bytes` to that array, so the tag leaked into the defaults and into later cassettes.

The fix copies Array and Hash default values (`match_requests_on`, `tags`, `persister_options`, ...) before merging, as suggested in the issue. As discussed there, settings made through `VCR.configure` keep applying globally; only per-cassette changes stay local to the cassette. Other values (symbols, booleans, integers, custom objects) are passed through unchanged.

### Tests

- `spec/lib/vcr/cassette_spec.rb`: two new examples — modifying a cassette's `match_requests_on` and adding a tag via `preserve_exact_body_bytes: true` must leave `default_cassette_options` and the next cassette unchanged. Both fail without the change.
- `bundle exec rspec`: 1999 examples, 0 failures, 1 pending (pending is pre-existing).
- `bundle exec cucumber features/`: 258 scenarios passed.
- Added a CHANGELOG entry under the unreleased section.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

🤖 Generated with [Claude Code](https://claude.com/claude-code)
