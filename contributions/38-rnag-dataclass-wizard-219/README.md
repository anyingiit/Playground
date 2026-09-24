# rnag/dataclass-wizard #219 — Python 3.14: a method named `list`/`List`/`dict` on the class breaks annotation resolution

| 项 | 值 |
|---|---|
| Issue | https://github.com/rnag/dataclass-wizard/issues/219 |
| Tier | 自由 |
| Repo | rnag/dataclass-wizard (~200★, Python, Apache-2.0) |
| Labels | acknowledged, bug, help wanted, typing |
| Status | ✅ ready — patch + PR text written |
| Duplicate-PR check | 2026-09-24 (checked twice, the second time right before finishing): no PR mentions #219 or annotation/shadowing. Open PRs are only #249, #253, #256, #257, all on other topics. Issue unassigned, no one has claimed it in the comments |
| Base | `main` @ 57535e9 (v1.0.0) |
| Patch | `0001-Fix-class-methods-shadowing-annotation-names-on-Pyth.patch` |

## 需要提交者注意
- 没有找到 AI 相关政策（没有 AGENTS.md / CLAUDE.md，CONTRIBUTING.rst 也没提），CONTRIBUTING 写明 “Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it”。PR 描述里已写 disclosure 段落。
- 没有 PR 模板，也没有 DCO/CLA 要求。HISTORY.rst 由维护者在发版时写，所以 PR 不改它。
- 维护者 rnag 会合并外部 PR（例如 #234 Charles Fauman），但他是一波一波处理的：上一次合并在 2026-07-02 的 v1.0，之后外部 PR #249/#253 一直开着。合并可能要等一段时间。
- 本地 uv 能拿到的 3.14 是 **3.14.0rc2**（不是 3.14 正式版）。复现和修复都在 rc2 上验证，涉及的 `annotationlib.ForwardRef.evaluate` 的 owner→locals 逻辑在正式版里也一样。

## 问题理解
在 Python 3.14 (PEP 649/749) 里，注解是惰性求值的，而且能看到类的命名空间。所以下面这个类的注解 `list[str]` 在 VALUE 格式下会求值成 `<function list>[str]`，并抛出 `TypeError`：
```python
@dataclass
class Inv(JSONWizard):
    items: list[str]
    def list(self): ...
```
`dataclasses` 在 3.14 用 FORWARDREF 格式，会把它存成 `ForwardRef('list[str]', owner=Inv)`。dataclass-wizard 在 `eval_forward_ref()` 里调用 `typing._eval_type(fref, module_globals, None)`。`locals=None` 时，`ForwardRef.evaluate()` 会用 `vars(owner)`（类命名空间）当 locals，于是 `list` 又解析成那个方法，报 `TypeError: 'function' object is not subscriptable`。`from_dict`/`to_dict` 都会失败，v1 和 v0 两套实现都有这个问题。在 3.13 及更早的版本上不会出现，因为那时 locals 为 None，只用模块 globals。维护者在评论里确认了这是 bug，并补充说 `typing.List`、`dict` 等同样会被同名方法影响。

## 合理性判断
- 维护者已加 `acknowledged` + `help wanted`，并在评论里明确说需要让注解解析更健壮。
- 仓库 main 上已经复现：CPython 3.14.0rc2 下 `from_dict` 抛出和 issue 一样的 `TypeError`。

## 改动
`dataclass_wizard/utils/_typing_compat.py` 和 `dataclass_wizard/v0/utils/typing_compat.py` 做了同样的改动：
- 新增 `_get_typing_locals(base_type)`。在 3.14+ 上，如果 ForwardRef 有 `__owner__` 且它是一个类，就返回 `vars(owner)`，但去掉那些**不可能是类型**的成员（`FunctionType`、`BuiltinFunctionType`、`classmethod`、`staticmethod`、`property`、`functools.cached_property`）。这样 `list`/`List`/`dict` 会落回模块 globals 或 builtins，而嵌套类等真正的类型仍然能从类命名空间解析。3.14 以下直接返回原来的 `_TYPING_LOCALS`，行为不变。
- `eval_forward_ref()` 改为把 `_get_typing_locals(base_type)` 作为 localns 传进去。
- 回归测试：`tests/unit/test_loaders.py::test_class_methods_do_not_shadow_types_in_annotations`（v1，包含 `list()` 方法、`List()` 方法、`dict` property、嵌套类 `Inner`，并做 round-trip），以及 `tests/unit/v0/test_load.py::test_class_methods_do_not_shadow_types_in_annotations`（v0）。
- 已知不覆盖的情况（PR 里也说明了）：不带下标的 `items: list` 在 3.14 下由 Python 自己直接求值成那个方法，不会生成 ForwardRef，这是语言语义，本 PR 不处理。

## 验证
隔离的 venv 放在 `/home/user/work/dcw-venv*`，uv 缓存放在 `/home/user/work/dcw-cache`，验证完已全部删除。
```
# red（不带修复，CPython 3.14.0rc2）
python -m pytest -q -p no:cacheprovider -o log_cli=false tests/unit/test_loaders.py tests/unit/v0/test_load.py -k shadow
  -> 2 failed (TypeError: 'function' object is not subscriptable)
# green（带修复，3.14.0rc2）
  -> 2 passed
# 全量（CI 在 tox 里等价于 PYTEST_ADDOPTS=--ignore-glob=*integration* pytest）
3.14.0rc2 base : 884 passed, 2 skipped, 6 xfailed, 4 xpassed
3.14.0rc2 patch: 886 passed, 2 skipped, 6 xfailed, 4 xpassed
3.13.12   patch: 886 passed, 2 skipped, 6 xfailed, 4 xpassed
3.12.3    patch: 886 passed, 2 skipped, 6 xfailed, 4 xpassed
3.11.15   patch: 885 passed, 2 skipped, 6 xfailed, 4 xpassed   (差 1 个是 conftest 在 <3.12 上就会 skip 的文件)
flake8 dataclass_wizard/utils/_typing_compat.py dataclass_wizard/v0/utils/typing_compat.py
  -> 只剩 main 上本来就有的 F401/E302（与本改动无关）；测试文件只多了 2 条 F405（JSONWizard 来自 star import，和文件里其它几百条一样）
python -m compileall -q dataclass_wizard -> OK
```
还手工验证了：继承场景（字段在父类、方法在父类）、嵌套类 + `list` 方法 + `List` 方法 + `Dict` property 组合，都能正常 load/dump。

## 如何提交
```bash
git clone https://github.com/<you>/dataclass-wizard.git && cd dataclass-wizard
git checkout -b fix-219-py314-class-method-shadowing origin/main
git am /path/to/0001-Fix-class-methods-shadowing-annotation-names-on-Pyth.patch
git push -u origin fix-219-py314-class-method-shadowing
# 向 rnag/dataclass-wizard:main 开 PR
```

## PR title
Fix class methods shadowing annotation names on Python 3.14 (fixes #219)

## PR body
```markdown
## Description

On Python 3.14 (PEP 649/749), a forward reference created by `annotationlib` is evaluated against the namespace of the class that owns the annotation. So with

    @dataclass
    class Inv(JSONWizard):
        items: list[str]
        def list(self): ...

`dataclasses` stores `items` as `ForwardRef('list[str]', owner=Inv)`. When `eval_forward_ref()` resolves it with `localns=None`, `ForwardRef.evaluate()` falls back to `vars(owner)`, so `list` becomes the method and loading fails with `TypeError: 'function' object is not subscriptable`. Both the v1 and v0 loaders are affected. As noted in the issue, `typing.List`, `dict`, and similar names hit the same problem when a method of the same name exists.

This PR adds a small `_get_typing_locals()` helper (used by `eval_forward_ref()` in both `utils/_typing_compat.py` and `v0/utils/typing_compat.py`). On 3.14+, when the forward ref has a class `__owner__`, the helper passes that class's namespace as locals, minus members that can never be a type: functions, builtin functions, `classmethod`/`staticmethod`, `property`, and `cached_property`. Names like `list`/`List`/`dict` then resolve from the module globals or builtins again, while real class-level types such as nested classes still resolve. On Python < 3.14 the behavior is unchanged (`_TYPING_LOCALS` as before).

Scope note: a *bare* `items: list` next to a `list()` method is evaluated by Python itself to the method, and no ForwardRef is involved, so this PR doesn't change that case.

Regression tests were added for v1 (`tests/unit/test_loaders.py`) and v0 (`tests/unit/v0/test_load.py`). The v1 test covers a `list()` method, a `List()` method, a `dict` property, and a nested dataclass, with a round-trip. Both tests fail on `main` under 3.14 with the `TypeError` from the issue and pass with this change. They also pass on older Pythons, where the method never interfered.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #219

## Checklist

- [x] Tests pass locally (`pytest --ignore-glob=*integration*`): 886 passed, 2 skipped, 6 xfailed, 4 xpassed on CPython 3.14.0rc2, 3.13 and 3.12, and 885 passed on 3.11. The new tests fail on unpatched `main` under 3.14 and pass with the fix. `flake8` reports nothing new in the changed modules.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (HISTORY.rst is written at release time)
- [ ] Documentation is updated (if applicable) — n/a
```
