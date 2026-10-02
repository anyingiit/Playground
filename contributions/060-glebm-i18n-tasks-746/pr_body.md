## Description

The Prism-based ERB scanner (`ErbAstScanner#process_comments`) parsed the body of an ERB comment (`<%# ... %>`) as Ruby code, only rewriting `i18n-tasks-use ` into `#i18n-tasks-use `. As a result, any commented-out code inside an ERB comment was treated as live code, e.g.

```erb
<%# ModelClass.human_attribute_name(:unknown) %>
<%# t("some.key") %>
```

was reported as using `activerecord.attributes.model_class.unknown` / `some.key` (and therefore as missing keys). The Parser-based scanner already treats ERB comments as comments and only reads magic comments from them.

This change turns every line of an ERB comment into a Ruby comment (stripping leading whitespace/`#`), so Prism only sees comments and the existing magic-comment handling picks up `i18n-tasks-use` lines (single-line, multi-line and `<%#-` forms keep working), while commented-out code is ignored.

The `comments.html.erb` fixture gets a few commented-out calls (`t(...)`, `human_attribute_name`, multi-line); the Prism spec asserts they are not reported. The same fixture is used by the Parser ERB spec, which already passes with it.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #746

## Checklist

- [x] Tests pass locally (`bundle exec rake` with `RUBYOPT="--enable-frozen-string-literal --debug-frozen-string-literal"` on Ruby 3.3.6: 286 examples, 0 failures, 5 pending — Google Translate specs, no API key). New assertions fail without the fix (11 used keys instead of 8). `bundle exec rubocop`: no new offenses (the 5 `Lint/InterpolationCheck` offenses in `spec/used_keys_erb_spec.rb` also exist on `main`).
- [x] `CHANGES.md` is updated (if applicable) — entry under "Unreleased"
- [ ] Documentation is updated (if applicable) — n/a, behaviour now matches the documented magic-comment usage
