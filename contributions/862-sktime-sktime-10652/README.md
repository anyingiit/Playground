# sktime/sktime#10652 — Task 1 slice: `SupervisedIntervals` 无条件第二组测试参数，移除测试跳过

| 项 | 值 |
|---|---|
| Issue | https://github.com/sktime/sktime/issues/10652 |
| Tier | 高星 |
| Labels | enhancement, good first issue, module:base-framework |
| Status | ✅ ready — 独立复核通过（修正了“无需 numba 即可构造”的措辞：估计器本身依赖 numba，新参数组只是不用 numba 特征函数）；未提交。**需先在 issue 下发 scope 评论（见下）** |
| Base | `main` @ 80ea2ef (2026-09-27, "[ENH] dedicated namespace hook in registry (#11316)") |
| Duplicate-PR check (2026-10-01) | issue open、未指派、页面无评论；`pulls?q=10652` 只有 #11335 (DOBIN, open)、#11218 (SameLocSplitter, open)、#10663/#11193/#11221 (task 2, merged)。`pulls?q=SupervisedIntervals` 只有已合并的 #11205（doctest）等旧 PR，无 open PR 涉及该类。其他 open 的 "second test parameter set" PR（#11067 FittedParamExtractor/WeightedEnsemble/ClustererPipeline、#11023/#11058 param_est/pipeline、#10980 Shapelet/TEASER、#10839 BOSS/TDE/SFAFast、#11226 TDE/RISE、#10974 SlidingWindowSegmenter、#10756 RandomSamplesAugmenter、#10833/#11335 DOBIN、#9136 HIVECOTEV2 …）均不含 SupervisedIntervals。 |

## 问题理解

#10652（fkiraly 开）要求用 "AI + 人工逐个审查" 收尾 #3429：给仍缺少 ≥2 组 `get_test_params` 的估计器补参数，并移除对应 `test_get_test_params_coverage` 跳过（Task 1）；Task 2（跳过列表迁移成 tag）已合并；Task 3 删除旧钩子。issue 要求贡献者说明自己 PR 的 scope。

`SupervisedIntervals` 带 `"tests:skip_by_name": ["test_get_test_params_coverage"]`，并在 `sktime/tests/_config.py::EXCLUDE_SOFT_DEPS`（“只有装了软依赖才有 2 组参数”的估计器）中：它的 `get_test_params` 在没装 numba 时只返回一个 `{}`。

## 合理性判断

- 维护者自己开的 issue，明确欢迎 AI 辅助（要求人工审查每个估计器）；正是 #11067 等 PR 采用的“无条件第二组参数”模式。
- 仓库无 AGENTS.md/CLAUDE.md，没有 AI 禁令；PR/issue 模板里有隐藏注释要求 LLM 生成内容在开头标注 "LLM generated content, by (your model name)"（见“需要提交者注意”）。
- 选 SupervisedIntervals 的理由：只需 numba（轻量），不受 `tests:skip_all` 影响（RandomIntervalFeatureExtractor、HIVECOTEV1、M5Dataset、HCrystalBallAdapter 都是 skip_all，改了 CI 也不会跑），且无任何 open PR 覆盖。

### 先在 issue 下发的 scope 评论（提交者需先贴，再开 PR）

> I'd like to take a small task-1 slice: `SupervisedIntervals` - add a second `get_test_params` set that does not use `numba` feature functions (so `get_test_params` returns two sets even without `numba`), remove its `test_get_test_params_coverage` skip tag and its entry in `EXCLUDE_SOFT_DEPS`. As far as I can see this isn't covered by any open PR (#11335, #11218, #11067, #11023, ...). PR to follow shortly.

## 改动

- `sktime/transformations/supervised_intervals.py`
  - `get_test_params` 新增不使用 numba 特征函数的第二组（估计器本身仍依赖 numba，但无 numba 时 `get_test_params` 也能返回 ≥2 组）：`{"n_intervals": 2, "min_interval_length": 4, "randomised_split_point": False}`（默认 features）；原有两组 numba 特征函数参数在装了 numba 时追加（共 4 组）。始终返回 list。
  - 删除 `tests:skip_by_name: ["test_get_test_params_coverage"]`。
- `sktime/tests/_config.py`：从 `EXCLUDE_SOFT_DEPS` 删除 `"SupervisedIntervals"`（`test_test_utils.py` 的断言消息要求如此）。

## 验证

环境：`uv venv -p 3.11`，`uv pip install -e . pytest pytest-xdist pytest-timeout "numba<0.68" ruff==0.13.1`（numba 0.68 超出 pyproject 上限 <0.68，故钉住）。pytest 用 `-o addopts=""` 关掉 setup.cfg 里的 `--only_changed_modules True / --matrixdesign True / -n auto`，改 `-n 2`。

| 命令 | 结果 |
|---|---|
| 基线 `pytest -o addopts="" sktime/tests/test_all_estimators.py -k "SupervisedIntervals and test_get_test_params_coverage"` | 63178 deselected（该测试因 skip tag 根本不被收集） |
| 基线：模拟 numba 缺失（mock `skbase.utils.dependencies._check_soft_dependencies` 对 numba 返回 False），脚本复刻 coverage 测试断言（`len(params) > 1`） | **AssertionError**，只返回 `[{}]` → red |
| 改后同一脚本 | 2 组参数且都可构造，OK → green |
| 改后 `check_estimator(SupervisedIntervals, raise_exceptions=False)`（装 numba） | 224 tests 全 PASSED，含 `test_get_test_params_coverage[SupervisedIntervals]` |
| 复核（独立 reviewer，真实无 numba 环境：`uv pip install -e . pytest ruff==0.13.1`，未装 numba）：脚本 `p = SupervisedIntervals.get_test_params(); assert isinstance(p, list) and len(p) > 1` | main：返回 `{}` → **AssertionError**（red）；patch：`[{}, {n_intervals: 2, min_interval_length: 4, randomised_split_point: False}]` → OK（green） |
| 复核：再装 `numba<0.68` 后 `check_estimator(SupervisedIntervals, raise_exceptions=False)` | 224 tests 全 PASSED（37s），get_test_params 返回 4 组 |
| 改后 `pytest -o addopts="" -n 2 sktime/tests/tests/test_test_utils.py sktime/transformations/tests/test_intervals.py sktime/tests/test_all_estimators.py -k "SupervisedIntervals or test_excluded_tests_by_test or test_run_test_for_class or test_intervals"` | 191 passed, 1 skipped (6m53s) |
| `ruff format --check` + `ruff check`（0.13.1，与 pre-commit 一致）改动文件 | clean |

说明：`SupervisedIntervals` 的 `python_dependencies` 含 numba，无 numba 时无法构造估计器，因此无 numba 时 `check_estimator` 本身会报 ModuleNotFoundError；本改动的意义是让 `get_test_params`（不构造对象，如 `test_test_utils` 中的调用）在无 numba 时也返回 ≥2 组，从而可以移出 `EXCLUDE_SOFT_DEPS`。装了 numba 时，基线的 `get_test_params` 其实已返回 3 组（skip 实为多余）；真正的“red”只出现在无 numba 环境（`test_test_utils` / 文档构建等会在无 numba 时调用 `get_test_params`），所以 red 用 mock 复现。未跑全量测试套件（6 万+ 用例，单次收集约 7 分钟），CI 默认也只测改动模块。

## 如何提交

```bash
git clone https://github.com/sktime/sktime && cd sktime
git checkout -b supervised-intervals-test-params origin/main
git am /path/to/0001-ENH-unconditional-second-test-parameter-set-for-Supe.patch
git push <your-fork> supervised-intervals-test-params   # PR 目标分支: main
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。

### 需要提交者注意
- **先在 #10652 贴上面的 scope 评论**（issue 要求说明 scope），再开 PR。
- sktime PR 模板含隐藏注释：LLM 生成内容需在开头加 "LLM generated content, by (your model name)"。按 owner 规则不写模型名，pr_body.md 第一行写的是 "LLM generated content, by Claude Code (reviewed by a human before submission)"；请提交者确认自己确实审过改动，或按需调整此行。issue 要求人工逐个审查估计器改动——请自己看一遍新参数组是否合理。
- 无 DCO、无 changelog 片段（sktime 发布时由 PR 标题生成 changelog）。PR 标题需以 [ENH]/[MNT]/[DOC]/[BUG] 开头（已用 [ENH]）。
- 模板 checklist 的 “把自己加入 .all-contributorsrc” 未勾选、补丁未改该文件；如需要可自行加 `anyingiit`（badge: code）。
- 提交前再查一次 `pulls?q=SupervisedIntervals`，确认没有人新开同类 PR。
