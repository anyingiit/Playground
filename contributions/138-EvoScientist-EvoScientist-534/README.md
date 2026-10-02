# EvoScientist/EvoScientist#534 — langgraph dev keeps running after Ctrl+C during startup

| 项 | 值 |
|---|---|
| Issue | https://github.com/EvoScientist/EvoScientist/issues/534 |
| Tier | 新锐 |
| Labels | bug, good first issue |
| Status | ✅ ready（补丁、测试、PR 文本都已完成） |
| 重复 PR 检查 | 无（2026-10-01：issue 无 assignee、无评论、无 linked PR；open PR 列表和 "534" 搜索都没有相关 PR） |
| Base | `main` @ 9ef018e |
| Patch | `0001-fix-langgraph_dev-stop-the-server-when-startup-is-in.patch` |

## 问题理解
`start_langgraph_dev()`（`EvoScientist/langgraph_dev/manager.py`）用 `start_new_session=True`（Windows 上是 `CREATE_NEW_PROCESS_GROUP`）启动 `langgraph dev`，所以终端的 Ctrl+C 只会发到 CLI。调用方的清理（atexit / finally）要等函数返回后才注册。结果是：Popen 之后、`return proc` 之前（写 PID 文件和 sidecar、最长 60s 的健康检查轮询）一旦出现 KeyboardInterrupt，服务器就成了孤儿进程，PID 文件和 sidecar 也留在磁盘上，下次 deploy 会遇到端口冲突。

## 合理性判断
标签是 bug + good first issue，issue 自己给出了修复建议（try/except 里调用 `stop_langgraph_dev()`），和代码一致，合理。CONTRIBUTING、labels、PR 模板里都没有禁止或限制 AI 贡献的条款。

## 改动
- `manager.py`：把 spawn 之后的所有逻辑包进 `try: ... except BaseException: stop_langgraph_dev(proc); raise`。原来的 "exited immediately" 和 "60s 内不健康" 两条路径各自调用了 `stop_langgraph_dev(proc)`，现在交给统一的 handler，行为不变。diff 大部分是缩进变化。
- `tests/test_langgraph_manager.py`：新增 `TestStartLanggraphDevCleansUpOnInterrupt`（3 个测试：健康检查轮询时 Ctrl+C、写 sidecar 时异常、正常启动不会触发 stop）。

## 验证
环境：`uv sync --dev`（Python venv，约 290MB，已删除）
- red：只回退 `manager.py`，运行 `pytest tests/test_langgraph_manager.py -k CleansUpOnInterrupt`，结果 2 failed, 1 passed
- green：同一命令全部通过；`pytest tests/test_langgraph_manager.py` 70 passed
- `uv run ruff check .`：All checks passed；`uv run ruff format --check .`：459 files already formatted
- `uv run pytest --timeout=30`（和 CI 一样）：4224 passed, 27 skipped
- 注：初版测试用 spy 替换了 `stop_langgraph_dev`，导致 `manager._PROCESS` 残留，让 `tests/test_background_middleware.py::test_run_launches_valid_command` 在全量运行时失败。改成用 monkeypatch 还原 `_PROCESS*` 全局变量后，全量测试通过。

## 需要提交者注意
- 仓库没有 DCO 要求，也没有 CHANGELOG。
- 仓库没有 AI 贡献政策；PR body 里已经带了 disclosure 段落。
- PR 模板有 "Type of change" 和项目自己的 checklist，pr_body.md 已经合并进去。
- 维护者合并时会 squash，标题会变成 `... (#PR号)`，不需要处理。

## 如何提交
```bash
git clone https://github.com/anyingiit/EvoScientist.git && cd EvoScientist   # 先 fork
git remote add upstream https://github.com/EvoScientist/EvoScientist.git && git fetch upstream
git checkout -b fix/langgraph-dev-ctrl-c-startup upstream/main
git am /path/to/0001-fix-langgraph_dev-stop-the-server-when-startup-is-in.patch
uv sync --dev && uv run ruff check . && uv run pytest --timeout=30
git push origin fix/langgraph-dev-ctrl-c-startup
gh pr create --repo EvoScientist/EvoScientist --head anyingiit:fix/langgraph-dev-ctrl-c-startup \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
见 `pr_title.txt`：`fix(langgraph_dev): stop the server when startup is interrupted (#534)`

## PR body
见 `pr_body.md`。
