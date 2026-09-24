# uutils/coreutils #9060 — who/unix.rs: improve code coverage

| 项 | 值 |
|---|---|
| Issue | https://github.com/uutils/coreutils/issues/9060 |
| Tier | 高活跃高Star |
| Labels | U - who, good first issue |
| Status | ✅ ready — patch + PR text done (not submitted) |
| Duplicate-PR check | 无 assignee、无评论、无 linked PR。`who repo:uutils/coreutils is:open` 的 open PR 只有 #14495(Windows 实现)、#9092(pid header)、#13389(stdout 写错误)、#11039(PID 存活)、#11579(systemd 回退)，都不是覆盖率测试，也不涉及 run-level。run-level `last=` bug 查过 issue/PR，均未报告 |
| Patch | `0001-who-test-each-record-type-against-a-utmp-file-fix-ru.patch`（base: `main` @ 76774a6） |

## 选题过程（原目标被跳过）
- **原目标 servo/rust-smallvec#673**（`TaggedLen` → `LocatedLength`）：issue 无人认领、无 PR（open 的 #672 是同一作者给 `TaggedLen` 加 `set_location`，没有改名）。但仓库的 `AGENTS.md` 和 Servo 贡献指南（https://book.servo.org/contributing/getting-started.html#ai-contributions）**明确禁止 LLM 生成的代码/PR/issue 内容**。按 brief 第 2 条（合理性判断要看 AGENTS/CONTRIBUTING），**整个 servo/* 都跳过**。
- 排查过的备选：astral-sh/ruff（AI_POLICY 禁止自主 agent 贡献，PR 正文要本人写）、clap（AI 写代码需先在 issue 获得许可，且禁止自主 agent）、nushell（AGENTS.md 拒绝 agent PR）、ratatui（允许 AI，但 good-first-issue 要么已有 PR，#1402/#334，要么已完成，#1015 的第 1 步已由 #2714 合并）、tokio（help-wanted 都是 hard/medium）。uutils 的 #14774/#14775/#11657/#10324/#10097 都已有 PR；#7201 线上已修好（DEVELOPMENT.html 返回 200）。
- **选定 uutils/coreutils #9060**（约 2.3 万 star，非常活跃）。CONTRIBUTING 的 "AI policy" 明确允许 AI 辅助贡献，条件是：提交者理解每一行、不能源自 GNU 代码、patch 小、PR 描述简短且用自己的话写。

## 问题理解
维护者 @sylvestre：`src/uu/who/src/platform/unix.rs` 覆盖率低，"can probably be improved easily"。原因是现有 `test_who.rs` 基本都在和宿主机的 GNU `who` 以及宿主机的 `/var/run/utmp` 对比，而 CI 上 utmp 几乎是空的，其中 9 个测试还被 `#[ignore = "issue #3219"]` 掉了。所以 `event_for`/`emit_event` 的各分支（boot、run-level、clock change、init、login、dead）、有真实记录时的 `emit_session`、`emit_names` 基本都没跑到。

## 合理性判断
合理：维护者本人提的，标了 good first issue。只加测试不改行为。另外，新测试发现了一个真实 bug（见下），修复只有一行，而且有 GNU 行为作参照。

## 改动
1. `tests/by-util/test_who.rs`：新增 `mod utmp_file`（仅 `linux + gnu + x86_64`，因为 glibc 的 utmp 布局依赖架构；这和 `test_uptime.rs` 里同类测试的限制一致）。测试会写一个 384 字节/条的 utmp 文件，每种记录各一条，然后用 `LC_ALL=C TZ=UTC` 跑 `who [opt] FILE`，断言输出：
   - 默认输出、`-b -r -t -p -l -d -u -T` 各选择器、`-a` 整表、`-q`（只断言用户名，见后续事项 2）、run-level 有/无上一级。
   - 期望输出都用系统 GNU `who` 9.4 在同一个文件上跑出来核对过（只运行二进制，没看 GNU 源码，符合 uutils 规定）。
2. `src/uu/who/src/platform/unix.rs`：修 `who -r` 的 `last=`。原代码是 `if last == 'N' { 'S' } else { 'N' }`，所以上一运行级别不是 'N' 时总是打印 `last=N`。GNU 对 3→5 的切换打印 `last=3`。现在改成 `else { last }`。

## 验证
环境：rustc 1.98.1，x86_64 glibc。构建用了 `CARGO_PROFILE_DEV_DEBUG=0 CARGO_INCREMENTAL=0`，因为磁盘空间紧张。
- **基线（未改的 main）**：`cargo test --no-default-features --features who --test tests test_who` → 11 passed, **1 failed (`test_boot`)**, 9 ignored。`test_boot` 是拿宿主 GNU `who -b` 做对比的；本机没有 `/var/run/utmp`，GNU 9.4 会自己合成一个 boot 时间，所以失败。这是环境原因，和本改动无关，改动前后都失败。
- **Red（新测试 + 原代码）**：`... --test tests test_who::utmp_file` → 5 passed, 1 failed：`test_run_level_reports_previous_level`（得到 `last=N`，期望 `last=3`）。
- **Green（加上修复）**：`... --test tests test_who` → 17 passed, 1 failed（还是预先存在的 `test_boot`），9 ignored。6 个新测试全部通过。
- `cargo fmt --all --check` ✅
- `cargo clippy --no-default-features --features who --all-targets -- -D warnings` ✅；`cargo clippy -p uu_who --all-targets -- -D warnings` ✅（加 `--features feat_systemd_logind` 也 ✅）
- `npx cspell@10.2.0 --config .vscode/cSpell.json`（和仓库 pre-commit 用的版本一致），检查 2 个改动文件 → 0 issues ✅
- `cargo test -p uu_who` ✅（0 个单元测试）
- **没跑**：完整的 `cargo clippy --workspace --all-features` 和全量 `cargo test`（磁盘和 CPU 都是共享的）；带 `feat_systemd_logind` 的集成测试（本机缺 `libsystemd`，链接失败）。这个 feature 不在 `feat_os_unix` 里，而且传了 FILE 参数时本来就不走 systemd 分支。

## 后续可另开的（本 PR 未包含，避免扩大范围）
1. `who -H` 表头的 TIME 列比 GNU 窄 2 格：`emit_row` 里 `TIME_WIDTH = 3+2+2+1+2 = 10`，但 "Nov 14 22:13" 有 12 个字符。数据行不受影响，只有表头 "TIME" 的填充不对。
2. `who -q` 输出 `# user=1`，GNU 是 `# users=1`（`en-US.ftl` 里 `who-user-count` 的 [one] 分支）。可能是有意的本地化，要问维护者。

## 如何提交
```sh
git clone https://github.com/uutils/coreutils && cd coreutils   # 或者用你的 fork
git checkout -b who-utmp-fixture-tests origin/main
git am /path/to/contributions/06-uutils-coreutils-9060/0001-who-test-each-record-type-against-a-utmp-file-fix-ru.patch
cargo test --no-default-features --features who --test tests test_who
git push <fork> who-utmp-fixture-tests   # 然后向 uutils/coreutils:main 开 PR
```
- 不需要 DCO/Signed-off-by；commit 格式是 `<util>: <what>`（已遵守）。
- ⚠️ uutils 的 AGENTS.md / AI policy 要求：**PR 描述要简短，用你自己的话写**；**回复 reviewer 必须本人来**；提交前自己过一遍 diff。下面的 PR 正文已经尽量简短，建议你按自己的话再改一下。
- ⚠️ 本仓库说明禁止引用或参照 GNU 源码。本改动只对比了 GNU `who` 二进制的输出。

## PR title
`who: test each record type against a utmp file, fix run-level "last="`

## PR body
```markdown
## Description

Most of `who`'s tests compare against the host's GNU `who` and `/var/run/utmp`, which is close to empty on CI, so the per-record paths in `platform/unix.rs` never ran. This adds tests that write a small utmp file (one boot, run-level, clock-change, init, login, user and dead record) and check `who FILE` with each selector and `-a`. The expected output matches GNU `who` 9.4 on the same file. The tests are limited to x86_64 glibc because the record layout depends on the target.

They caught one bug: `who -r` printed `last=N` for any previous run level other than `N`. GNU prints the level itself (`last=3` for a 3 -> 5 switch). Fixed in one line.

Not included: `-H` pads the TIME heading to 10 columns where GNU uses 12, and `-q` prints `# user=1` where GNU prints `# users=1`. Happy to follow up on these if wanted.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #9060

## Checklist

- [x] Tests pass locally (`cargo test --no-default-features --features who --test tests test_who`: 17 passed; the only failure is `test_boot`, which also fails on main on my machine because it diffs against the host's `who -b`. The new run-level test fails without the fix. `cargo fmt --all --check`, `cargo clippy --no-default-features --features who --all-targets -- -D warnings` and cspell are clean)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (release notes are generated from PRs)
- [ ] Documentation is updated (if applicable) — n/a
```
