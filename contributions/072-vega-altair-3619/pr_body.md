## Description

Unregistering the currently active plugin via `PluginRegistry.register(name, None)` only removed it from `_plugins`, leaving `_active` / `_active_name` / `_options` pointing at the removed entry. As described in #3619, after `alt.theme.unregister(...)` on the active theme, `alt.theme.active` still reported the removed theme and `alt.theme.enable()` failed with a confusing `NoSuchEntryPoint` error.

Changes:
- `PluginRegistry.register(name, None)`: if the removed plugin was active, fall back to the `"default"` plugin when one is registered (every built-in Altair registry has one), otherwise clear the active plugin and its options. Unregistering an inactive plugin is unchanged.
- `alt.theme._register(name, None)` now goes through `_themes.register(name, None)` instead of popping `_plugins` directly, so `alt.theme.unregister` gets the same behavior.
- Tests: two new `PluginRegistry` tests (with/without a `"default"` plugin) and the commented-out `# BUG: #3619` assertion in `test_theme_unregister` is now enabled (`theme.active == "default"`).

Note: an earlier attempt (#4086) was closed by its author without being merged.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #3619

## Checklist

- [x] Tests pass locally
  - `pytest tests/utils/test_plugin_registry.py tests/vegalite/v6/test_theme.py` → 34 passed (the 3 new/enabled tests fail without the fix)
  - `pytest -n 3 tests/utils tests/vegalite -m "not slow and not datasets_debug and not no_xdist"` → 520 passed, 11 skipped, 1 xfailed, 1 xpassed
  - `ruff check` / `ruff format --diff --check` → clean; `mypy` on the changed files → no issues
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (release notes are generated from PR titles)
- [ ] Documentation is updated (if applicable) — n/a (behavior noted in the `register` docstring)
