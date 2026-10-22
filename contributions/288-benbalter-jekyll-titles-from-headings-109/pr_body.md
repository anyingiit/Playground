Fixes #109.

With `collections: true`, `inferred_title?` returned true for every `Jekyll::Document`. So a post or collection document with an explicit `title:` in its front matter got that title replaced by its first heading, and with `strip_title` the heading was removed as well. The README says only titles inferred from the filename should be overridden.

### Changes

- `inferred_title?` now treats a document's title as inferred only when it equals the titleized slug of its filename. Jekyll sets the inferred title with `||=`, so an explicit title wins there, and it is now kept here as well.
- The slug comes from the filename the same way `Jekyll::Document#populate_title` derives it, using Jekyll's own dated and dateless filename matchers. Jekyll 4 strips trailing periods from the slug and Jekyll 3 doesn't, so both forms are accepted. A custom `slug:` in the front matter doesn't affect the comparison.
- Fixtures and specs, as asked in the issue:
  - a post with an explicit `title:` and a different H1, which keeps its title, and with `strip_title` keeps its heading too;
  - a post with a custom `slug:`, whose filename-inferred title is still overridden by its heading.
- A `## Unreleased` entry in CHANGELOG.md.

One edge case remains: an explicit title that happens to equal the titleized filename slug (e.g. `title: Test` in `2016-01-01-test.md`) can't be told apart from an inferred one, so it is still overridden. Jekyll gives the document the same data either way. Also, a `title` set through front matter `defaults` now counts as explicit for documents, as it already does for pages, so such sites keep that title instead of the first heading.

### Testing

- `bundle exec rspec`: 48 examples, 0 failures, on Jekyll 4.4.1 and on Jekyll 3.10.0 (`JEKYLL_VERSION="~> 3.0"`). Without the change in `generator.rb`, the explicit-title specs fail. The custom-slug spec guards against comparing with `data["slug"]`.
- `bundle exec rubocop lib spec *.gemspec`: no offenses. To stay under `RSpec/MultipleMemoizedHelpers`, the new specs look up their documents inline.

### Motivation and disclosure

This is a `good first issue` with a clear expected behaviour and requested tests. I prepared it with help from an AI coding assistant (Claude Code), reviewed the change myself, and ran the specs and RuboCop listed above.
