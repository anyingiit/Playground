<!-- claude-projects-attribution: {"github_login":"anyingiit"} -->
_Requested by **winshyon** · [project thread](https://claude.ai/code/project/chan_01H2rJuKkQ8qneVtVjS5nY5K?thread=cmsg_01H2rJuKkQ8qneVtVjS5nY5KPKpHzfAxy5KoBhHBfd3QVb)_

## Description

`TooManyMethods` counted methods defined inside a nested `Foo = Struct.new(...) do ... end` (or `Foo = Class.new do ... end`) towards the enclosing class. `ContextBuilder` already opens a separate module context for such a constant assignment (`defines_module?`), but `ModuleContext#node_instance_methods` uses `local_nodes(:def)`, which only stops at `:class` and `:module` nodes.

This makes `node_instance_methods` leave out `def` nodes found inside a module-defining constant assignment, using the same `defines_module?` check. Other constant assignments that contain a `def` (e.g. `X = class_eval do ... end`, `X = def foo; end`) still count towards the class, as before. Nodes are compared by identity, so an outer method that happens to look exactly like one in the nested definition is still counted. `class << self` bodies, `module_function` and private methods are counted exactly as before.

`node_instance_methods` is also used by `DataClump`, `InstanceVariableAssumption` and `MissingSafeMethod`, which likewise no longer look at a nested Struct/Class definition's methods when checking the outer class.

Reproduction from the issue (with `max_methods: 3`): before, `WeeklyReminder has at least 5 methods`; after, no warning.

Note: open PR #1845 also touches `TooManyMethods` (counting per visibility); this change is in `ModuleContext` and should combine with it.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #1476

## Checklist

- [x] Tests pass locally — four new specs in `spec/reek/smell_detectors/too_many_methods_spec.rb`: nested `Struct.new` / `Class.new` (fail on `master`, pass with the change), plus non-module constant assignments and an identical-looking outer method (still counted); `bundle exec rake ci` (Ruby 3.3.6): spec 1121 examples / 0 failures, features 125 scenarios passed, rubocop no offenses, quality 134 examples / 0 failures
- [ ] `CHANGELOG.md` is updated — left for release time; happy to add an entry if you prefer
- [ ] Documentation is updated — n/a

🤖 Generated with [Claude Code](https://claude.com/claude-code)
