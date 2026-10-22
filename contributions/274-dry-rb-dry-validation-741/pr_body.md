## Description

From dry-rb/dry-validation#741: with a `filter` inside a nested hash, one failing filter stops every other value in that hash from being coerced. The same keys at the top level work as expected.

```ruby
schema = Dry::Schema.Params do
  required(:transfer).hash do
    required(:first_date).filter(format?: /\A\d{4}-\d{2}-\d{2}\z/).value(:date)
    optional(:last_date).filter(format?: /\A\d{4}-\d{2}-\d{2}\z/).value(:date)
  end
end

schema.(transfer: {first_date: "2025-01-01", last_date: ""}).to_h
# before: {transfer: {first_date: "2025-01-01", last_date: ""}}
# after:  {transfer: {first_date: #<Date 2025-01-01>, last_date: ""}}
```

In dry-validation this shows up as a rule for `first_date` receiving a `String`, which is what the reporter saw. It reproduces with current dry-validation `main` + dry-schema `main`; with this patch the rule receives a `Date`, and dry-validation's own suite passes against the patched dry-schema (228 examples, 0 failures, 1 pending).

Root cause: when the result already has errors, `ValueCoercer#call` coerces key by key and skips any top-level key with `input.error?(name)`, which is true for an error anywhere *under* that key. So a nested filter error on `transfer.last_date` made the whole `transfer` hash stay raw.

The fix keeps the existing behaviour when the error is on the key itself (e.g. "must be a hash"), and when errors are only deeper inside the value, it coerces the value and then puts the original input back under each failing path. Values that failed a filter are therefore still left untouched (the second new spec checks that `"2025/01/02"`, which `Params` would happily parse, is kept as is), while their siblings are coerced as they would be at the top level. As a side benefit the error paths are compiled once per call instead of once per key.

One limitation I left alone: with `maybe(:hash) { ... }`, if the failing value can't be coerced at all, the lax sum type returns the whole hash unchanged, so its siblings stay raw there. That also happens without filters, so it comes from how the sum type coerces rather than from this code.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues / help-wanted issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes dry-rb/dry-validation#741

## Checklist

- [x] Tests pass locally: `bundle exec rspec` → 3266 examples, 0 failures, 4 pending. All 3 new examples in `spec/integration/schema/filter_spec.rb` (nested and two-level nested hashes) fail without the fix and pass with it.
- [x] `bundle exec rubocop` → no offenses
- [x] `CHANGELOG.md` updated under Unreleased / Fixed
- [ ] Documentation — n/a (bug fix)
