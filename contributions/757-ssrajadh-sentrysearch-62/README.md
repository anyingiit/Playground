# ssrajadh/sentrysearch #62 — Add `stats --json` for scripting

| 项 | 值 |
|---|---|
| Issue | https://github.com/ssrajadh/sentrysearch/issues/62 |
| Tier | 新锐 |
| Labels | enhancement, good first issue |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复PR检查 | 2026-10-01：issue 是 open 状态，无人分配，也没有评论和关联 PR。用 `pulls?q=62`、`is:pr json`、`is:pr stats` 搜索都没有找到相关 PR。anyingiit 在这个仓库没有 PR。 |
| Base | `master` @ ab688137（2026-09-28） |

## 问题理解
issue 是维护者 ssrajadh 本人提的。现在的 `stats` 只有给人看的输出，`[missing]` 标记夹在路径里，脚本很难解析。issue 要求加 `--json`，输出一个 JSON 对象，包含 backend、model、total_chunks、unique_source_files、source_files、missing_files 六个键。

验收条件：
- `stats --json | jq .total_chunks` 能取到数值。
- 不加这个 flag 时输出不变。
- 空索引时 `--json` 也能正常输出。

## 合理性判断
- 维护者自己开的 issue，带 good first issue 标签，范围写得很清楚（cli.py 的 stats 和 tests/test_cli.py）。
- cli.py 里原本没有任何 `--json` 先例，所以按最简单的方式实现：`click.echo(json.dumps(..., indent=2))`，没有引入新依赖。
- 空索引时，`--json` 输出一个合法对象（total_chunks 0、两个空列表），而不是 "Index is empty" 提示，这样 jq 管道不会出错。`store.get_stats()` 在空索引时也会返回全部三个键（0、0、[]），所以 JSON 分支和原文本分支一样，直接用 `s["..."]` 取值。

## 改动
- `sentrysearch/cli.py`：
  - `stats` 新增 `--json` 选项（参数名 `as_json`，避免和 json 模块重名）。
  - `backend` 取 `store.get_backend()`；`model` 没有时输出 `null`。
  - `missing_files` 是 `source_files` 中 `os.path.exists` 返回 False 的那些，顺序保持不变。
  - 新增 `import json`。
- `tests/test_cli.py`：新增 3 个测试，另加 `import json`。
  - `test_stats_json_with_data`：用 tmp_path 造一个真实存在的文件和一个不存在的文件，断言完整的 JSON 对象。
  - `test_stats_json_empty`：mock 的 `get_stats()` 返回空索引的真实形状 `{"total_chunks": 0, "unique_source_files": 0, "source_files": []}`，`detect_index` 返回 `(None, None)`。
  - `test_stats_without_json_is_human_readable`：逐字锁定不带 flag 时的输出。
- `README.md` 和 `README.zh.md`：在"Managing the index / 管理索引"示例里加了 `sentrysearch stats --json | jq .total_chunks` 和键说明。CONTRIBUTING 要求新增用户可见的 flag 时更新 README。

## 验证（uv，Python 3.12）
- 环境：`uv sync --group test`
- Red（先只加测试，不改 cli.py）：`uv run pytest tests/test_cli.py -k stats -q`
  - 结果：2 failed, 3 passed。
  - 失败的是 `test_stats_json_with_data` 和 `test_stats_json_empty`，报错 `No such option: --json`。
  - 纯文本输出的那个测试在 base 上就通过，作用是防止原输出被改动。
- Green：`uv run pytest tests/test_cli.py -k stats -q`，5 passed。
- 全量（与 CI 同参数）：`uv run pytest --cov --cov-report=term-missing`，441 passed。
- 手动冒烟：`HOME=$(mktemp -d) uv run sentrysearch stats --json` 输出合法 JSON（backend gemini、model null、total_chunks 0、空列表）。同一环境下不加 flag 仍然输出 "Index is empty..."。
- 真实索引冒烟（复审时补做）：在临时 HOME 下用 `SentryStore(backend="local", model="qwen2b").add_chunks(...)` 写入两个 chunk（一个文件存在，一个不存在），然后 `sentrysearch stats --json | jq -c .` 输出 total_chunks 2、missing_files 只含不存在的那个、backend "local"、model "qwen2b"；不加 flag 的文本输出和原来一致（含 `[missing]`）。
- 在干净的 master worktree 上 `git apply --check` patch 通过。
- CI 没有 lint 步骤，所以没有跑额外的 lint。CI 的 macOS 和 Windows 矩阵本地没法跑。
  - 测试里路径都来自 tmp_path，或者是直接比较的字符串，不依赖路径分隔符。
  - 纯文本测试用的 `/a/video1.mp4` 是 mock 出来的字符串，`os.path.exists` 也被 patch 了，所以 Windows 上也成立。

## 复审记录（独立 reviewer，2026-10-01）
- 重新验证 red→green：把 cli.py 换回 base 后 `-k stats` 为 2 failed / 3 passed，恢复后 5 passed；全量 `uv run pytest --cov --cov-report=term-missing` 441 passed；patch 在干净 master worktree 上 `git apply --check` 通过；作者为 anyingiit，无 AI 模型名。
- 修正：去掉了 `.get(..., 默认值)` 防御写法（真实 `get_stats()` 总会返回三个键，原 README 的理由不成立），改为与文本分支一致的 `s["..."]`，diff 更小；空索引测试改用真实返回形状。pr_body 中的示例输出改成与 `indent=2` 实际输出一致。

## 需要提交者注意
- 仓库没有 AI 政策，不需要 DCO 或 CLA，也没有 PR 模板和 CHANGELOG。PR 正文按 CONTRIBUTING 的要求写了 what、why、测试方式和 cost/perf 影响。
- JSON 用 `indent=2` 美化输出。如果维护者更想要单行输出，把 `indent=2` 去掉即可，测试不受影响。
- 空索引时 backend 输出的是回退值 "gemini"，和原文本逻辑使用的 store 一致。
- 建议分支名：`feature/stats-json`（CONTRIBUTING 的建议格式）。

## 如何提交
```bash
git clone https://github.com/ssrajadh/sentrysearch && cd sentrysearch
git checkout -b feature/stats-json origin/master
git am /home/user/Playground/contributions/757-ssrajadh-sentrysearch-62/0001-feat-add-json-flag-to-stats-command.patch
uv sync --group test && uv run pytest
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/757-ssrajadh-sentrysearch-62 ssrajadh/sentrysearch master feature/stats-json contributions/757-ssrajadh-sentrysearch-62/pr_title.txt contributions/757-ssrajadh-sentrysearch-62/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
