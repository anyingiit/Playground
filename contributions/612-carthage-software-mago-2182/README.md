# carthage-software/mago #2182 — Mago misaligns variadic parameters

| 项 | 值 |
|---|---|
| Issue | https://github.com/carthage-software/mago/issues/2182 |
| Tier | 新锐 (Rust 写的 PHP toolchain，2024 年创建，增长快、非常活跃) |
| Labels | 无 |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01: `/pulls?q=2182` 无结果；issue open、无 assignee、无评论、无关联 PR |
| Base | `main` @ 9608b8c |

## 问题理解
开启 `align-parameters = true` 时，formatter 把对齐用的空格插在 `...`（以及 `&`）和变量名之间：
`string ...          $renders`，违反 PSR-12「variadic 运算符与参数名之间不能有空格」。

## 合理性判断
明确的 bug，PSR-12 原文有规定；issue 由维护者建议从 discussion #2153 转出。修改只影响开启 `align-parameters`（默认 false）时的输出。

## 改动
- `crates/formatter/src/internal/format/mod.rs`：`FunctionLikeParameter` 的格式化中，把对齐 padding（`IfBreak` 空格）移到 `&` / `...` **之前**。前缀宽度计算本来就包含 `&`/`...`，因此变量 `$` 仍然对齐，符号紧贴变量：
  `string           ...$renders`
- 新测试 `crates/formatter/tests/cases/align_parameters_variadic_and_by_reference/`（variadic、引用、引用+variadic、无类型 variadic）并在 `tests/mod.rs` 注册。

## 验证（CARGO_TARGET_DIR 在 work 目录）
- Red：撤掉 src 改动，`cargo test -p mago-formatter --test mod align_parameters` → `align_parameters_variadic_and_by_reference` FAILED（3 passed; 1 failed）
- Green：恢复后 → 4 passed
- `cargo test -q -p mago-formatter --locked` → 469 + 53 passed, 0 failed
- `cargo fmt --all -- --check` → OK
- `cargo clippy -p mago-formatter --all-targets --all-features -- -D warnings` → 无警告
- 未运行：`just check` 中的 `cargo run -- fmt --check/lint/analyze`（需构建整个 mago 二进制，且只检查 `composer/`、`scripts/` 下的 PHP，本改动不涉及；mago.toml 也未开启 align-parameters）以及全 workspace 的 `cargo test`/clippy（4 核共享，只跑了受影响的 crate）。

## 需要提交者注意
- 仓库 CI `commit-authorship.yml`：commit 作者/提交者/`Co-authored-by` 不能含 claude/anthropic/copilot 等字样（"AI tools are welcome, but the commit author must be a real person"）。patch 作者是 anyingiit，无 AI trailer —— 不要添加。
- 不需要 DCO（维护者自己的提交带 Signed-off-by，但没有 DCO 检查）。
- PR body 使用了仓库自己的 PR 模板（📌/🔍/🛠️/📂/🔗/📝）并加入了 motivation/disclosure 段落和 checklist。
- 设计选择：保持 `$` 列对齐（sigil 右对齐贴着变量）。另一种风格是让 `...$renders` 从变量列开始；已在 PR 的 Notes for Reviewers 里说明，维护者若偏好另一种需改 `get_parameter_prefix_width`（不计 `&`/`...`）并调整测试期望。
- 无 CHANGELOG 文件，无需文档改动。

## 如何提交
```bash
tools/submit_pr.sh contributions/612-carthage-software-mago-2182 carthage-software/mago main fix/align-parameters-variadic contributions/612-carthage-software-mago-2182/pr_title.txt contributions/612-carthage-software-mago-2182/pr_body.md
```
（手动：fork → `git checkout -b fix/align-parameters-variadic origin/main` → `git am 0001-*.patch` → push → 开 PR，标题见 `pr_title.txt`，正文见 `pr_body.md`。）

## PR title
见 `pr_title.txt`：`fix(formatter): keep \`...\` and \`&\` attached to the variable when aligning parameters`

## PR body
见 `pr_body.md`。
