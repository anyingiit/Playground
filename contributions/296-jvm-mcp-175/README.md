# oscarbol09/jvm-mcp#175 — find_slow_queries 可配置结果数量

| 项 | 值 |
|---|---|
| Issue | https://github.com/oscarbol09/jvm-mcp/issues/175 （enhancement, good first issue, help wanted；2026-10-22 新开） |
| Tier | 新锐 |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 23:10 UTC：无关联 PR、无评论/assignee；open PR 仅 #180、#181，无关 |
| AI 政策 | 同 295：未禁止，只要求避免 AI 填充段落；正文只留一句 disclosure |
| Base | `main` @ 68e7fc7（与 295 改的文件不重叠，可各自独立合并） |
| DCO / CLA / 认领 | 无 / 无 / 不需要 |

## 改动
- core：`findSlowQueries(int limit)`，`Math.clamp(limit, 1, 100)`；无参版本委托默认 20；SQL 改为 `LIMIT ?` 绑定参数。
- MCP 工具 schema 加可选 `limit`（1–100，默认 20），用 `ToolArgs.getIntArg` 读取并夹取。
- CLI：`--limit`（默认 20）。README 工具表与示例。
- 测试：clamp 参数化测试、handler 传参/夹取/schema 测试、CLI 默认与 `--limit 5` 测试。

## 验证
- 去掉主代码改动后新测试编译失败/失败（红），加上后通过。
- `mvn verify`：core 371、mcp-server 285，0 失败，JaCoCo 达标。PostgreSQL Testcontainers IT 因无 Docker 跳过（正文已说明）。

## 如何提交
```
tools/submit_pr.sh contributions/296-jvm-mcp-175 oscarbol09/jvm-mcp main slow-queries-limit contributions/296-jvm-mcp-175/pr_title.txt contributions/296-jvm-mcp-175/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
PASS：新克隆干净应用，verify 计数一致；`LIMIT ?` 在 pgJDBC 下有效；三项需求全部覆盖；测试有意义且风格一致；README 准确；无竞争 PR；正文所有说法（含 get_heap_histogram 对比）属实。建议正文写"等价的 mvn verify" → 已改。
