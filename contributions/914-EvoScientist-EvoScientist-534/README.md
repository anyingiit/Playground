# EvoScientist/EvoScientist#534 — langgraph dev keeps running after Ctrl+C during startup

| 项 | 值 |
|---|---|
| Issue | https://github.com/EvoScientist/EvoScientist/issues/534 |
| Tier | 新锐 |
| Labels | bug, good first issue |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01：issue 无 assignee、无评论、无 linked PR；PR 列表搜索 `534` 只命中无关的 #504/#259/#242/#190（均已合并、未涉及此问题） |
| Base | `main` @ 9ef018e |

## 问题理解
`start_langgraph_dev()`（`EvoScientist/langgraph_dev/manager.py`）用 `start_new_session=True` 启动 langgraph dev，终端 Ctrl+C 只发给 CLI。调用方的 atexit/信号清理在启动返回后才注册，而健康等待循环自身没有对 `KeyboardInterrupt` 的清理，于是启动阶段按 Ctrl+C 会留下孤儿服务器、PID 文件和 workspace sidecar，导致下次 deploy 端口冲突、serve 复用孤儿进程等。

## 合理性判断
维护者自己标了 bug + good first issue，并给出了修复建议（`try...except BaseException` + `stop_langgraph_dev(proc)`）。代码中确认问题存在，最新 main 未修复。CONTRIBUTING 要求 PR 针对 issue 中的 bug，符合。

## 改动
- `manager.py`：Popen 之后的 PID/sidecar 写入、全局状态赋值和健康等待整体包进 `try/except BaseException: stop_langgraph_dev(proc); raise`。原有“立即退出”“60 秒不健康”两条路径改为直接 raise，由同一个 except 清理（错误信息不变）。
- `tests/test_langgraph_manager.py`：新增 `TestStartLanggraphDevInterruptedStartup`（2 个测试）。

## 验证
```
uv sync --dev                     # .venv 288M，验证后已删除
.venv/bin/pytest tests/test_langgraph_manager.py -k Interrupted
  # 修复前：1 failed (test_keyboard_interrupt_during_health_wait_stops_server: assert [] == [424242]), 1 passed   ← red
  # 修复后：2 passed                                                                                              ← green
.venv/bin/ruff check .            # All checks passed!
.venv/bin/ruff format --check .   # 459 files already formatted
.venv/bin/pytest --timeout=30     # 4223 passed, 27 skipped（与 CI 相同命令；未装 all-channels extra，相关测试可能 skip）
```

## 需要提交者注意
- 仓库无 AI 贡献限制（CONTRIBUTING.md / .github 中未发现）；PR 正文已含披露段落。
- 无 DCO / Signed-off-by 要求，无 CHANGELOG。
- PR 模板（Description / Type of change / Checklist）已合并进 pr_body.md。
- 提交者邮箱为 `49945850+anyingiit@users.noreply.github.com`。

## 如何提交
```bash
git clone https://github.com/anyingiit/EvoScientist && cd EvoScientist   # 先 fork
git remote add upstream https://github.com/EvoScientist/EvoScientist && git fetch upstream
git checkout -b fix/langgraph-dev-startup-interrupt upstream/main
git am /path/to/0001-Stop-half-started-langgraph-dev-when-startup-is-inte.patch
git push origin fix/langgraph-dev-startup-interrupt
gh pr create --repo EvoScientist/EvoScientist --head anyingiit:fix/langgraph-dev-startup-interrupt \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
见 `pr_title.txt`：Stop half-started langgraph dev when startup is interrupted (#534)

## PR body
见 `pr_body.md`。
