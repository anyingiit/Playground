# MakazhanAlpamys/Soup#1224 — `--baseline registry://` uses the oldest score for each benchmark

| | |
|---|---|
| Issue | https://github.com/MakazhanAlpamys/Soup/issues/1224 |
| Tier | 高活跃 + 高 Star（Soup，~7.1k★，每天多次合并） |
| Labels | `help wanted`（bug） |
| Status | ✅ 实现 + 8 个新测试（修复前 7 个失败）+ 相关套件 333 passed + ruff 通过 |
| 重复 PR 检查 | 无引用 #1224 的 PR（2026-09-24 检查） |

## 问题理解
`ExperimentTracker.get_eval_results` 按 `created_at DESC` 返回（新→旧）。`resolve_baseline` 的 registry 分支用 dict 推导式，
同名 benchmark **后写覆盖前写**，于是留下的是**最旧**的分数；而 `_registry_provenance` 取的是**最新**一条带戳记录的 provenance。
分数和 provenance 来自不同的行：用户按警告重新测量后，警告消失但基线仍是旧分数。issue 中的例子：候选 0.38 对真实基线 0.45 是 −0.07 的回归，
却因为用了旧的 0.30 被判为 +0.08 通过。影响 `soup eval gate`、`soup ship`、训练中 eval gate、loop stages。

## 合理性判断
issue 由维护者本人撰写，附带可复现脚本、根因行号、修复路径和 6 条验收标准；本改动逐条对应。

## 改动
- `src/soup_cli/eval/gate.py`
  - `_newest_row_per_benchmark()`：每个 benchmark 只取第一行（即最新）。
  - `_row_provenance()`：从**同一行**读取 provenance（取代跨 benchmark 的 `_registry_provenance`）。
  - provenance 按 benchmark 检查；同类问题合并成一条警告，并在末尾列出受影响的 benchmark（`Affected benchmark(s): gsm8k.`）。
- `src/soup_cli/experiment/tracker.py`：`get_eval_results` 显式 tie-break `ORDER BY created_at DESC, rowid DESC`（与 `list_runs` 一致）。
- `docs/evaluation.md`：补一句 registry 基线的规则。
- `changelog.d/0.75.1/PR_NUMBER.fixed.md`：**提交 PR 后请把文件名和正文里的 `PR_NUMBER` 改成真实 PR 号**（仓库规则：用 PR 号命名）。
- `tests/test_issue1224_registry_baseline_newest_row.py`（8 个测试，覆盖全部验收标准）：
  重测后返回新分数且无警告 · "最新优先"而非"最好戳优先" · 两个 benchmark 只重测一个时只点名旧的 · 同类问题共用一条警告 ·
  最新行无戳仍警告 unknown provenance · 相同 `created_at` 结果确定 · tracker 层 tie-break · `run_gate` 层面 0.38 对 0.45 判为回归。

## 验证
| 命令 | 结果 |
|---|---|
| `pytest tests/test_issue1224_registry_baseline_newest_row.py -o addopts="" --no-cov` | 8 passed ✅ |
| 同上，但回退 `src/` 改动 | **7 failed, 1 passed**（红→绿成立） |
| `pytest tests/test_issue404_baseline_scorer_stamp.py tests/test_eval_gate.py tests/test_tracker.py tests/test_registry.py tests/test_ui.py tests/test_eval_platform.py` | 333 passed ✅ |
| `ruff check src/soup_cli/ scripts/ tests/ benchmarks/` | All checks passed ✅ |
| `pytest tests/test_issue487_changelog_fragments.py` | 用占位名 `PR_NUMBER.fixed.md` 时 **1 failed / 20 passed**（该测试要求片段名为数字 PR 号）；改成数字名后 **21 passed** ✅ —— 开 PR 后改名即可 |
| 全量 `pytest tests/ -o addopts="" -m "not smoke"`（无 GPU） | **24671 passed, 166 skipped, 3 failed**：① changelog 片段占位名（见上一行，改名后通过）；② `test_issue580_…real_venv_launcher` 与 ③ `test_v0714::…test_secrets_not_leaked_to_child` 在 `main` 上同样失败（本地环境相关），与本改动无关 |

## 如何提交
```bash
git clone https://github.com/<you>/Soup && cd Soup
git checkout -b fix/1224-registry-baseline-newest-row origin/main
git am /path/to/0001-fix-eval-use-the-newest-eval-row-per-benchmark-for-r.patch
# ⚠️ 开 PR 后必须：git mv changelog.d/0.75.1/PR_NUMBER.fixed.md changelog.d/0.75.1/<PR号>.fixed.md
#    并把正文里的 #PR_NUMBER 换成 #<PR号>，否则 tests/test_issue487_changelog_fragments.py 会失败
git push -u origin HEAD   # base: main
```
仓库惯例：认领 issue 时在 issue 下留言（"the comment is the claim"）。

### PR — chefs-pick-oss-starter 格式
**Title:** `fix(eval): use the newest eval row per benchmark for registry baselines`

```markdown
## Description

`resolve_baseline("registry://…")` built its score map with a dict comprehension over rows that
`ExperimentTracker.get_eval_results` returns newest first, so each benchmark kept its **oldest** score, while
the provenance warning came from the newest stamped row. Re-measuring a baseline — what the warning asks
for — silenced the warning but kept the stale score, so a candidate at 0.38 passed against a stale 0.30
instead of regressing against the re-measured 0.45.

- Pick one row per benchmark, the newest, and take **both** the score and the provenance from it.
- Check provenance per benchmark. Benchmarks with the same problem share one warning, which now ends with
  `Affected benchmark(s): …` so a partially re-measured baseline names what is still stale.
- `get_eval_results` orders by `created_at DESC, rowid DESC` (as `list_runs` already does), so identical
  timestamps resolve deterministically to the later insert.
- `docs/evaluation.md` states the rule; changelog fragment added under `changelog.d/0.75.1/`.

Tests (`tests/test_issue1224_registry_baseline_newest_row.py`) cover every acceptance item in the issue:
re-measured baseline is used and silent; newest wins even when its stamp is worse; only the stale benchmark
is named; unstamped newest row still warns; identical timestamps are deterministic (resolver and tracker);
and a `run_gate` check that 0.38 regresses against a re-measured 0.45.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1224

## Checklist

- [x] Tests pass locally — new file: 8 passed (7 of them fail without the fix); `test_issue404_baseline_scorer_stamp`,
      `test_eval_gate`, `test_tracker`, `test_registry`, `test_ui`, `test_eval_platform`: 333 passed;
      `ruff check src/soup_cli/ scripts/ tests/ benchmarks/` clean; full suite 24671 passed — the only other failures
      (`test_issue580_…real_venv_launcher`, `test_v0714::…secrets_not_leaked_to_child`) fail identically on `main` here
- [x] `CHANGELOG.md` is updated (if applicable) — via `changelog.d/0.75.1/<this PR>.fixed.md`
      (`test_issue487_changelog_fragments.py` passes once the fragment carries this PR's number)
- [x] Documentation is updated (if applicable) — `docs/evaluation.md`
```
