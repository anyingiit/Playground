## Description

With `validate_keys` on, valid keys of a nested schema under `maybe(:array).each(...)` were reported as "is not allowed":

```ruby
NestedSchema = Dry::Schema.define { required(:bar).filled(:string) }

BrokenSchema = Dry::Schema.define do
  config.validate_keys = true
  required(:foo).maybe(:array).each(NestedSchema)
end

BrokenSchema.(foo: [{bar: "bar"}]).errors.to_h
# before: {foo: {0 => {bar: ["is not allowed"]}}}
# after:  {}
```

Root cause: when `each` gets a schema (or `each(:hash) { ... }`), `Macros::Value#call` / `Macros::Schema#define` only wrap the nested schema in an array when the key's current type is an array. After `maybe(:array)` the type is `nil | array`, which isn't recognised, so the key was retyped as `nil | NestedSchema`, i.e. an optional *hash*. The key map then became `{foo: [:bar]}` instead of `[:foo, [:bar]]`, which is what breaks key validation. The same wrong type also meant `Params` schemas didn't coerce nested string keys (`{"foo" => [{"bar" => "x"}]}` gave `{foo: [{"bar" => "x"}]}`) and didn't drop unknown nested keys.

The fix adds a `maybe_array_type?` check and, for that case, builds `nil | array(NestedSchema)` (the existing `maybe` branch adds the `optional`). This covers both the schema-object form (`each(NestedSchema)`, fixed in `Macros::Value`) and the nested block form `each { hash { ... } }` (fixed in `Macros::Schema#define`); `each(:hash) { ... }` already produced the right type.

Not changed here: `maybe(:array).each(...)` given `nil` raises `NoMethodError` (`undefined method 'map' for nil`) because the `each` rule isn't guarded by the `maybe`. That happens on `main` too, with or without a nested schema, so I left it out to keep this focused; happy to look at it separately.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues / help-wanted issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #455

## Checklist

- [x] Tests pass locally: `bundle exec rspec` → 3267 examples, 0 failures, 4 pending. The 4 new examples in `spec/integration/schema/macros/maybe_spec.rb` (validate_keys and the key map for the schema and `each { hash { ... } }` forms, and Params key coercion) fail without the fix and pass with it; reverting only the `schema.rb` change makes the block-form examples fail.
- [x] `bundle exec rubocop` → no offenses
- [x] `CHANGELOG.md` updated under Unreleased / Fixed
- [ ] Documentation — n/a (bug fix)
