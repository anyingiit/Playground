Fixes #67.

`Generator#option` read `site.config["optional_front_matter"][key]` without checking the type, so `optional_front_matter: true` in `_config.yml` crashed the build with `undefined method '[]' for true`. An array value raised a `TypeError` instead.

### Changes

- `option(key)` now returns the value only when the config is a Hash, the same `is_a?(Hash)` guard jekyll-default-layout uses. A non-hash value is treated as no configuration, so the plugin keeps its default behaviour (enabled, no cleanup). This includes `optional_front_matter: false`, which was already ignored before; disabling the plugin still takes `enabled: false`.
- A `## Unreleased` entry in CHANGELOG.md.
- Specs for `optional_front_matter: true` and for an array value. Both generate the pages as with no config. Without the fix both fail.

### Testing

- `bundle exec rspec`: 40 examples, 0 failures. The 2 new examples fail without the change in `generator.rb`.
- `bundle exec rubocop lib spec *.gemspec`: no offenses. `gem build` succeeds.

The issue also mentions the same pattern in jekyll-titles-from-headings (`generator.rb`, lines 88–90). I can send the same guard there as a separate PR.

### Motivation and disclosure

This is a small, well-described `good first issue`. I prepared it with help from an AI coding assistant (Claude Code), reviewed the change myself, and ran the specs and RuboCop listed above.
