# sdlc-pro/spring-lens#524 — 新增 IsolationLevel 枚举

| 项 | 值 |
|---|---|
| Issue | https://github.com/sdlc-pro/spring-lens/issues/524 （core-module, enhancement, good first issue；里程碑 2.0.0；母 epic #506） |
| Tier | 自由 |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 23:20 UTC：无 assignee/评论/关联分支；搜 IsolationLevel 无 PR |
| AI 政策 | 无；正文含 disclosure |
| Base | **`dev`** @ 3386b90（与 298 同建新包 `model.transaction`，文件不重叠，可独立合并） |
| DCO / CLA / 认领 | 无 / 无 / 不需要 |

## 改动
`IsolationLevel`（DEFAULT -1 / READ_UNCOMMITTED 1 / READ_COMMITTED 2 / REPEATABLE_READ 4 / SERIALIZABLE 8），缓存 `VALUES`，`value()`，`from(int)`（0–8 边界 + 循环查找，回退 DEFAULT），完整 JavaDoc；`IsolationLevelTest` 16 例。照 `BeanRole` 写法。

## 验证
- 去掉查找循环（issue 骨架原样）时 4/16 失败，补上后全过。
- `mvn -pl spring-lens-core -am test -Djacoco.skip=true`：150 个测试通过。

## 如何提交
```
tools/submit_pr.sh contributions/299-spring-lens-524 sdlc-pro/spring-lens dev isolation-level-enum contributions/299-spring-lens-524/pr_title.txt contributions/299-spring-lens-524/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
PASS：补丁只含两个 Java 文件；需求与 DoD 全满足；JavaDoc 隔离语义准确；红→绿复现；无竞争；正文准确。建议正文命令带上 `-Djacoco.skip=true` 以与实际一致 → 已改。
