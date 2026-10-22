# 396 — sinelaw/fresh#2944 远程文件按远端用户判断是否可写

| 项 | 值 |
|---|---|
| Issue | https://github.com/sinelaw/fresh/issues/2944 |
| Tier | 新锐（Rust 终端编辑器，2025 年起，增长很快，测试非常全） |
| Labels | triaged, actionable（维护者 8-19 标记） |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 **PASS**，已采纳其建议） |
| 重复 PR 检查 | 2026-10-22 21:30 UTC：issue 无评论、无 assignee、Development 空；无相关开放 PR |
| AI 政策 | CONTRIBUTING 无 AI 条款；维护者自己大量用 Claude |
| Base | `master` @ 4caedcd |
| DCO / CLA | 无；PR 模板的 GPL 许可勾选框已勾 |
| 需先认领 | 否 |

## 问题理解
SSH 远程编辑时，Fresh 用**本地**进程的 uid/gid 去比对远程文件的 uid/gid 判断可写；两台机器 id 不同（如 Termux），开了 `auto_read_only` 就会把 0644/0600 的自有文件标成只读。issue 期望由远端 agent 以远端用户身份判断。

## 改动
- `agent.py` 的 `stat` 增加 `writable: os.access(path, W_OK, effective_ids=…)`。
- `RemoteMetadata` 增加可选 `writable`；`convert_metadata` 优先用它，缺失时回退到旧的 uid/gid 比对。
- 新测试：agent 集成测试（真跑 agent.py，chmod 0444 后与 `faccessat` 结果一致）+ convert_metadata 单测（他人 uid 但 agent 说可写 → 可写；自己 uid 但 agent 说不可写 → 只读）。

## 验证
- 红：换回旧 agent.py / 旧判断逻辑 → 两个新测试都失败；绿：`services::remote` 73 个全过。
- `all_tests remote` e2e：90 passed。fmt、`check --all-targets` 通过；clippy 无新增警告。未用真实 SSH（不同 uid）实测。
- 独立复核 agent：VERDICT PASS；采纳：去掉多余 helper（含 `let _ = rm`）、测试改为与 `faccessat` 对比（不依赖 root 判断）、注释与 PR 正文补充 ACL/只读挂载、措辞调整。

## 需要提交者注意
- 与 395（同仓库 fresh）改动文件不重叠，可任意顺序提交。提交信息带 `Assisted-by: Claude Code`。

## 如何提交
```
git clone https://github.com/sinelaw/fresh && cd fresh
git checkout -b remote-writable-by-agent origin/master
git am /path/to/0001-Let-the-remote-agent-decide-whether-a-remote-file-is.patch
```
