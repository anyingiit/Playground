# MakazhanAlpamys/Soup #1221

| 项 | 值 |
|---|---|
| Issue | https://github.com/MakazhanAlpamys/Soup/issues/1221 — `soup data forge --judge-provider` writes an empty-answer row for every failed judge call and still reports "synth complete" |
| Tier | 高活跃高Star |
| Labels | bug, help wanted |
| Status | ✅ ready — patch + PR text done (base `main` @ 1826a2b) |
| Duplicate-PR check | `1221 repo:MakazhanAlpamys/Soup` → 0 PRs; `forge judge empty answer … is:open` → 0; newest open PR is #1202 (none touch forge); issue has 0 comments, unassigned (checked 2026-09-24) |
| Audit | clean — see `AUDIT.md` |
| Patch | `0001-fix-data-soup-data-forge-stops-writing-empty-answer-.patch` (single commit, `git apply --check` OK on main @ 1826a2b) |

## 问题理解

`make_judge_provider_fn` 在默认 `raise_on_error=False` 时，任何传输/HTTP/解析失败都返回 `{"text": ""}`。
`soup data forge` 构造 judge 时没有传 `raise_on_error=True`。`synthesise_forge_rows` 用
`score_uncertainty` 给空回复打分 → 1.0（最大），而剪枝条件是 `score < threshold` 且 threshold ≤ 1.0，
所以任何阈值都剪不掉。结果：每个失败调用产生一行空 assistant 回答，绿色 "synth complete" 面板，exit 0。
用这个文件训练会教模型"什么都不回答"。

Issue 验收标准：
- CliRunner 对 `127.0.0.1:9`：无空回答行、非零退出、消息里有 provider 和失败原因；在 main 上失败。
- 本地 stub server 变体：HTTP 404/429/500、200 空内容、200 畸形 JSON、每隔一次失败（只写成功行并报告失败数）。
- 空回复在 `--uncertainty-threshold` 0.0 和 1.0 都被剪掉。
- ollama / vllm / anthropic（mock transport）行为一致。
- CLI 输出用 ANSI-strip + 空白折叠 helper 断言。

## 合理性判断

合理。维护者本人按项目模板写的 bug，给了明确的 fix path，并指向已经合并的同类修复 #969
（`soup data recipe` 已改为 `raise_on_error=True` + 失败计数）。main @ 1826a2b 上代码与 issue 描述一致
（`commands/data_forge.py` 构造 judge 未传 `raise_on_error`）。无 PR、无认领。

## 改动

- `src/soup_cli/utils/data_forge.py`
  - 新增 `ForgeJudgeStats` dataclass（`calls` / `failures` / `first_error`，`record_failure()` 截断到 200 字符），导出到 `__all__`。
  - `synthesise_forge_rows(..., stats=None)`：每次调用计数；judge 抛异常（含 `ProviderCallError`，描述带 `__cause__`，如 `ollama provider request failed (ConnectError: [Errno 111] Connection refused)`）、返回非 Mapping、非字符串 text、空/纯空白 text → 记为失败、不生成行，**与阈值无关**。`stats` 类型错误抛 `TypeError`。签名向后兼容（关键字参数可选）。
- `src/soup_cli/commands/data_forge.py`
  - live judge 用 `raise_on_error=True` 构造。
  - 有失败时拼出 `N of M judge calls failed for --judge-provider <p> (<endpoint>); first error: <...>`（endpoint 复用 `recipe_run._provider_endpoint_label`，不含凭据/路径）。
  - 0 行且有失败 → 红色 `No usable rows produced: ...`，exit 1，不写 dataset/provenance。
  - 部分失败 → 写成功行，面板标题改成黄色 `Data Forge — synth complete with judge failures`，多一行 `Judge calls: N of M failed`，面板后打印黄色 Warning 行。
  - 无失败时输出完全不变（离线 stub 路径不变）。
- `docs/data.md`：把 "Per-call judge exceptions logged at DEBUG." 改为描述新行为。
- `tests/test_issue1221_forge_judge_failures.py`：28 个测试（端口 9；ThreadingHTTPServer stub 的 404/429/500/空/畸形 × ollama/vllm；交替失败 × ollama/vllm；CLI 阈值 0.0/1.0；`synthesise_forge_rows` 单元测试 "" / 空白 / None × 阈值；raising judge 计数；anthropic mock 500/空/部分失败；健康 judge 和离线 stub 对照）。
- `changelog.d/0.75.1/PR_NUMBER.fixed.md`：**提交 PR 后需改名为 `<PR号>.fixed.md` 并把正文里的 `#PR_NUMBER` 替换为 PR 号**（`tests/test_issue487_changelog_fragments.py` 的文件名正则只接受数字，用占位名时该测试会失败；临时改名为 `9999.fixed.md` 验证过 21/21 通过）。

## 验证

环境：Python 3.11 venv，`pip install --no-cache-dir -e ".[dev]"`（在 /home/user/work/Soup-1221/.venv，已删除）。

| 命令 | 结果 |
|---|---|
| `pytest tests/test_issue1221_forge_judge_failures.py -o addopts="" --no-cov -p no:cacheprovider -q`（**无修复**，stash src+docs） | **25 failed, 3 passed**（通过的 3 个是对照：健康 judge、离线 stub、stats 类型检查） |
| 同上（**有修复**） | **28 passed** |
| `ruff check src/soup_cli/ scripts/ tests/ benchmarks/` | All checks passed! |
| `pytest tests/test_v0470_part_a.py tests/test_v0537.py tests/test_issue817_recipe_provider.py tests/test_issue813_gate_exit_codes.py tests/test_v0716.py tests/test_v07113.py tests/test_v0715.py tests/test_v0403_part_c.py tests/test_issue979_documented_cli_flags_exist.py tests/test_issue1221_forge_judge_failures.py -o addopts="" --no-cov -p no:cacheprovider -q` | 658 passed, 5 skipped |
| `pytest tests/test_issue823_stale_feature_descriptions.py tests/test_issue459_interleave_streaming_hub.py …`（引用 docs/data.md 的测试） | 37 passed |
| `pytest tests/test_issue487_changelog_fragments.py …` | 占位名 `PR_NUMBER.fixed.md`：1 failed（预期，文件名需为数字）；临时改为 `9999.fixed.md`：21 passed |
| Issue 原始复现（端口 9） | 修复后：`No usable rows produced: 2 of 2 judge calls failed for --judge-provider ollama (http://127.0.0.1:9); first error: ollama provider request failed (ConnectError: [Errno 111] Connection refused)`，exit=1，未生成任何文件 |

未运行：完整测试套件（机器共享、另一个长测试在跑）；GPU/smoke 测试与本改动无关。

## 如何提交

```bash
git clone https://github.com/<you>/Soup && cd Soup
git checkout -b fix/issue-1221-forge-judge-failures origin/main
git am /path/to/0001-fix-data-soup-data-forge-stops-writing-empty-answer-.patch
# 开 PR 拿到编号 N 后：
git mv changelog.d/0.75.1/PR_NUMBER.fixed.md changelog.d/0.75.1/N.fixed.md
sed -i 's/#PR_NUMBER/#N/' changelog.d/0.75.1/N.fixed.md
git commit --amend --no-edit && git push -f
```
Base branch: `main`。Conventional Commits 已遵守；仓库不要求 DCO。若发布了新版本（CHANGELOG 出现比 0.75.1 更新的标题），需把 fragment 移到新版本目录。

## PR title

```
fix(data): soup data forge stops writing empty-answer rows for failed judge calls (#1221)
```

## PR body

```markdown
## Description

`soup data forge --judge-provider` built its judge without `raise_on_error`, so every transport, HTTP or parse failure came back from `make_judge_provider_fn` as `{"text": ""}`. `synthesise_forge_rows` then scored that empty reply with `score_uncertainty`, which returns the maximum 1.0 when either side is empty, and the prune test is `score < threshold` with the threshold capped at 1.0, so no `--uncertainty-threshold` could remove it. The command wrote one empty-assistant row per failed call, printed the green "synth complete" panel and exited 0.

This follows the fix path in the issue and the #969 precedent for `soup data recipe`:

- The forge judge is built with `raise_on_error=True`.
- `synthesise_forge_rows` takes an optional `stats: ForgeJudgeStats` (keyword-only, backwards compatible). It counts judge calls. A call that raises (including `ProviderCallError`; the description keeps the cause, e.g. `ollama provider request failed (ConnectError: [Errno 111] Connection refused)`), returns a non-mapping or non-string reply, or returns empty/whitespace-only text is recorded as a failure and never becomes a row, whatever the threshold. An empty answer is no answer, not a "maximally uncertain" one.
- The CLI builds `N of M judge calls failed for --judge-provider <p> (<endpoint>); first error: <...>`. The endpoint label reuses `recipe_run._provider_endpoint_label`, so it carries no credentials, path or query.
  - **No usable row:** red `No usable rows produced: …`, exit 1, and no dataset or provenance file is written.
  - **Partial outage:** the successful rows are written. The panel title becomes a yellow `Data Forge — synth complete with judge failures` and shows `Judge calls: N of M failed`, followed by a warning line with the first error.
  - **No failures:** the output is unchanged, and so is the offline stub path.
- `docs/data.md`: replaced "Per-call judge exceptions logged at DEBUG." with the new behaviour.

Tests (`tests/test_issue1221_forge_judge_failures.py`, 28 cases). All CLI output is checked after an ANSI-strip and whitespace-collapse helper (`tests.conftest.strip_ansi`).
- **Unreachable judge:** CliRunner against `127.0.0.1:9`. Asserts no rows or files, a non-zero exit, and that the provider, endpoint and failure are named.
- **Failing stub server:** a local `ThreadingHTTPServer` stub returning HTTP 404 / 429 / 500, 200 with empty content, or 200 with malformed JSON, each for both `ollama` and `vllm`. Every case exits 1 with `6 of 6 judge calls failed` and the matching first error.
- **Partial failure:** every second call fails, for `ollama` and `vllm`. Only the 3 successful rows are written and `3 of 6` is reported.
- **Empty replies:** pruned at `--uncertainty-threshold` 0.0 and 1.0, both through the CLI and in unit tests of `synthesise_forge_rows` (`""`, whitespace, `None`).
- **Anthropic:** `httpx.post` is mocked for HTTP 500, empty text and a partial outage.
- **Controls:** a healthy judge still writes 6 rows under the green panel, and the offline stub is unchanged.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #1221

## Checklist

- [x] Tests pass locally
  - `pytest tests/test_issue1221_forge_judge_failures.py -o addopts="" --no-cov -p no:cacheprovider`: 28 passed. On `main` without the fix: 25 failed and 3 passed; the 3 that pass are the healthy, offline and type-check controls.
  - Related suites: `tests/test_v0470_part_a.py tests/test_v0537.py tests/test_issue817_recipe_provider.py tests/test_issue813_gate_exit_codes.py tests/test_v0716.py tests/test_v07113.py tests/test_v0715.py tests/test_v0403_part_c.py tests/test_issue979_documented_cli_flags_exist.py`, together with the new file, gave 658 passed and 5 skipped.
  - The docs-referencing tests (`test_issue823_…`, `test_issue459_…`) gave 37 passed, and `tests/test_issue487_changelog_fragments.py` gave 21 passed.
  - `ruff check src/soup_cli/ scripts/ tests/ benchmarks/` is clean.
- [x] `CHANGELOG.md` is updated (if applicable) — via the fragment `changelog.d/0.75.1/<this PR>.fixed.md`
- [x] Documentation is updated (if applicable) — `docs/data.md` Data Forge section
```
