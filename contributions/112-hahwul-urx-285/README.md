# hahwul/urx #285 — Add unit tests for fmt_count

| 项 | 值 |
|---|---|
| Issue | https://github.com/hahwul/urx/issues/285 |
| Tier | 新锐 |
| Labels | good first issue, progress, rust（`progress` 是 auto-labeler 按 src/progress/** 打的组件标签，不代表有人认领） |
| Status | ✅ ready — 独立复审通过（2026-10-01 19:1x UTC），可提交 |
| 重复 PR 检查 | 2026-10-01 18:3x UTC：issue 仍为 open，无人分配，无评论，没有关联 PR；`pulls?q=285+is:pr` 只搜到无关的 #66。main 仍是 9e11bf6，`fmt_count` 还没有测试。 |
| Base | `main` @ 9e11bf629a97 |

## 问题理解
`src/runner/mod.rs` 里的私有函数 `fmt_count(n: usize) -> String` 给数字加千位分隔符，用在进度汇总中，目前没有单元测试。issue 要求补一个测试，至少覆盖 0 → "0"、1000 → "1,000"、1234567 → "1,234,567"。

## 合理性判断
- issue 由维护者开出，带 good first issue 标签，范围很小，只涉及测试。
- issue 里的行号（20-31）和 "file lacks a test module" 都已过时：函数现在在 41-52 行，文件第 835 行已有 `mod tests { use super::*; ... }`，所以新测试直接加进这个模块，没有另建模块。
- AI 政策：AGENTS.md 是开发指南，没有禁止 AI；没有 CLAUDE.md；CONTRIBUTING.md 没提 AI。labels 里有 "jules"，说明维护者接受 AI 工具。不需要 DCO，没有 PR 模板。
- `src/cache/command.rs:487` 有一个近似的 helper，超出本 issue 范围，没有改，只在 PR 正文里提了一句。

## 改动
`src/runner/mod.rs` 的现有 `mod tests` 末尾新增 2 个测试（+18 行）：
- `test_fmt_count_inserts_thousands_separators`：0、7、999、1000、12345、999_999、1_000_000、1_234_567
- `test_fmt_count_handles_usize_max`（`#[cfg(target_pointer_width = "64")]`）：`usize::MAX` → `"18,446,744,073,709,551,615"`

commit message 按 CONTRIBUTING 的要求用现在时并引用 issue：`Add unit tests for fmt_count (#285)`，正文里写了 `Closes #285`。

## 验证（rustc/cargo 1.97.0，`CARGO_TARGET_DIR=/home/user/work/urx/target-cache`，`-j2`）
这是纯测试改动，没有 red→green。为证明测试能发现回归，做了两次变异测试：
- `cargo test -j2 --bin urx fmt_count`：**2 passed**
- 变异 1：`is_multiple_of(3)` 改成 `is_multiple_of(4)`，两个测试都 **FAILED**（`left: "1000" right: "1,000"`；`"1844,6744,..."`）
- 变异 2：删掉 `i > 0 &&`，`test_fmt_count_inserts_thousands_separators` **FAILED**（`left: ",999" right: "999"`）
- 还原后重新运行：**2 passed**
- `cargo fmt --check`：通过
- `cargo clippy -j2 --tests -- --deny warnings` 和 `cargo clippy -j2 -- --deny warnings`：通过
- `cargo test -j2`（全量）：全部通过（bin 单测 1228 passed / 2 ignored，另外两个测试目标分别 2 passed、1 passed）。AGENTS.md 提到的 OTX 网络失败这次没有出现。

## 需要提交者注意
- 维护者通常自己修 good-first-issue（同类 issue 曾被他直接在 main 上修掉）。提交前请再确认一次 main 上 `fmt_count` 是否已经有测试：`grep -n "fmt_count(0)" src/runner/mod.rs`。
- 近期合并的 PR 基本都来自维护者本人或 dependabot，外部 PR 可能需要等一段时间。
- 不需要 CHANGELOG（CHANGELOG.md 按版本整理，测试改动不需要记录）。
- AI 政策：仓库没有禁止 AI 辅助的规定；PR 正文已含 AI 辅助披露段落，提交时保留即可。commit 中没有 AI trailer（仓库不要求）。
- DCO：不需要（无 DCO bot / 无 Signed-off-by 要求），提交时不要加 `--signoff`。
- 认领：不需要先认领 / 被 assign，issue 无人分配，可直接开 PR。

## 独立复审（2026-10-01 19:1x UTC）
- 重新确认：issue #285 仍 open、无 assignee、无评论；`pulls?q=fmt_count+is:pr` 0 结果；upstream main 仍为 9e11bf6。
- 在 9e11bf6 新 worktree 上 `git am` 补丁：干净应用，作者为 anyingiit <49945850+anyingiit@users.noreply.github.com>，commit 中无 AI 模型名。
- `cargo test -j2 --bin urx fmt_count`：2 passed；把 `is_multiple_of(3)` 改为 `(4)` 后两个测试都 FAILED；还原后 `cargo fmt --check` 通过，`cargo clippy -j2 --tests -- --deny warnings` 通过。
- 未发现需要修改的问题。

## 如何提交
```bash
git clone https://github.com/hahwul/urx && cd urx
git checkout -b test/fmt-count-unit-tests origin/main
git am /home/user/Playground/contributions/112-hahwul-urx-285/0001-Add-unit-tests-for-fmt_count-285.patch
cargo test --bin urx fmt_count && cargo fmt --check && cargo clippy --tests -- --deny warnings
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/112-hahwul-urx-285 hahwul/urx main test/fmt-count-unit-tests contributions/112-hahwul-urx-285/pr_title.txt contributions/112-hahwul-urx-285/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
