# zerobrewhq/zerobrew#357 — Enable arg_required_else_help

| 项 | 内容 |
|---|---|
| Status | ✅ ready — patch、测试 red→green、fmt/clippy/test 均已完成，PR 文本已写 |
| Issue | https://github.com/zerobrewhq/zerobrew/issues/357 |
| Tier | 新锐 |
| Labels | area: cli, good first issue, priority: low, status: accepted, type: feature（无 assignee，无评论） |
| 重复 PR 检查 | 2026-10-01 查过 `pulls?q=357` 和 `is:pr arg_required_else_help`，都是 0 条 |
| Base | `main` @ d9c8b0a |

## 问题理解
Issue 希望 `zb` 不带参数时显示帮助，而不是报 "requires a subcommand"。实测发现，clap derive 遇到必填子命令时已经隐式开启了 `arg_required_else_help`，所以环境干净时裸跑 `zb` 本来就会显示帮助。
**真正的根因**：clap 把通过环境变量（`env = "ZEROBREW_ROOT"`、`env = "ZEROBREW_AUTO_INIT"`）填入的参数也算作“用户给了参数”。`zb init` 和 `install.sh` 都会把 `export ZEROBREW_ROOT=...` 写进 shell 配置，所以几乎所有装好的用户都会看到 issue 里的那个错误。复现：`ZEROBREW_ROOT=/tmp/x zb` 会报错。

## 合理性判断
维护者已经打了 `status: accepted`，并归入 milestone "CLI UX & Documentation"，诉求合理。

## 改动
- `zb_cli/src/cli.rs`：新增 `Cli::try_parse_args(args)`。完全没有参数时，先用 `mut_args(|a| a.env(None))` 去掉 env 来源再解析，这样走的是 clap 自带的 help-on-missing-subcommand 路径（输出到 stderr、退出码 2，和无 env 时一致）。有参数时行为不变。
- `zb_cli/src/bin/zb.rs`：`Cli::parse()` 改为 `Cli::try_parse_args(std::env::args_os()).unwrap_or_else(|e| e.exit())`。
- 新增 3 个单元测试，并在 `CHANGELOG.md` 的 Unreleased 下加了 `### Fixed` 条目。
- 已知取舍：裸跑 `zb` 显示的帮助里不再有 `[env: ZEROBREW_ROOT=]` 这类提示（`zb --help` 仍然有）。PR 描述里已说明。

## 验证
- Red：临时把 `if args.len() <= 1` 改成 `if false && ...`，运行 `cargo test -p zb_cli --lib cli::tests`，结果 `shows_help_without_arguments_when_env_options_are_set` FAILED（left: MissingSubcommand, right: DisplayHelpOnMissingArgumentOrSubcommand）。
- Green：恢复后同一命令 10 passed。
- `cargo fmt --all -- --check` 通过；`cargo clippy --workspace --all-targets -- -D warnings` 通过。
- `cargo test --workspace --no-fail-fast` 结果：zb_core 50 passed，zb_io 272 passed，zb_cli lib 64 passed / 2 failed。失败的是 `init::tests::is_writable_returns_false_for_readonly_dir` 和 `needs_init_when_not_writable`，原因是这里以 root 运行（root 能写只读目录）。这两个在 base 分支上同样失败，与本改动无关。被 `#[ignore]` 的网络测试未运行。
- 手动验证（用 debug 二进制）：`zb`、`ZEROBREW_ROOT=/tmp/x zb`、`ZEROBREW_AUTO_INIT=true zb` 都显示帮助，exit 2；`zb -v` 仍然报缺少子命令；`zb --version` 正常。

## 需要提交者注意
- CONTRIBUTING 里有 “A note on LLM usage”：允许使用 LLM，但大量依赖 LLM、缺少思考的 PR 可能被直接关闭。PR 模板**强制要求披露 AI 使用**，pr_body.md 已勾选 AI 披露框并说明了用途。建议提交前自己读一遍改动，确认能解释清楚根因（env 参数被 clap 当成显式参数）。
- 提交信息格式按要求为 `fix(zb_cli): ...`。仓库不要求 DCO，也不要求 AI trailer，所以都没加。
- PR 正文开头是仓库模板要求的勾选项，已经填好。

## 如何提交
```bash
git clone https://github.com/zerobrewhq/zerobrew && cd zerobrew
git checkout -b fix/357-help-without-args origin/main
git am /path/to/053-zerobrewhq-zerobrew-357/0001-*.patch
# 推到 fork 之后：
tools/submit_pr.sh contributions/053-zerobrewhq-zerobrew-357 zerobrewhq/zerobrew main fix/357-help-without-args contributions/053-zerobrewhq-zerobrew-357/pr_title.txt contributions/053-zerobrewhq-zerobrew-357/pr_body.md
```
