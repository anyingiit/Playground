# mloda-ai/mloda-registry#742 — Exclude .claude/worktrees from the bandit scan

| Item | Value |
|---|---|
| Issue | https://github.com/mloda-ai/mloda-registry/issues/742 |
| Tier | 新锐 |
| Labels | `bug`, `good first issue`, `help wanted` |
| Status | ✅ 实现 + before/after bandit 复现 + 全量 `tox` 通过；PR 文本已写好 |
| Duplicate-PR check | `742 repo:mloda-ai/mloda-registry` → 0 PR；`bandit worktrees repo:mloda-ai/mloda-registry` → 0 PR；最近 bandit 相关 PR 列表中无相关项；issue 0 评论、无 assignee（2026-09-24 查询，issue 当天由维护者 TKaltofen 创建） |
| Base | `main` @ `0bdee17` |

## 问题理解
bandit 不读取 `.gitignore` / git exclude。当 Claude Code 在 `.claude/worktrees/<name>/` 下放一个 git worktree 时，
`tox` 的 bandit 步骤（`bandit -c pyproject.toml -r -q -x <anchored globs> .`）会把 worktree 中那份仓库副本也扫一遍，
报出副本里的问题，导致本地 `tox` 失败。维护者给出的步骤：在 `tox.ini` 的 `-x` 列表与根 `pyproject.toml`
`[tool.bandit] exclude_dirs` 中都加上 `.claude/worktrees/*` 与 `*/.claude/worktrees/*`（沿用已有的 anchored-glob 风格），
PR 标题用 `chore:`。

注：issue 里举例的 `scripts/verify_builds.py` B404/B603/B607 在当前 `main` 的 worktree 副本里已不再触发
（该文件现在有 `# nosec`，#375 之后修复），所以复现时我在 worktree 里放了一个一次性的 bandit 阳性文件
（不提交）来模拟“worktree 中存在尚未修好的代码”这一一般情形。

## 合理性判断
维护者本人提出，issue 已给出明确方案与验收标准；`tox.ini` 注释与 `pyproject.toml` 注释都说明两处排除列表需使用
anchored globs，改动完全符合现有约定。根 `pyproject.toml` 的 `[tool.bandit]` 为手工维护（生成器只改 workspace
members 与 `mloda` 依赖，见 `docs/packaging.md`），已用 `scripts/generate_pyproject.py --check` 验证无漂移。

## 改动（2 文件，+4/-2）
- `tox.ini`：bandit `-x` 列表末尾追加 `,.claude/worktrees/*,*/.claude/worktrees/*`
- `pyproject.toml`：`[tool.bandit] exclude_dirs` 追加 `".claude/worktrees/*"`, `"*/.claude/worktrees/*"`

## 验证
环境：fresh `git clone --depth 1`；tox 4.64.1 + tox-uv + uv 0.12.18（与 CI 固定的 `uv>=0.12,<0.13` 一致）；
`tox -e python310`（注意：本机该 env 实际使用 Python 3.11 解释器，因 `python310` 不是 tox 识别的版本因子）。
复现准备：`git worktree add --detach .claude/worktrees/probe HEAD`，并在其中放入一次性文件
`throwaway_probe.py`（`import subprocess; subprocess.call("ls", shell=True)`）。

| 场景 | 命令 | 结果 |
|---|---|---|
| RED：tox 的 bandit 命令（旧 `-x`，旧 pyproject） | `bandit -c pyproject.toml -r -q -x <旧列表> .` | exit 1，B404/B607/B602 × `./.claude/worktrees/probe/throwaway_probe.py` |
| RED：直接 `bandit -c pyproject.toml -r -q .`（旧 pyproject） | 同左 | exit 1，同样 3 个问题 |
| GREEN：仅 tox.ini 改动（新 `-x` + 旧 pyproject） | | exit 0 |
| GREEN：仅 pyproject 改动（直接 bandit，默认排除） | `bandit -c pyproject.toml -r -q .` | exit 0 |
| GREEN：两者都改 | tox 命令 | exit 0 |
| 负向对照：`.claude/probe_outside.py`、`tmp_worktrees_probe/worktrees_probe.py` | tox 命令 / 直接 bandit | 两个文件都仍被报告（exit 1）→ `.claude/worktrees/` 之外不被排除 |
| 无 worktree 时扫描范围对比（JSON 输出） | 旧配置 vs 新配置 | 均为 565 文件、60841 LOC、0 issue，文件集合完全相同 |
| **验收：全量 `tox -e python310`（worktree + 阳性文件仍在）** | `tox -e python310` | pytest **7945 passed, 340 skipped, 1 xfailed**；ruff format（1301 files already formatted）✅；ruff check ✅；`mypy --strict` 565 files no issues ✅；bandit ✅；`congratulations :)` |
| check-generated | `python scripts/generate_pyproject.py --check` | ✅ 35 个 pyproject 均最新，workspace / root 依赖无漂移 |

复现用的 worktree 与阳性文件验证后已删除，未提交。

## 规范
- Conventional Commits：`chore: exclude .claude/worktrees from the bandit scan`（issue 指定 `chore:`；commit-lint 正则通过）
- AGENTS.md/CLAUDE.md：禁止 `Co-Authored-By` 等署名行 → commit 中无任何署名；不需要 DCO / Signed-off-by
- 无 CHANGELOG（semantic-release 自动生成）；无文档改动需要（AGENTS.md 对 bandit 的描述为“显式 -x anchored globs 列表”，仍准确）
- 仓库 PR 模板有 Summary / Type of change / Checklist，已合并进下方 PR body

## 如何提交
```bash
git clone https://github.com/<you>/mloda-registry && cd mloda-registry
git checkout -b chore/bandit-exclude-claude-worktrees origin/main
git am /path/to/0001-chore-exclude-.claude-worktrees-from-the-bandit-scan.patch
uv run tox          # 可选复核
git push -u origin HEAD   # base: main；PR 标题必须是 Conventional Commit（chore:）
```

### PR — chefs-pick-oss-starter 格式（融合仓库模板）
**Title:** `chore: exclude .claude/worktrees from the bandit scan`

```markdown
## Description

bandit does not read `.gitignore` or git's exclude file, so a Claude Code git worktree checked out under
`.claude/worktrees/` is scanned as a second copy of the repository, and anything bandit flags in that copy
fails the local `tox` gate. This adds `.claude/worktrees/*` and `*/.claude/worktrees/*` to both exclusion
lists, in the existing anchored-glob style:

- `tox.ini`: the bandit `-x` list
- `pyproject.toml`: `[tool.bandit] exclude_dirs`, so a direct `bandit -c pyproject.toml -r .` behaves the same

No other paths are affected.

**Type of change:** Refactor / maintenance (`chore:`)

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #742

## Checklist

- [x] Tests pass locally
  - Setup: `git worktree add --detach .claude/worktrees/probe HEAD`, plus a throwaway file in it that bandit
    flags (`subprocess.call("ls", shell=True)`, not committed). On current `main` the worktree's
    `scripts/verify_builds.py` already carries `# nosec`, so the throwaway file stands in for unfinished work.
  - Before: tox's bandit command and a direct `bandit -c pyproject.toml -r -q .` both exit 1 with
    B404/B602/B607 in `./.claude/worktrees/probe/throwaway_probe.py`.
  - After: both exit 0. Each of the two edits works on its own (new `-x` with the old `pyproject.toml`, and the
    new `pyproject.toml` with bandit's default excludes).
  - Negative control: the same file placed at `.claude/probe_outside.py` and at `tmp_worktrees_probe/worktrees_probe.py`
    is still reported. With no worktree present, the scanned set is identical before and after (565 files, 60,841 LOC).
  - `uv run tox` with the worktree still in place: 7945 passed, 340 skipped, 1 xfailed; ruff format, ruff check,
    `mypy --strict` and bandit all clean.
  - `python scripts/generate_pyproject.py --check`: all up to date (the root `[tool.bandit]` table is hand-maintained).
- [ ] Tests added or updated — n/a (tooling config only; behaviour verified manually as above)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, generated by semantic-release
- [ ] Documentation is updated (if applicable) — n/a
- [x] `pyproject.toml` not edited by hand where generated — only the root `[tool.bandit]` table, which the generator doesn't manage
- [x] PR title follows Conventional Commits
```
