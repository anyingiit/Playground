## Description

A constructor type built on `Types::Any` (or any type that no predicates can be inferred from) was ignored when it was the only argument to `value`, `filled` or `maybe`:

```ruby
AnyUpcase = Types::Any.constructor { |v| v.to_s.upcase }

schema = Dry::Schema.Params { required(:stuff).value(AnyUpcase) }
schema.(stuff: "foo").to_h # => {stuff: "foo"}, constructor never called
```

Root cause: in `Macros::DSL#extract_type_spec`, the inferred predicates for such a type are empty, so the method hits `return self if predicates.empty?` *before* `type(resolved_type)` runs. The key keeps its default `Any` type and the constructor is dropped. When a constraint is added (`.constrained(...)`), predicates are inferred, the early return is skipped and the type is set, which is why the reporter's second call worked.

The fix sets the type (when `set_type` is on, as for the normal path) before that early return. Nothing else changes: no rules are added for such a type, as before. With the change, `value`, `filled` and `maybe` all apply the constructor (`{stuff: "FOO"}`).

One visible side effect: in `Params` schemas, `maybe(:any)` (or `maybe` with an Any-based constructor) now gets the `nil | Any` key type, so an empty string is coerced to `nil`, the same as `maybe(:string)` already does. JSON schemas still keep `""`.

A related thing I noticed while tracing this, which I left alone to keep the change focused: when that early return is hit, keyword predicates and blocks given to the same macro are also dropped, e.g. `required(:a).value(:any, included_in?: ["X"])` or `required(:a).filled(:any)` accept any input. Happy to look at that separately if you think it's worth fixing.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues / help-wanted issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #504

## Checklist

- [x] Tests pass locally: `bundle exec rspec` → 3264 examples, 0 failures, 4 pending. The new example in `spec/integration/schema/type_spec.rb` ("using a constructor type built on Any") fails without the fix and passes with it.
- [x] `bundle exec rubocop` → no offenses
- [x] `CHANGELOG.md` updated under Unreleased / Fixed
- [ ] Documentation — n/a (bug fix)
