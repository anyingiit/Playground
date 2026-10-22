# arxanas/git-branchless#1308 — `--color` option does not always work

| 项 | 值 |
|---|---|
| Issue | https://github.com/arxanas/git-branchless/issues/1308 |
| Tier | 自由 |
| Labels | bug, good first issue, has-workaround |
| Status | ✅ ready — patch + PR text done, red→green verified (2026-10-22) |
| 重复 PR 检查 | 2026-10-22：issue open、无指派；评论里无人认领（只有 owner 分析和用户 workaround）；`gh pr list --search 1308` 与 `color in:title` 只有 dependabot 和 2022 年的 #512/#342（旧修复），无处理本问题的 PR |
| Base | `master` @ 03d6ab8 |

## 问题理解
`do_main_and_drop_locals`（`git-branchless-invoke`）先 `T::parse_from(args)` 解析完整命令，再用 `GlobalArgs::command().ignore_errors(true)` 单独解析全局参数。后者没有子命令，遇到 `smartlog` 就出错并停止，所以写在子命令之后的 `--color` / `-C` 被忽略；只有 `git branchless --color always smartlog` 生效。

## 合理性判断
维护者打了 bug + good first issue，owner 在评论中提出的方案之一是"从实际执行的子命令读取值"，本改动正是如此（借助 clap 对 `global = true` 参数的向上传播）。owner 明确否定了"只允许在顶层写全局参数"的方案（会破坏 `git sl --color` 这种 alias）。仓库无 AI 政策（AGENTS/CLAUDE/CONTRIBUTING/labels 均未提及）。

## 改动
- `git-branchless-invoke/src/lib.rs`：新增 `parse_global_args::<T>()`：若 `T::command()` 已含 global 的 `color` 参数（主程序 `Opts` 通过 flatten 带有），就用完整命令（ignore_errors）解析，再 `GlobalArgs::from_arg_matches`；否则（独立的 `git-branchless-<sub>` 开发用二进制）沿用旧的 `GlobalArgs::command()`。新增单测 `test_global_args_position`。
- `CHANGELOG.md`：Unreleased → Fixed 加 `(#1308)` 条目。
- Commit：`fix(invoke): respect global options after the subcommand`，作者 anyingiit <49945850+anyingiit@users.noreply.github.com>，正文 `Fixes #1308`。

## 验证
环境：Homebrew cargo/rustc 1.94.1（本机无 rustup，rust-toolchain.toml 的 1.86 未使用），`CARGO_TARGET_DIR` 在工作目录。
- RED（临时把条件改成恒 false = 旧行为）：`cargo test -p git-branchless-invoke` → `test_global_args_position FAILED`，`args: ["git-branchless", "smartlog", "--color", "always"], parsed: GlobalArgs { working_directory: None, color: None }`。
- GREEN：`cargo test -p git-branchless-invoke` → 1 passed（doctest 1 ignored，原本就是 ignore）。
- 手工端到端：`cargo build -p git-branchless`，在临时仓库 `git-branchless init` 后：`--color always smartlog`、`smartlog --color always`、`smartlog --color=always`、alias `git sl --color always` 管道到 `cat` 都有 ANSI 转义；`smartlog --color never` 和无参数时没有。
- `cargo fmt --all -- --check` OK；`cargo clippy -p git-branchless-invoke --no-deps --all-targets -- --deny warnings --allow renamed_and_removed_lints` 无警告。
- 注意：CI 的 `cargo clippy --workspace ... --deny warnings` 在本机 rustc 1.94 下 `git-branchless-lib` 有 4 个既有错误（新版 lint），与本改动无关；CI 用 1.86 不受影响。
- 未跑：全 workspace 集成测试（需要 TEST_GIT 环境、耗时长）；改动只影响全局参数解析。

## 需要提交者注意
- 仓库不要求 DCO/CLA，也无 changeset 机制；无 AI trailer 要求，PR 正文已含 Claude Code 披露段落。
- CHANGELOG 条目用的是 issue 号 `(#1308)`（与现有条目风格一致）。
- 设计取舍：独立 `git-branchless-<sub>` 二进制（仅开发用）仍是旧行为；如维护者希望也支持，可改为对 `T::command()` 调 `GlobalArgs::augment_args`。

## 如何提交
```bash
git clone https://github.com/anyingiit/git-branchless.git && cd git-branchless   # 先 fork
git remote add upstream https://github.com/arxanas/git-branchless.git && git fetch upstream
git checkout -b fix-global-args-after-subcommand upstream/master
git am /path/to/contributions/207-arxanas-git-branchless-1308/0001-*.patch
cargo test -p git-branchless-invoke
git push origin fix-global-args-after-subcommand
```
PR 标题：见 `pr_title.txt`；PR 正文：见 `pr_body.md`。

## 独立复核（2026-10-23）
- 上游复查：#1308 仍 open、无指派，最后评论 2024-05；无竞争 PR。
- 新浅克隆 master @ 03d6ab8，`git am` 干净；作者 anyingiit。
- RED（条件改为恒 false）：`test_global_args_position` FAIL（`smartlog --color always` → color: None）；GREEN：`cargo test -p git-branchless-invoke` 1 passed。fmt OK；clippy（不加 allow 参数）`--deny warnings` 无警告。
- 独立二进制：7 个 `git-branchless-<sub>` 的 T（SmartlogArgs 等）都不含全局 color 参数 → 走原 `GlobalArgs::command()` 路径，行为与原来逐字节一致（它们本来就会在 `T::parse_from` 处拒绝 `--color`/`-C`，未变）。
- 子命令自身参数：全仓只有 GlobalArgs 定义 `-C`/`--color`；`wrap` 用 external_subcommand 原样收参，`git-branchless wrap commit --amend --allow-empty -C HEAD` 正常（-C 交给 git，未被当作 chdir）；`test run -x 'echo -C foo --color always'` 正常。
- 端到端：`smartlog --color always`/`--color=always`/前置 `--color always`/alias `git sl --color always` 有 ANSI；`--color never`/无参数没有；`smartlog -C <repo>` 在别处运行正常。
- 结论：无需修改。
