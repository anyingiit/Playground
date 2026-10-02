## Type of Changes

|     | Type                   |
| --- | ---------------------- |
| ✓   | :sparkles: New feature |

## Description

Adds an optional extension, `pylint.extensions.exit_argument_names`, with a new convention message:

- `non-standard-exit-argument-names` (C3801): `Arguments of __exit__ should be named 'exc_type, exc_value, traceback' instead of 't, v, tb'`

It checks `__exit__` and `__aexit__` methods (sync or async) defined in a class. The expected names are the ones used in the [data model docs](https://docs.python.org/3/reference/datamodel.html#object.__exit__), which use the same three names for `__aexit__`.

To keep false positives low, the check skips:
- signatures with `*args` / `**kwargs`
- signatures that don't have exactly three positional arguments after `self` (`unexpected-special-method-signature` already reports those)
- static methods, class methods, module-level functions and nested functions
- arguments that match `ignored-argument-names` (so `def __exit__(self, *_)` and `def __exit__(self, _, __, ___)` are fine)

I made this an **opt-in extension** rather than adding it to the default special-methods checker on purpose: the convention isn't widely followed. In CPython 3.11's stdlib, for example, `(exc_type, exc_val, exc_tb)` appears ~38 times, `(type, value, traceback)` ~27 times and `(t, v, tb)` ~19 times. Enabling this by default would flood existing code bases. If you'd prefer it in `special_methods_checker.py` (disabled by default, or under a different name or ID), I'm happy to move it. I also didn't reuse `arguments-renamed` as suggested in the issue: that message is about overrides diverging from a parent method, which is a different situation.

The message ID category 38 comes from `script/get_unused_message_id_category.py`. `doc/user_guide/checkers/extensions.rst` and `messages_overview.rst` were regenerated with the doc build helpers in `doc/exts`. pylint's own code base passes the new check, so it could be added to the repo's `pylintrc` `load-plugins` list if you want to dogfood it. I left that out to keep the change small.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #7534

## Checklist

- [x] Tests pass locally (Python 3.11, astroid 4.3.3 pin from `requirements_test_min.txt`)
  - `pytest "tests/test_functional.py::test_functional[exit_argument_names]"`: new functional test; fails before the change (`bad-plugin-value`, expected messages missing), passes after
  - `pytest tests/test_functional.py`: 919 passed, 57 skipped
  - `pytest tests/lint tests/message tests/checkers/unittest_base_checker.py tests/test_self.py`: pass
  - `pytest doc/test_messages_documentation.py -k non-standard-exit`: 2 passed (the 7 other failures there, the spelling and Python-version-specific examples, happen on `main` in my environment too)
  - `ruff check`, `isort --check`, `black --check`, `mypy` on the new module; `pylint --rcfile=pylintrc` on it scores 10.00/10
- [x] News fragment: `doc/whatsnew/fragments/7534.new_check`
- [x] Documentation is updated: `doc/data/messages/n/non-standard-exit-argument-names/` (bad/good/pylintrc/details/related) and regenerated `extensions.rst` / `messages_overview.rst`
