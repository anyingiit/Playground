## Description

`hanami generate struct` generates a struct inheriting from the app's or slice's `DB::Struct` base class, but it didn't create that base class when it was missing, so the new struct referenced an undefined constant. This happens for example in an app generated with `--skip-db`, or a slice created before the db layer was added (#450).

This creates the base class when it doesn't exist yet, in the same way `generate part` already creates the base part:

- `app/db/struct.rb` (`Test::DB::Struct < Hanami::DB::Struct`, with `require "hanami/db/struct"`), identical to what `hanami new` generates
- for a slice, also `slices/<slice>/db/struct.rb` (`Main::DB::Struct < Test::DB::Struct`), identical to what `hanami generate slice` generates

Existing base classes are left untouched.

Two notes:

- In an app without hanami-db in the Gemfile, the generated `require "hanami/db/struct"` still needs hanami-db added. That's no worse than before, when the struct referenced an undefined constant.
- Like `generate part`, the app base class path is relative to the current directory. So running the generator from inside a slice directory (where the slice is detected from the cwd) would put it under that slice's folder. I kept the behaviour consistent with `generate part` rather than changing it in one generator only. Happy to fix both if you'd like.

I kept this to structs as the issue asks. `generate relation` and `generate repo` have the same gap with `DB::Relation` / `DB::Repo`. If you'd like, I can extend this PR to them or do it in a follow-up.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues / help-wanted issues. The change was prepared with Claude Code and checked as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Fixes #450

## Checklist

- [x] Specs added in `spec/unit/hanami/cli/commands/app/generate/struct_spec.rb` (app and slice, with and without existing base classes). The 2 "without base struct" examples fail before the change and pass after; the struct spec file passes in full (11 examples)
- [x] The rest of `spec/unit` gives the same results before and after the change (locally, without MySQL/Postgres)
- [x] RuboCop clean on the changed files
- [x] `CHANGELOG.md` entry under Unreleased
