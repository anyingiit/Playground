# fsspec/projspec#69 — Allow walk to take an integer value

| 项 | 值 |
|---|---|
| Issue | https://github.com/fsspec/projspec/issues/69 |
| Tier | 自由 |
| Labels | enhancement, good first issue (issue type: Feature; project board "Projspec Plans" → Backlog) |
| Status | ✅ ready — patch + PR text done (not submitted) |
| Base | `main` @ dc5de4c (2026-07-12) |
| Duplicate-PR check | PR list (all states, and `walk` keyword) checked 2026-09-24 at start and again before finishing: no PR touches `walk`; issue has 0 comments, unassigned, no linked branch/PR |

## 问题理解

`projspec.Project(path, walk=...)` 目前只接受 `True`（遍历整棵树）/ `False`（不下探）/ `None`（仅当根目录没匹配到任何 spec 时下探一层）。维护者 martindurant 自己开的 issue 希望能指定精确的下探深度（int）。代码里也有两处 TODO 注释（`__init__` 的 `walk` 参数和 `resolve()` 的子目录循环）提到“allow int for walk”。Issue 里另外提到的 “用 fsspec 的 depth-first walk 提前跳过忽略目录” 只是 *possible addition*，本 PR 不做（在 PR 描述里说明）。

## 合理性判断

- Issue 由维护者本人提出并标 `good first issue`，代码中有对应 TODO → 需求明确、在范围内。
- 仓库有 `AGENTS.md`（面向 AI coding agent 的架构说明），CONTRIBUTING 未禁止 AI；没有 AI 禁令。
- 外部 PR 有被合并（freakboy3742 #30、ktaletsk #35/#58/#72、jezdez #91、mcg1969 #96，2026-01~05）。

## 改动

- `src/projspec/proj/base.py`
  - `Project.__init__` / `Project.resolve` 的 `walk` 类型改为 `bool | int | None`，docstring 说明 int 语义；删除两处已实现的 TODO。
  - 新增小工具函数 `_child_walk(walk)`：`True`→`True`（无限），`None`/`False`→`False`（与原来 `walk or False` 行为一致），int→`walk - 1`（剩余深度预算）。注意 `bool` 是 `int` 子类，先判 bool。
  - `resolve()` 开头校验：负数 / 非整数（如 `1.5`、`"2"`）抛 `ValueError`。
- `src/projspec/utils.py`：`scan_glob(walk=...)` 类型注解与文档同步（直接透传给 `Project`）。
- `docs/source/intro.rst`：补一句 `walk=2` 的用法。
- `tests/test_basic.py`：新增 `test_walk_depth`（参数化 None/False/0/1/2/3/10/True）、`test_walk_depth_counts_directories_without_specs`（中间无 spec 的目录也占一层，子项目键为 `empty/a`）、`test_walk_invalid`（-1/1.5/"2"）。
- 未改 CLI（`--walk` 仍是 flag），留给维护者决定是否加 `--depth`。

## 验证

环境：`uv venv -p 3.11` + `uv pip install -e ".[test]"`（与 CI `pip install -e .[test]` 相同 extras），venv 的 `bin` 放进 `PATH`（部分测试会 `python -m django startproject` 等子进程）。

| 命令 | 结果 |
|---|---|
| 基线（未改）`pytest -q` | 580 passed, 16 skipped |
| 仅回退 `src/`、保留新测试：`pytest -q tests/test_basic.py -k walk` | **6 failed**, 7 passed（walk=1/2 深度错误、无 spec 中间层、3 个非法值未抛错）→ red |
| 打补丁后 `pytest -q tests/test_basic.py -k walk` | 13 passed → green |
| 打补丁后全量 `pytest -q`（CI 用 `pytest -v --cov projspec`） | 592 passed, 16 skipped |
| `pre-commit run --files <changed files>`（CI lint job 的 hooks：black 23.11、absolufy-imports、yesqa、blacken-docs、whitespace 等） | all Passed |

## 如何提交

```bash
git clone https://github.com/fsspec/projspec && cd projspec
git checkout -b walk-depth origin/main
git am /path/to/0001-Allow-walk-to-take-an-integer-depth.patch
git push <your-fork> walk-depth   # PR 目标分支: main
```

### 需要提交者注意
- 仓库无 DCO / changelog 要求；无 PR 模板。提交信息风格为普通英文句子（非 Conventional Commits）。
- 仓库对 AI 无禁令（有 AGENTS.md 指导 agent），PR 描述中已包含 Claude Code 披露段落。
- 这是 Feature 类 issue（非 bug）；设计选择（int 语义、非法值抛 ValueError、未改 CLI）已写在 PR 描述里方便维护者调整。

## PR title

Allow `walk` to take an integer depth

## PR body

```markdown
## Description

`Project(walk=...)` (and `Project.resolve(walk=...)`) now also accepts a non-negative integer,
giving the maximum number of directory levels to descend below the root, as proposed in #69:

- `walk=True` – walk the whole tree (unchanged)
- `walk=False` / `walk=0` – never descend (unchanged for `False`)
- `walk=None` (default) – descend one level only if the root matched no spec (unchanged)
- `walk=N` – descend at most `N` levels; each child is scanned with `N - 1`

Because `bool` is a subclass of `int`, booleans are handled first. Negative or non-integer values
raise `ValueError` early in `resolve()`. The two TODO comments about an integer walk are removed,
`scan_glob`'s type hint/docstring is updated (it passes `walk` straight through), and the intro docs
mention `walk=2`. A directory without any spec still counts as one level (its matches show up as
`"dir/sub"` children as before).

I did not change the CLI (`--walk` is still a flag) or switch to fsspec's depth-first walk for early
pruning (the "possible addition" in the issue) — happy to follow up on either if wanted.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #69

## Checklist

- [x] Tests pass locally (`pip install -e .[test]`, `pytest -q`: 592 passed, 16 skipped; the 12 new tests in `tests/test_basic.py` (`-k walk`) fail on `main` without the change for the integer/invalid cases; `pre-commit run` on the changed files passes)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (the repo has no changelog)
- [x] Documentation is updated (if applicable) — docstrings of `Project`, `Project.resolve`, `scan_glob`, and `docs/source/intro.rst`
```
