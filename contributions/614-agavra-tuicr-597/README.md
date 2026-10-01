# agavra/tuicr #597 — PHP syntax highlighting is missing in PR mode

| 项 | 值 |
|---|---|
| Issue | https://github.com/agavra/tuicr/issues/597 |
| Tier | 新锐 (3.3k stars, 年轻且快速增长) |
| Labels | 无 |
| Status | ✅ ready |
| 重复 PR 检查 | 2026-10-01：`/pulls?q=597` 0 结果；issue open、无指派、无评论、timeline 无关联 PR。**注意** #625（closes #547，作者 ronen-hoffer，PR 全文件异步高亮，8/19 起停滞，9/30 作者询问是否该关闭）范围更大，可能顺带修复本问题，但未引用 #597 |
| AI 政策 | CONTRIBUTING.md 明确工作流就是"用 Codex/Claude 等 AI agent 做修改"，无限制；无 DCO、无 AI trailer 要求 |

## 问题理解
容器语法（PHP/Vue/Svelte/Astro/MDX/ERB）在 `diff_parser` 中跳过逐 hunk 高亮，依赖之后的全文件高亮 pass（`enhance_with_full_file_highlight`）。本地 git/hg/jj 后端会跑这一步，但 forge PR 路径（`fetch_pr_data` → `prepare_open_pr` → `parse_file_patches`）从不跑，所以 `tuicr pr <n>` 中 PHP 完全无高亮。issue 作者自己给出的分析与代码一致。

## 合理性判断
明确的 bug，issue 中给了根因；修复方向正是 issue 建议的"在 PR 路径补上全文件 pass"。

## 改动
- `FilePatch` 新增 `old_content` / `new_content: Option<String>`（只有 forge PR 路径会填）。
- `pr_open::fetch_pr_data`（后台线程）对容器语法文件调用已有的 `ForgeBackend::fetch_file_content`（优先本地 blob，否则 API），最多 50 个文件。
- `diff_parser::parse_file_patches` 对带内容的文件运行 `enhance_with_full_file_highlight`；应用前校验 diff 行与该侧文件内容逐行一致，不一致（如 base_sha 是移动后的 base 分支 tip）就丢弃该侧，避免错位上色。
- `AGENTS.md` 新增 gotcha #22。
- 未覆盖：PR 中的 commit-range 子视图（已在 PR body 说明）。

## 验证
在 `/home/user/work/tuicr`（`CARGO_TARGET_DIR=target`）：
- 红：注释掉 `attach_container_file_contents` 调用后 `cargo test --lib pr_open` → 2 failed（两个 PHP 测试）。
- 绿：恢复后 `cargo test --lib pr_open` → 15 passed。
- `cargo fmt --all --check` ✅；`cargo clippy -- -D warnings` ✅。
- `cargo test`：1829 passed，2 failed（`default_preference_routes_reftable_repo_to_cli`、`should_discover_worktree_with_relativeworktrees_extension`），在未修改的 main 上同样失败（本机 git 2.43 不支持 reftable/relativeWorktrees）；`--test forge_remote_formats` 3 passed；`--bins` 2 passed。

## 需要提交者注意
- 与 #625 有重叠：若维护者偏好 #625 的方案，本 PR 可能被关闭；PR body 中已主动说明。提交前可再看一眼 #625 是否已合并 / #597 是否已有人认领。
- 无 PR 模板、无 DCO、无 AI trailer 要求；CHANGELOG 由 git-cliff 生成，无需手改。
- 50 文件上限是自己定的数值，评审可能会提出调整。

## 如何提交
base 分支：`main`
```bash
tools/submit_pr.sh contributions/614-agavra-tuicr-597 agavra/tuicr main fix/pr-container-grammar-highlight contributions/614-agavra-tuicr-597/pr_title.txt contributions/614-agavra-tuicr-597/pr_body.md
```
或手动：fork → `git checkout -b fix/pr-container-grammar-highlight origin/main` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR。

## 独立复核 (2026-10-01)
issue 仍 open、无指派、`/pulls?q=597` 0 结果；patch 在 main 新浅克隆上 `git am` 干净；`cargo test --lib forge::pr_open` 去掉 `attach_container_file_contents` 调用 → 2 failed，恢复 → 全绿；`cargo fmt --all --check` ✅；CI 同款 `cargo clippy -- -D warnings` ✅（`--all-targets` 有一个 main 上既有的 `src/vcs/git/mod.rs:708` clippy 警告，与本 PR 无关）。
