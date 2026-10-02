# mitsuhiko/minijinja#956 — Rendering loops forever when an iterator's __next__ keeps raising (Python bindings)

| 项 | 值 |
|---|---|
| Issue | https://github.com/mitsuhiko/minijinja/issues/956 |
| Tier | 自由 |
| Labels | 无 |
| Status | ✅ ready — independently reviewed 2026-10-01 (issue open, 0 PRs; git am clean on main@5978498; red→green re-run; commit scope aligned to upstream `fix(py):`) |
| 重复 PR 检查 | 2026-10-01 复查：`/pulls?q=956` 0 条；open PR 仅 #957(match)、#940(wordwrap)、#902(auto escape)，无重叠；issue 无 assignee、无评论 |
| Base | `main` @ 5978498 |

## 问题理解
`minijinja-py/src/typeconv.rs` 中 `DynamicObject::enumerate` 用 `filter_map` 收集 Python 迭代器，`__next__` 抛出的异常被直接丢弃；若迭代器一直抛异常而不 `StopIteration`，`collect()` 永不结束 → 100% CPU 死循环。

## 合理性判断
明确的 bug（DoS 级挂死），issue 里给了复现；作者在 #814 已让属性查找异常向上抛出，本修复与之一致。AI 政策：HEAD 提交 "docs: remove AI disclosure requirement"，README 有 "AI Use Disclaimer"（项目自身也用 AI），未禁止 AI 贡献；无 PR 模板、无 DCO 要求。

## 改动
- `typeconv.rs`：遇到第一个错误即停止，把错误作为 invalid value（`Value::from(to_minijinja_error(err))`，即 `Value` 文档里的 "fallible iteration" 模式）放在末尾。VM 的 `Iterate` 指令对每个 item 做 `assert_valid!`，因此 for 循环会抛出原始 Python 异常（`ValueError`）。
- `tests/test_basic.py`：新增 `test_iteration_errors`（迭代器抛 100 次后才 StopIteration，回归时测试失败而不是挂死；并断言 `__next__` 只调用 1 次）。
- `CHANGELOG.md`：Unreleased 加一条（引用 #956，项目惯例是 PR 号，提交后可改成 PR 号）。

## 验证（/home/user/work/minijinja/minijinja-py，uv venv py3.11，`maturin develop`）
- red（未改 typeconv.rs）：`pytest tests/test_basic.py -k iteration_errors` → `FAILED ... DID NOT RAISE ValueError`
- green：`pytest` → 49 passed
- issue 原始复现脚本：修复后输出 `raised ValueError('backend unavailable')`，不再挂死
- `pyright python` → 0 errors；`cargo fmt -p minijinja-py -- --check` OK；`cargo clippy -p minijinja-py -- -F clippy::dbg-macro -D warnings` 无警告
- `black --check tests python`：本地新版 black 会重排现有 `test_loop_controls`（版本差异，非本改动引入）；新增测试本身符合 black，已不包含无关格式化改动。

## 需要提交者注意
- 提交作者：anyingiit <49945850+anyingiit@users.noreply.github.com>；仓库无 DCO / AI trailer 要求，未加。
- PR body 已含 disclosure 段落（项目已移除强制 AI 披露要求，保留无妨）。
- CHANGELOG 条目引用的是 issue 号 #956，若维护者希望用 PR 号可在 PR 开出后修改。

## 如何提交
```bash
git clone https://github.com/mitsuhiko/minijinja && cd minijinja
git checkout -b fix-python-iter-errors origin/main
git am /path/to/055-mitsuhiko-minijinja-956/0001-*.patch
# 或使用工具脚本：
tools/submit_pr.sh contributions/055-mitsuhiko-minijinja-956 mitsuhiko/minijinja main fix-python-iter-errors contributions/055-mitsuhiko-minijinja-956/pr_title.txt contributions/055-mitsuhiko-minijinja-956/pr_body.md
```

## PR
标题见 `pr_title.txt`，正文见 `pr_body.md`。
