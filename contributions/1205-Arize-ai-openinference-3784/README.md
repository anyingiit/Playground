# Arize-ai/openinference#3784 — Cohere instrumentation never ends the LLM span for an abandoned chat_stream

| 项 | 值 |
|---|---|
| Issue | https://github.com/Arize-ai/openinference/issues/3784 |
| Tier | 自由 |
| Labels | good first issue |
| Status | ✅ ready — 独立复核通过；提交前先在 issue 下征得维护者确认（见“需要提交者注意”第 1 条） |
| Base | `main` @ c7f15ec (2026-10-01, "chore: release main (#3915)") |
| Duplicate-PR check | 2026-10-01 23:25 UTC: issue OPEN, 0 comments, 无 assignee，无 linked PR。`pulls?q=3784` 只命中 #3796（feiiiiii5，**openai** 包的同类修复，不涉及 cohere）；`pulls?q=cohere` 与 open `stream` PR 列表中没有任何 cohere 流式/abandon 相关 PR。 |

## 问题理解

`_Stream`（`cohere/_stream.py`）是包住 `chat_stream` 迭代器的 `wrapt.ObjectProxy`，只在三种情况下结束 span：迭代耗尽（StopIteration）、迭代抛错、context manager `__exit__`。调用方如果：
- 创建 stream 后从不迭代就丢弃；
- 迭代一部分后 `break` 丢弃；
- 显式 `close()` / `aclose()`（ObjectProxy 直接转发给底层 generator，不调用 `_finish`）；

span 永远不会 end，in-memory exporter 里一个 span 都没有，trace 中这次调用直接消失。issue 作者给出的修复方案：照搬同仓库 `openinference-instrumentation-ollama` 的 `_Stream`：加 `__del__`（try/except 包住 `self._finish(None)`）、加 `close()`/`aclose()` 覆盖、`_finish` 接受 `Optional[Status]`。issue 还提到 together 包有同样问题——本补丁**只修 cohere**，保持小而聚焦（CONTRIBUTING 明确要求小 PR、不要混合）。

## 合理性判断

- 明确的 bug（span 泄漏/丢失），且仓库内 ollama 包已有相同模式的先例，修复方向无争议；标签 `good first issue`。
- CONTRIBUTING 写明最可能接受 “Small, focused bug fixes / reliability fixes” —— 本补丁正是。
- AI 政策：仓库有 AGENTS.md / CLAUDE.md（面向 Claude Code 的指导），labels 里有 `good-agent-issue` / `agent-in-progress`（维护者自己用 Claude 工作流），CONTRIBUTING、.github、label 描述中**没有禁止 AI 贡献**的条款。
- 风险点见“需要提交者注意”第 1 条（CONTRIBUTING 要求等维护者确认）。

## 改动

- `python/instrumentation/openinference-instrumentation-cohere/src/openinference/instrumentation/cohere/_stream.py`
  - 新增 `close()`：调用底层 `close`（若有），`finally` 中 `self._finish(None)`。
  - 新增 `async aclose()`：同上（异步）。
  - 新增 `__del__`：`try: self._finish(None) except BaseException: pass`。
  - `_finish(self, status: Optional[trace_api.Status])`（`_WithSpan.finish_tracing` 本来就接受 None → span 状态保持 UNSET）。
  - docstring 同步更新。`_finish` 原本就通过 `with_span.is_finished` 幂等，所以正常耗尽后再 GC / 重复 close 不会产生第二个 span。
- `tests/.../cohere/test_instrumentor.py`：新增 4 个测试（`import gc`）：未迭代即丢弃、迭代一半丢弃（保留部分输出 "The sky is blue "）、`close()`（且二次 close + GC 不重复）、异步 `aclose()`。两处变量标注 `stream: Any`，因为 SDK 把返回值类型标成 `Iterator`/`AsyncIterator`（无 close/aclose），否则 mypy 报 attr-defined。

## 验证

环境：在 clone 的 `python/.venv`（uv, Python 3.12）里 `uv pip install -e openinference-semantic-conventions -e openinference-instrumentation -e instrumentation/openinference-instrumentation-cohere -r instrumentation/openinference-instrumentation-cohere/test-requirements.txt -r dev-requirements.txt`（等价于 tox `cohere` testenv 的安装；cohere==5.21.1，ruff 0.9.2，mypy 1.11.2）。在 `python/instrumentation/openinference-instrumentation-cohere` 目录下执行：

| 命令 | 结果 |
|---|---|
| 基线（未改）`pytest -q tests` | 45 passed |
| 仅回退 `_stream.py`、保留新测试：`pytest -q tests -k "abandoned or close"` | **4 failed**（全部因为没有 span 被导出）→ red |
| 打补丁后 `pytest -q tests -k "abandoned or close"` | 4 passed → green |
| 打补丁后全量 `pytest -q tests` / `pytest -n 4 tests`（CI: `pytest -n auto -x -ra .`） | 49 passed / 49 passed |
| `ruff format --diff` + `ruff check --no-fix`（CI 的 ruff 步骤） | clean / All checks passed |
| `mypy .`（CI 的 mypy 步骤） | Success: no issues found in 9 source files |

未运行：tox 本身、py310/py314 矩阵、`cohere-latest` 变体、其它包。改动不涉及版本相关 API，预计无差异。

## 需要提交者注意

1. **CONTRIBUTING 里有一句：“An open issue is not an invitation to submit a PR. Even if an issue is labeled or acknowledged, please wait for explicit confirmation from a maintainer before starting work on it.”** 稳妥做法：先在 issue 下留言询问能否提交（例如 “Happy to send a small PR mirroring the Ollama fix for Cohere — OK?”），得到维护者确认后再开 PR。issue 作者 feiiiiii5 也在做同类修复（#3796 for openai），提交前再查一下是否已有人开了 cohere PR。
2. 需要签 **CLA**（仓库根目录 `CLA.md`；首次 PR 时 CLA bot 会提示），不需要 DCO / Signed-off-by。
3. 提交信息/PR 标题用 Conventional Commits（AGENTS.md: “Follow conventional commit format for PR titles”），CHANGELOG 由 release-please 自动生成，无需手动改。
4. 仓库 PR 模板在 `python/pull_request_template.md`（Description / Resolves # / 3 个 checklist 项），已并入 pr_body.md。CONTRIBUTING 要求“影响 emitted spans 时附 trace 截图”——本补丁只是让原来丢失的 span 被导出（属性不变，状态 UNSET），PR 中已说明；维护者若要截图可用 Phoenix 本地跑 examples/chat.py 改成中途 break 来截。
5. 仓库对 AI 无禁令（有 CLAUDE.md/AGENTS.md），PR 描述已包含 Claude Code 披露段落。
6. pre-commit 钩子（ruff 等）未安装运行；已直接跑 CI 同版本的 ruff format/check 和 mypy。

## 如何提交

```bash
git clone https://github.com/Arize-ai/openinference && cd openinference
git checkout -b fix-cohere-abandoned-stream origin/main
git am /path/to/0001-fix-cohere-end-the-LLM-span-when-a-chat_stream-is-ab.patch
git push <your-fork> fix-cohere-abandoned-stream   # PR 目标分支: main
gh pr create --repo Arize-ai/openinference --base main --head anyingiit:fix-cohere-abandoned-stream \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

参考 clone（含提交）：`/home/user/work/openinference-3784`，分支 `fix-cohere-abandoned-stream`。

## PR title

fix(cohere): end the LLM span when a chat_stream is abandoned or closed early

## PR body

见 `pr_body.md`。

## 独立复核

复核时间 2026-10-01 23:40 UTC。

- Issue 仍为 OPEN，无 assignee、无评论、无关联 PR；PR 搜索 `cohere` 没有任何针对 cohere 流式/abandon 的 PR（#3796 是 openai 包的修复）。
- 补丁与同仓库 `openinference-instrumentation-ollama/_stream` 的 `close`/`aclose`/`__del__` 写法逐行一致；`_finish` 本身靠 `is_finished` 保证幂等，所以正常耗尽后再被 GC、或重复 close，都不会产生第二个 span。`__del__` 由 `try/except BaseException` 包住，即使 `__init__` 没跑完也不会在 GC 时抛错。issue 提出的三点（`__del__`、`close()`、`aclose()`）都已覆盖。together 包按 issue 的说法要另开 PR，这里不做。
- 原 venv 已被删除，按 README 中的命令重建（Python 3.12，cohere==5.21.1）。只把 `_stream.py` 回退到 main 版本时，4 个新测试**全部失败**；恢复补丁后 4 个全部通过，整个包 **49 passed**。`ruff format --diff`、`ruff check --no-fix`、`mypy .` 均无问题。唯一的 warning 是 cohere SDK 自带的 Pydantic 弃用警告，与本补丁无关。
- `0001-*.patch` 与 workdir 中的 HEAD（9b2335b）内容一致；作者是 anyingiit <49945850+anyingiit@users.noreply.github.com>；补丁里没有出现 AI 模型名。提交信息符合 Conventional Commits，并包含 `Closes #3784`。仓库的 CHANGELOG 由 release-please 生成，不需要手动修改。
- pr_title.txt、pr_body.md（英文，含 Motivation/disclosure 段落和 `Closes #3784`）、AUDIT.md 都在，内容一致。复核中没有修改任何东西。

Status: ✅ ready — 补丁正确且聚焦，已验证新测试在修复前失败、修复后通过；提交前请先在 issue 下征得维护者同意，并签署 CLA。
