## Description

Building a named scope, e.g. `scope("my_scope", **locals)`, in a view without a configured `scope_namespace` failed deep inside `ScopeBuilder` with an unclear error:

```
NoMethodError: undefined method 'const_defined?' for nil
```

As described in #264, resolving named scopes from the top-level namespace isn't intended, so `scope_namespace` is required for named scopes. `ScopeBuilder` now checks for it before resolving the scope class, and raises `Hanami::View::UndefinedConfigError` with the message `no +scope_namespace+ configured`. This is the same error the view already raises for missing `paths` and `template`.

Unnamed scopes (`scope(**locals)`) and scope classes passed directly (`scope(MyScope, ...)`) don't use the namespace, so they behave as before.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues / help-wanted issues. The change was prepared with Claude Code and checked as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #264

## Checklist

- [x] Spec added in `spec/integration/scope_builder_spec.rb`. It fails before the change (it gets the `NoMethodError`) and passes after.
- [x] Full suite: same results before and after. The 2 `spec/unit/tilt_spec.rb` failures also happen on `main` in my environment.
- [x] RuboCop clean on the changed files
- [x] `CHANGELOG.md` entry under Unreleased / Fixed
