# pylint-dev/pylint #7534 — warn on non-standard `__exit__` argument names

| 项 | 值 |
|---|---|
| Issue | https://github.com/pylint-dev/pylint/issues/7534 |
| Tier | 高星 |
| Labels | Enhancement ✨, Hacktoberfest, Help wanted 🙏, Needs PR |
| Status | ✅ ready（独立复审通过，2026-10-01）— patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：`pulls?q=7534` 0 结果；issue open、无 assignee、无评论、无关联 PR |
| Base | `main` @ 8e75f579（2026-09-30，"Upgrade astroid to 4.3.3 (#11508)"） |

## 问题理解
issue 希望当 `__exit__` 的参数没有按数据模型文档写成 `exc_type, exc_value, traceback` 时给出提示。作者提出了两种做法：新增一个 refactor 消息，或者复用 `arguments-renamed`。没有维护者评论，标签是 Needs PR / Help wanted。

## 合理性判断
- 不复用 `arguments-renamed`：它针对的是子类重写方法时改了参数名，语义不同。改为新增消息 `non-standard-exit-argument-names`（C3801，C 类）。38 是 `script/get_unused_message_id_category.py` 给出的下一个空闲类别。
- 默认开启会产生大量告警（3.11 stdlib 主要用 `exc_type, exc_val, exc_tb` / `type, value, traceback` / `t, v, tb`），所以做成可选 extension，并在 PR 正文里说明：如果维护者希望放进 special_methods_checker，可以再挪过去。
- 消息名、ID、是否做成 extension 都是设计选择，维护者可能要求改。这一点已在 PR 正文中说明。

## 改动
- 新增 `pylint/extensions/exit_argument_names.py`：`ExitArgumentNamesChecker`，处理 `visit_functiondef` 和 `visit_asyncfunctiondef`。
  - 只检查类中的普通方法 `__exit__` / `__aexit__`（`node.is_method()` 且 `node.type == "method"`），因此 staticmethod、classmethod、模块级函数和嵌套函数都会跳过。
  - 带 `*args` 或 `**kwargs` 的签名跳过；self 之后不是恰好 3 个位置参数（posonly 和普通参数合计）的也跳过，这类情况由 `unexpected-special-method-signature` 负责。
  - 匹配 `ignored-argument-names`（默认 `_.*|^ignored_|^unused_`）的参数不算不一致。
  - 消息格式：`Arguments of __exit__ should be named 'exc_type, exc_value, traceback' instead of 't, v, tb'`，confidence HIGH。
- 功能测试：`tests/functional/ext/exit_argument_names/{.py,.rc,.txt}`，共 6 个阳性用例和多个阴性用例。
- 文档：`doc/data/messages/n/non-standard-exit-argument-names/`（bad.py、good.py、pylintrc、details.rst、related.rst）。
- `doc/user_guide/checkers/extensions.rst` 和 `doc/user_guide/messages/messages_overview.rst` 是 doc 构建生成后提交进仓库的文件，这次用 `doc/exts` 里的 `pylint_extensions.builder_inited(None)` / `pylint_messages.build_messages_pages(None)` 重新生成，diff 只包含新条目。
- towncrier：`doc/whatsnew/fragments/7534.new_check`，结尾是 "Closes #7534"，`script/check_newsfragments.py` 检查通过。

## 验证（Python 3.11.15，venv 在 /home/user/work/pylint/.venv，`pip install -r requirements_test_min.txt && pip install -e .`）
- Red（还没有 extension 模块时）：`pytest "tests/test_functional.py::test_functional[exit_argument_names]"` 失败，报 `1: bad-plugin-value`，6 条期望的 `non-standard-exit-argument-names` 都没有出现。
- Green：同一条命令 1 passed。
- `pytest tests/test_functional.py -q`：919 passed, 57 skipped（76s）。
- `pytest tests/lint tests/message tests/checkers/unittest_base_checker.py -q`：160 passed, 7 skipped。`tests/test_self.py` 合并跑：154 passed, 9 skipped, 1 xfailed。
- `pytest doc/test_messages_documentation.py -k non-standard-exit`：2 passed。整个文件有 7 个失败（wrong-spelling-*、anomalous-*-in-string-bad、using-generic-type-syntax-…），原因分别是缺 enchant 词典和 Python 版本差异，与本改动无关。
- `ruff check`、`ruff check --config doc/data/ruff.toml`（doc 示例）、`isort --check`、`black --check`、`mypy`、`pylint --rcfile=pylintrc pylint/extensions/exit_argument_names.py`（10.00/10）都通过。
- 手动运行：`python -m pylint --load-plugins=pylint.extensions.exit_argument_names --disable=all --enable=non-standard-exit-argument-names sample.py` 对 `(exc_type, exc_val, exc_tb)` 报 C3801；对 `pylint/` 自身运行，没有告警。
- 没有运行 pre-commit（hooks 要联网拉取）和 `tox -e docs`（完整 sphinx 构建）。

## 独立复审（2026-10-01）
- 重新读 issue：需求是对非标准 `__exit__` 参数名给出提示，补丁满足（另外覆盖 `__aexit__`）。
- 在 base 8e75f579 上 `grep -rhoE '"[CWERIF]38[0-9]{2}"' pylint` 无结果，C38xx 空闲。
- 新 worktree（8e75f579）上 `git am 0001-*.patch` 干净应用，结果树与 `exit-argument-names` 分支一致。
- 移走 `pylint/extensions/exit_argument_names.py` 后 `pytest "tests/test_functional.py::test_functional[exit_argument_names]"` 失败，恢复后通过；`doc/test_messages_documentation.py -k exit` 通过。
- `ruff check --force-exclude`、doc ruff 配置、black、isort、mypy、`pylint --rcfile=pylintrc --fail-on=I`（10.00/10）、`script/check_newsfragments.py` 均通过。
- 额外手测：子类把 `exc_val, exc_tb` 改成标准名不会触发 `arguments-renamed`；带关键字参数 `*, extra=None` 的标准签名不报；函数内定义的类中的 `__exit__` 照常检查。
- PR 正文中 CPython 3.11 stdlib 的统计（38/27/19）已用 grep 复核。补丁无需修改。

## 需要提交者注意
- 仓库没有 AI 政策（AGENTS.md / CONTRIBUTING / .github 都查过），不要求 DCO 或 AI trailer。PR 模板只要求 Type of Changes、Description、Closes，以及 towncrier fragment，均已包含。
- 消息名、ID 和"做成 extension"的选择可能会被维护者要求调整，PR 正文已主动提出可以修改。
- 如果维护者希望 pylint 自己也启用这个检查，可以在仓库 `pylintrc` 的 load-plugins 里加上它（pylint 自身代码 0 告警）。

## 如何提交
```bash
git clone https://github.com/pylint-dev/pylint && cd pylint
git checkout -b exit-argument-names origin/main
git am /home/user/Playground/contributions/116-pylint-dev-pylint-7534/0001-Add-optional-extension-for-non-standard-__exit__-arg.patch
pytest "tests/test_functional.py::test_functional[exit_argument_names]" tests/test_functional.py -q
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/116-pylint-dev-pylint-7534 pylint-dev/pylint main exit-argument-names contributions/116-pylint-dev-pylint-7534/pr_title.txt contributions/116-pylint-dev-pylint-7534/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
