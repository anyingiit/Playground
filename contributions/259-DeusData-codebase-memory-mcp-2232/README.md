# DeusData/codebase-memory-mcp #2232 — /api/project-health 在表缺失时仍报 healthy

| 项 | 内容 |
|---|---|
| Status | ✅ ready — 补丁已生成，红→绿已验证，lint 已对比 base（2026-10-01） |
| Issue | https://github.com/DeusData/codebase-memory-mcp/issues/2232 |
| Tier | 新锐 |
| Labels | bug, priority/high, ux/behavior |
| Base | `main` @ 0f52d30c (2026-09-30) |
| 重复 PR 检查 | `/pulls?q=2232` 只搜到已合并的 #2065（修的是 store 计数函数和 MCP index_status，不涉及本 handler）和无关的 #924；issue 无 assignee、无评论 → 无重复 |

## 问题理解
`GET /api/project-health?name=X`（`src/ui/http_server.c` 的 `handle_project_health`）直接把 `cbm_store_count_nodes/edges` 的返回值写进 JSON。
#2065 之后这两个函数读失败时返回 `CBM_STORE_ERR`(-1)，所以 nodes/edges 表缺失或损坏的库会被报成 `{"status":"healthy","nodes":-1,"edges":-1,...}`。

## 合理性判断
这是明确的 bug（maintainer 已标 priority/high），修法与 MCP `index_status`（mcp.c ~6885）已有的规则一致：负数计数视为读失败。
`corrupt` + `reason` 是该 endpoint 已有的返回形态（打不开库时返回 `cannot open`），graph-ui 的 `StatsTab.tsx` 也已处理 `corrupt`，因此 API 形态不变、前端无需改动。
CONTRIBUTING 规定 bug fix 无需事先讨论；允许 AI 辅助，但需要披露，且每个 commit 都要有 DCO 签名。

## 改动
- `src/ui/http_server.c`：计数 < 0 时返回 `{"status":"corrupt","reason":"cannot read nodes|edges|nodes and edges"}`。用两个 bool 写，避免 cppcheck 报 knownConditionTrueFalse 误报（最初的三元写法会触发）。
- `tests/test_httpd.c`：新增 `ui_server_project_health_reports_unreadable_counts_issue2232`。表完好时应为 healthy；`DROP TABLE nodes/edges` 后应为 corrupt + reason，且不含 `healthy` 和 `-1`。
- 提交信息遵循 Conventional Commits：`fix(ui): ...`，带 `Fixes #2232` 和 DCO `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`。

## 验证（Ubuntu 24.04 x86_64，gcc，ASan/UBSan）
- 红：只加测试、不改源码，`make -f Makefile.cbm -j2 test-focused TEST_SUITES=httpd` → `FAIL tests/test_httpd.c:1470: strstr(resp, "healthy") is not NULL`。测试提前退出导致 fixture 未清理，因此还有 LeakSanitizer 报告。
- 绿：加上修复后同一命令 → `66 passed, 1 skipped`，rc=0。最终版本（bool 写法）已重跑确认。
- 测试输出中的 `src/mcp/mcp.c:3047:5: runtime error: null pointer passed as argument 1` 在红跑（无修复）中同样出现，是 base 已有问题，与本改动无关。
- clang-format：CI 用 clang-format-20（pip 的 20.1.8）。`tests/test_httpd.c` 干净；`src/ui/http_server.c` 在 base 上就有 11 处违规（56–716 行，Windows 相关代码等），本改动的 hunk 没有新增违规。**上游 main 的 lint-format 本身可能就会因此失败，与本 PR 无关。**
- cppcheck 2.13（apt 版，Makefile.cbm 的参数）：只对 `src/ui/http_server.c` 跑，修复前后结果完全相同。全仓跑太慢，且 2.13 在其他文件也有报告（与 CI 版本不同），已中止。
- `make -f Makefile.cbm lint-no-suppress` 通过。
- 未跑：全量 `scripts/test.sh`（ASan 全量构建 + 全部 suite，在共享 4 核上太慢）、clang-tidy。

## 需要提交者注意
- **DCO 必需**：补丁中已有 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`，与 commit author 一致。签名代表你本人对 DCO 1.1 的法律声明，请确认后再提交。
- AI 政策：允许 AI 辅助，但**必须披露**（pr_body 中已有 motivation/disclosure 段落）。不要在 commit 或 PR 中贴私有会话链接。项目没有强制 AI trailer，所以没有加。
- maintainer 要求 PR 中的结论可复查，pr_body 已写明命令和结果；若 reviewer 追问，用上面的命令回答即可。
- 若 CI 的 lint-format 因 http_server.c 的既有违规失败，说明这是 main 上本来就有的问题（可在 main 上复现）。

## 如何提交
```bash
git clone https://github.com/DeusData/codebase-memory-mcp.git && cd codebase-memory-mcp
git checkout -b fix/project-health-unreadable-counts origin/main
git am /path/to/0001-fix-ui-report-unreadable-counts-as-corrupt-in-api-pr.patch
make -f Makefile.cbm test-focused TEST_SUITES=httpd   # 可选：复查
# fork 后推送并开 PR：
tools/submit_pr.sh contributions/259-DeusData-codebase-memory-mcp-2232 DeusData/codebase-memory-mcp main fix/project-health-unreadable-counts contributions/259-DeusData-codebase-memory-mcp-2232/pr_title.txt contributions/259-DeusData-codebase-memory-mcp-2232/pr_body.md
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。
