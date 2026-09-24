# rnag/dataclass-wizard #219 — Python 3.14: a method named `list`/`dict` on the class breaks annotation resolution

| 项 | 值 |
|---|---|
| Issue | https://github.com/rnag/dataclass-wizard/issues/219 |
| Tier | 自由 |
| Labels | acknowledged, bug, help wanted, typing |
| Status | 🚧 in progress — reproduced on 3.14, investigating fix |
| Duplicate-PR check | 2026-09-24: no PR mentions #219 / annotation resolution (only unrelated #253 open) |

## Notes
- Reproduced on main (v1.0.0) with CPython 3.14.0rc2: `TypeError: 'function' object is not subscriptable` from `annotationlib.ForwardRef.evaluate`.
- Maintainer (rnag) acknowledged; says same happens for `typing.List`, `dict`, etc. when a same-named method exists on the class.
