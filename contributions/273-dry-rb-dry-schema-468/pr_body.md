## Description

With the struct extension, a single invalid attribute made every other coercible attribute fail too (the case from #468):

```ruby
class MyStruct < Dry::Struct
  attribute :date, Types::JSON::DateTime
  attribute :number, Types::JSON::Decimal
  attribute :string, Types::String
end

schema = Dry::Schema.Params { required(:data).value(MyStruct) }

schema.(data: {date: "00", number: 42, string: "Hi!"}).errors.to_h
# before: {data: {date: ["must be a date time"], number: ["must be a decimal"]}}
# after:  {data: {date: ["must be a date time"]}}
```

Root cause: in `extensions/struct.rb`, `Macros::Hash#call` already defines the nested schema from the struct's attributes (`super(schema, ...)` adds a `required`/`optional` key with each attribute's type, so each key is coerced on its own). It then also did

```ruby
type(schema_dsl.types[name].constructor(schema))
```

which wraps the key's type in a constructor that runs the whole input through the struct's hash schema first. That coercion is all-or-nothing: if any attribute fails, the constructor gives back the original hash and none of the values are coerced, so valid-but-uncoerced values (an Integer for a decimal, a String for a date) then fail their type checks as well.

The fix removes that extra constructor and relies on the per-key types of the nested schema. The line dates back to the original extension, when it wrapped the struct class itself (#253); since #378 it has wrapped `struct.schema`, which the nested schema already covers.

I compared old and new output with `Params`, `define` and `JSON` schemas; `value`, `hash`, `maybe`, `array` and `each`; and structs using `transform_keys`, `attribute?`, defaults, nested structs and arrays, and nested hash schemas. For valid hash input to `value`, `hash` and `maybe`, the output is unchanged, and `key_map`, `json_schema` and `info` output are identical. The removed line also replaced the key's type with a hash constructor even for `array(Struct)` / `each(Struct)`, so valid coercible elements were reported as errors; those are now coerced too. `maybe(Struct)` now accepts `nil`, and `nil` given to `value(Struct)` in JSON/define schemas gives "must be a hash" (as with a plain `hash`) instead of one "is missing" error per attribute. The existing struct, json_schema and info specs pass unchanged.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues / help-wanted issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #468

## Checklist

- [x] Tests pass locally: `bundle exec rspec` → 3268 examples, 0 failures, 4 pending. Of the 5 new examples in `spec/extensions/struct_spec.rb`, 4 fail without the fix and pass with it (invalid input, `array(struct)`, `maybe(struct)` with `nil`); the plain valid-input one passes either way.
- [x] `bundle exec rubocop` → no offenses
- [x] `CHANGELOG.md` updated under Unreleased / Fixed
- [ ] Documentation — n/a (bug fix)
