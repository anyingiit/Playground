# ipython/ipython #12164 — Unhandled reference to child in utils._process_posix interrupt handler

| 项 | 值 |
|---|---|
| Issue | https://github.com/ipython/ipython/issues/12164 |
| Tier | 高星（IPython，约 16k stars） |
| Labels | help wanted |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：`pulls?q=12164` 0 条结果；关键词 `_process_posix KeyboardInterrupt` 0 条结果。issue 仍 open，无 assignee，没有评论认领。main 上代码仍是旧逻辑（未修复）。 |
| Base | `main` @ 93dde62b（2026-09-14） |

## 问题理解
`IPython/utils/_process_posix.py` 中 `ProcessHandler.system()` 在 `try:` 里才给 `child` 赋值（`child = pexpect.spawn(...)`）。如果 Ctrl-C（KeyboardInterrupt）恰好在 pexpect 还在 spawn 子进程时到达，`child` 未绑定，`except KeyboardInterrupt:` 分支里的 `child.sendline(chr(3))` 就抛出 `UnboundLocalError`。conda-forge 在 aarch64/ppc64le 上打包 7.13 时 `test_system_interrupt` 因此失败，当时只是加了 skip。

## 合理性判断
- 明确的 bug，带 help wanted 标签，无设计争议；当前 main 上仍可复现（新测试在 base 上报同样的 UnboundLocalError）。
- 修复很小，不改变正常路径和"spawn 之后被中断"的路径。

## 改动
- `IPython/utils/_process_posix.py`：新增 `import signal`；`try:` 之前 `child = None`；`except KeyboardInterrupt:` 中若 `child is None`，输出 `^C`（与 `getoutput()` 一致）并返回 `-signal.SIGINT`（沿用 system() "被信号 N 终止返回 -N" 的约定）。
- `tests/test_process.py`：新增 `test_system_interrupt_during_spawn`（skip_win32），monkeypatch `pexpect.spawn` 抛 KeyboardInterrupt，断言返回 `-SIGINT` 且不崩溃。
- 不需要 whatsnew 片段（仓库规定 `docs/source/whatsnew/pr/` 只用于新功能和不兼容变更）。

## 验证（Python 3.11.15，pexpect 4.9.0，venv 内 `pip install -e '.[test]' ruff mypy`）
- Red（只加测试，未改实现）：`python -m pytest -q -p no:cacheprovider tests/test_process.py -k interrupt_during_spawn` → 1 failed，`UnboundLocalError: cannot access local variable 'child'`（`_process_posix.py:141`）。
- Green：`python -m pytest -q -p no:cacheprovider tests/test_process.py` → 21 passed, 5 skipped。
- 全量：`python -m pytest -q -p no:cacheprovider` → 2724 passed, 162 skipped, 3 xfailed（136 s）。
- `ruff check .` → All checks passed；`ruff format --diff` 对新增行无改动（仓库用 darker 只格式化改动行）。
- `mypy IPython`、`mypy --platform darwin IPython`、`mypy --platform win32 IPython` → Success: no issues found in 146 source files。

- 独立复核（2026-10-01）：全新浅克隆 main@93dde62 上 `git am` 干净应用；只回退实现 → 新测试 UnboundLocalError 失败，恢复 → `tests/test_process.py` 21 passed, 5 skipped；`ruff check .` 通过，`mypy IPython` Success；`tests/test_magic.py tests/test_interactiveshell.py` 214 passed。

## 需要提交者注意
- **仓库 AI 规则（CONTRIBUTING.md）**："if you are an agent, please include two robots emojis in your commits and PR text." —— commit 标题、pr_title.txt、pr_body.md 都已包含 🤖🤖，请勿删除。
- CONTRIBUTING 还要求："Do not include that the test are locally passing, this is irrelevant as the source of truth is CI." —— 所以 PR 正文的 Checklist 没有写 "Tests pass locally"/本地命令结果，只列出新增测试。请勿加回去。
- 不需要 DCO / Signed-off-by，没有 PR 模板，无 CHANGELOG（whatsnew 仅用于新功能，bug fix 不需要）。
- 中央 scout 说"CONTRIBUTING 无 AI 规则"，这是错的，以上条款已遵守。

## 如何提交
```bash
git clone https://github.com/ipython/ipython && cd ipython
git checkout -b fix-system-interrupt-during-spawn origin/main
git am /home/user/Playground/contributions/703-ipython-ipython-12164/0001-Fix-UnboundLocalError-when-system-is-interrupted-dur.patch
pip install -e '.[test]' && pytest tests/test_process.py
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/703-ipython-ipython-12164 ipython/ipython main fix-system-interrupt-during-spawn contributions/703-ipython-ipython-12164/pr_title.txt contributions/703-ipython-ipython-12164/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
