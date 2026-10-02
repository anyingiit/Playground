# lysine-dev/okio #1874 — collectRecursively opens symlinks even when followSymlinks=false

| 项目 | 内容 |
|---|---|
| Issue | https://github.com/lysine-dev/okio/issues/1874 （原 square/okio，已迁移到 lysine-dev/okio） |
| Tier | 高星 |
| Labels | `PR welcome`, `file system` |
| Status | ⏭️ skipped — 项目明令禁止 LLM/生成式工具贡献 |
| 重复 PR 检查 | 无（`pulls?q=1874`、`symlink`、`collectRecursively` 均无相关 PR；issue 未分配、无评论） |

## 跳过原因

仓库 `CONTRIBUTING.md`（main @ fb4817a）有专门的 “No Generative Tools” 一节：

> We don't use LLMs or generative tools in our source code or documentation. ...
> We require all contributors to do likewise. ...
> We'll immediately reject LLM-generated contributions to protect the culture of our project. We ban repeat offenders.

例外仅限：非英语母语者的机器翻译（需披露）、本地自动补全。本项目的工作方式（Claude Code 生成补丁与 PR 文本）明显违反该政策，
按 CONTRIBUTION_BRIEF 2b 规则 **跳过**，未实现、未构建、未运行任何代码。

## 已做的核查

- Issue：open，未分配，无评论，作者 OliverO2，2026-09-23 创建；问题本身合理（`okio/src/commonMain/kotlin/okio/internal/FileSystem.kt`
  中 `collectRecursively` 在 `followSymlinks=false` 时仍对符号链接调用 `listOrNull`，在 WASI 上遇到符号链接环会导致 `deleteRecursively` 失败）。
- 规范 owner：`build.gradle.kts` 的 POM/SCM 指向 `github.com/lysine-dev/okio`，GitHub issue 页显示 `lysine-dev/okio`，确认仓库已迁移。
- 不在排除列表中（grep `okio` / `lysine` 无命中）。
- 浅克隆 `/home/user/work/square-okio` 后运行 `tools/audit_repo.py`：无自动执行钩子、无可疑模式；仅 `gradle/wrapper/gradle-wrapper.jar`（标准 wrapper，distributionUrl 为 services.gradle.org 且带 sha256 校验）。因已决定跳过，未执行任何构建。克隆已删除。

## 需要提交者注意

如果提交者希望亲自修复，必须**完全手写**代码、测试与 PR 文本（项目会直接拒绝并封禁使用 LLM 的贡献者），不要使用本仓库中任何 AI 产出的内容。
