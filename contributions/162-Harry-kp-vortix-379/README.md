# Harry-kp/vortix#379 — vortix list says "1 hours ago" and "1 days ago"

| 项 | 值 |
|---|---|
| Issue | https://github.com/Harry-kp/vortix/issues/379 |
| Tier | 自由 |
| Labels | good first issue |
| Status | ✅ ready — patch + PR text done (not submitted) |
| Base | `main` @ 51b2eb0 (2026-10-02 02:35 +0530, "docs: say where to install shell completions (#377)") |
| Duplicate-PR check | 2026-10-01 23:10–23:30 UTC: `pulls?q=is:pr 379` → 0；`format_elapsed` → 0；`hour` → 仅 #357/#264/#90（已合并、无关）；issue 0 评论、无 assignee、无 linked PR/branch、无 `in-progress` 标签 |

Status: ✅ ready

## 独立复核（2026-10-01 23:45 UTC）

全新 depth-1 克隆（main 仍为 51b2eb0）→ `git am` 干净应用，作者 anyingiit <49945850+anyingiit@users.noreply.github.com>；去掉实现改动后 `cargo test -p vortix format_elapsed` 失败（`left: "1 hours ago"`），恢复后通过；`cargo fmt --check`、`cargo clippy -p vortix --all-targets -D warnings` 均干净；补丁内无 AI 模型名。issue 仍 0 评论、无 assignee、无 linked PR；open PR 仅 #378/#376/#348，#376 改的是 `ui/helpers.rs` 的 `format_relative_time`，不涉及 `profiles.rs`，无冲突。结论：✅ ready。

## 问题理解

维护者 Harry-kp 自己开的 issue（2026-10-01）。`vortix list` 显示 profile 上次使用时间，`format_elapsed`（`crates/vortix/src/cli/profiles.rs`）对小时/天总是用复数，于是出现 "1 hours ago"、"1 days ago"。要求：值为 1 时用单数，≥2 保留复数；"min" 已经没问题；在 `test_format_elapsed` 里加 3600、7199、86400、172799 秒四个用例；`cargo test -p vortix format_elapsed` 通过。

## 合理性判断

- 维护者本人提出、需求精确（连测试值都给了），明显的语法 bug，范围极小。
- AI 政策：仓库有 `AGENTS.md` / `CLAUDE.md`（面向 coding agent 的规则，维护者自己也用 Claude Code + "Autopilot"），CONTRIBUTING / labels 页均无 AI 禁令。
- CONTRIBUTING 要求：bug fix 必须带一个"没有修复就会失败"的测试 ✔；Conventional Commit 标题 ✔；不得改无关文件 ✔。

## 改动

`crates/vortix/src/cli/profiles.rs`：
- 新增私有小函数 `plural_ago(n, unit)`：`n == 1` → `"1 {unit} ago"`，否则 `"{n} {unit}s ago"`；小时与天两个分支调用它。
- `test_format_elapsed` 加 4 个断言（3600/7199 → "1 hour ago"，86_400/172_799 → "1 day ago"）。

## 验证

环境：rustup 按 `rust-toolchain.toml` 装的 1.91.0，`CARGO_TARGET_DIR=/home/user/work/s2-1252/target`，`-j2`。

| 命令 | 结果 |
|---|---|
| 只加测试、未改实现：`cargo test -j2 -p vortix format_elapsed` | **FAILED**：`left: "1 hours ago"` / `right: "1 hour ago"`（profiles.rs:955）→ red |
| 加修复后同命令 | `test cli::profiles::tests::test_format_elapsed ... ok` → green |
| `cargo fmt --all -- --check` | 无输出（通过） |
| `cargo clippy -j2 -p vortix --all-targets -- -D warnings` | Finished，无警告 |
| `cargo test -j2 -p vortix` | lib 972 passed；bin 5；cli_import_config_dir 1；cli_integration 41；cold_start 1；integration 28；suite 38；tunnel_custodian 7；doctest 2 passed 1 ignored；0 failed |

未运行：`scripts/ci-local.sh` 中的 `cargo doc`、`cargo xtask check-*`、release build/size smoke、macOS 相关步骤（改动只涉及一个私有函数和单测，不影响文档/构建）。

## 需要提交者注意

- 仓库 `CLAUDE.md` 写着 "Commit with the configured identity — never pass `-c user.*`"（针对 agent）；补丁作者已是 anyingiit 身份，直接 `git am` 即可。
- `CLAUDE.md` 要求提交前跑维护者的 `ponytail:ponytail-review` 和 `docs-review` skill（维护者私有插件，这里无法运行）；改动很小，无文档引用此输出。
- `CHANGELOG.md` 由维护者发布时用 `/release-changelog` 写，PR 不改。
- 无 DCO 要求，未加 Signed-off-by。PR 模板（What does this PR do / Related Issue / Type of Change / Checklist）已在 pr_body.md 中套用，并包含 Claude Code 披露段。
- 标签 `in-progress` = "Autopilot is working on it"：提交前再看一眼 issue 是否已被打上该标签或有人认领/开 PR（issue 是 10-01 当天新开的）。

## 如何提交

```bash
git clone https://github.com/Harry-kp/vortix && cd vortix
git checkout -b fix-elapsed-singular origin/main
git am /path/to/0001-fix-say-1-hour-ago-and-1-day-ago-in-vortix-list.patch
cargo test -p vortix format_elapsed
git push <your-fork> fix-elapsed-singular   # PR 目标分支: main
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。
