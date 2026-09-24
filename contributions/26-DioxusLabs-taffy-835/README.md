# DioxusLabs/taffy #835 — Document `known_dimensions` vs `available_space` on `LayoutInput`

| 项 | 值 |
|---|---|
| Issue | https://github.com/DioxusLabs/taffy/issues/835 |
| Tier | 高活跃高Star (taffy ≈3.6k★；最近提交 2026-09-18，外部贡献者的 PR 也会被合并，例如 #1181、#1189) |
| Labels | documentation, good first issue |
| Status | ✅ 完成 — patch 已导出，测试/文档构建通过，PR 文本已写 |
| 重复 PR 检查 | 2026-09-24 开工前和收尾时都查过（web 搜索 `repo:DioxusLabs/taffy is:pr` 搜 `835` / `known_dimensions` / `LayoutInput`）：没有针对 #835 的 PR；issue 没有 assignee，也没有评论认领。相关但不冲突：#893（open，只改 `LayoutInput::run_mode` 的一行注释，和本补丁改的行不重叠）。 |
| Base | `main` @ `e661b359`（2026-09-18） |
| Patch | `0001-Document-known_dimensions-vs-available_space-on-Layo.patch`（1 个文件，+64 行，只改文档） |

## 问题理解
Issue #835（Fancyflame 提出，由讨论 #716 延伸而来）要求把 #716 里维护者 nicoburns 的解释写进 `LayoutInput` 的 rustdoc。解释的核心有三点：
- `available_space` = containing block（大致就是父节点）的尺寸，是**软约束**，相当于问节点："如果给你这么多空间，你会多大？"
- `known_dimensions` = 节点**自身**的尺寸，是**硬约束**，相当于问节点："如果你这一维正好是 X，另一维是多少？"
- `known_dimensions` 优先：某一轴给了 known dimension，这一轴的 available_space 就可以不看，该轴的输出尺寸也会被忽略。

## 合理性判断
- 这是维护者在 #716 给出的原话，贴了 good first issue + documentation 标签，要求明确。
- 按代码核对过："输出被忽略 / known 优先"这个说法和 `src/compute/leaf.rs` 的实现一致：
  `known_dimensions.or(node_size).unwrap_or(measured_size …)`，而且该轴的 available space 会先被替换成 known dimension。
- 现有的 field 文档已经说了 `known_dimensions` 是什么，但没讲它和 `available_space` 的区别，也没讲谁优先，所以 #835 仍然有价值，并非已经修复。
- AI 政策：taffy 仓库（CONTRIBUTING.md、PR 模板、.github）没有 AI/LLM 相关规定。

## 改动（`src/tree/layout.rs`）
- `LayoutInput` 的类型级文档新增 `# known_dimensions vs available_space` 小节：分别说明软/硬约束，并说明 known 优先。
- 新增一个可运行的 doctest：一个简化的文本 measure 函数，演示 (1) 只有 available width = 100 时文本换行成两行；(2) known width = 50 时优先使用 known 值。
- `known_dimensions` 和 `available_space` 两个字段的文档各加一句互相引用，并链接到类型级说明。
- CHANGELOG：只改文档、不影响库用户，所以没改（PR 模板只要求"影响外部用户的改动"更新 CHANGELOG）。

## 验证（工作目录 `/home/user/work/taffy`，toolchain 1.98.1，`CARGO_TARGET_DIR` 放在工作目录内，完成后已删除）
| 命令 | 结果 |
|---|---|
| `cargo fmt --all -- --check` | ✅ 通过 |
| `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps` 与加 `--all-features` 的版本 | ✅ 无警告（新加的 intra-doc 链接都能解析） |
| `cargo test --doc -- LayoutInput` | ✅ 1 passed（新 doctest）；未打补丁的 base 上同一过滤条件匹配 0 个 doctest（等价于 red→green：新示例确实被执行、断言确实被检查） |
| `cargo test --doc` | ✅ 6 passed |
| `cargo test --tests`（默认 features） | ✅ 151 + 115（4 ignored）+ 6125 passed |
| `cargo test --all-features` | ✅ 153 + 117（4 ignored）+ 6 + 6125 passed |
| `cargo clippy --all-features --all-targets` | 改动的文件 0 个告警。`-D warnings` 下有 2 个**已有**错误（`src/style/compact_length.rs:31` MSRV `map_addr`、`src/util/parse.rs:19` `useless_borrows_in_formatting`），`git stash` 回到 base 后同样出现，与本改动无关（CI 本身不跑 clippy；justfile 用的是 `cargo +nightly clippy`，且不带 `-D`） |

## 如何提交
```bash
git clone https://github.com/DioxusLabs/taffy && cd taffy
git checkout -b docs-layout-input-known-dimensions origin/main
git am /path/to/0001-Document-known_dimensions-vs-available_space-on-Layo.patch
git push <your-fork> docs-layout-input-known-dimensions   # 然后向 DioxusLabs/taffy:main 开 PR
```

## 需要提交者注意
- taffy 的 CONTRIBUTING 流程是"先在 issue 下评论说要做，由团队 assign"。建议先在 #835 留一句（你自己写），再开 PR。
- 仓库没有 AI 政策，不需要 DCO / Signed-off-by，也没有 Conventional Commits 要求（提交标题风格为 `Area: description`）。
- 开 PR 前请自己读一遍文档措辞，确认和你对 taffy 的理解一致。

---

## PR title
Document `known_dimensions` vs `available_space` on `LayoutInput`

## PR body
```markdown
# Objective

Fixes #835

`LayoutInput` documents what `known_dimensions` and `available_space` are individually, but not how they differ or which one wins. This adds the explanation from #716 to the `LayoutInput` docs.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Context

- New "`known_dimensions` vs `available_space`" section in the `LayoutInput` type docs:
  - `available_space` is the size of the containing block (roughly, the parent). It is a soft constraint: "if you had this much space, what size would you be?"
  - `known_dimensions` is the size of the node itself. It is a hard constraint: "if your size in this axis is exactly X, what is the other axis?"
  - `known_dimensions` takes precedence. This matches `compute_leaf_layout`, which uses `known_dimensions.or(node_size).unwrap_or(measured_size …)` and replaces the available space in a known axis.
- A small runnable doctest: a toy text measure function that shows both cases (wrapping to the available width vs. a known width winning).
- One-line cross-references on the `known_dimensions` and `available_space` field docs.

This is a docs-only change, so there is no CHANGELOG entry.

Verification (rustc 1.98.1):
- `cargo fmt --all -- --check`: ok
- `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps` (with and without `--all-features`): no warnings
- `cargo test --doc`: 6 passed, including the new `LayoutInput` doctest
- `cargo test --tests` and `cargo test --all-features`: all pass (6125 generated tests, etc.)

## Feedback wanted

Happy to trim the example or move it elsewhere (e.g. next to the measure-function docs) if you'd prefer it shorter.
```

## 候选排除记录（本次搜索中放弃的候选）
- lycheeverse/lychee #2143：两个 PR (#2144, #2233) 都被关闭，维护者表示要"从根本上移除 `error:` sentinel"，方案由维护者主导。
- lycheeverse/lychee #2193：**issue 的前提在 HEAD (2c1fb3a) 上不成立**。lychee 实际不会重试 5xx，只重试 429、超时和部分网络错误。
  用本地 HTTP server 实测：521/500/503 各只被请求 1 次，429 被请求 4 次（`--max-retries 3`）。
  原因：`Status::Error(RejectedStatusCode(_))` 的 `should_retry` 只对 429 返回 true（d22d188，2025-05）；
  `RetryExt for StatusCode` 里的 5xx 规则只用于"是否缓存"的判断。看起来是 2025 年去掉 `error_for_status` 后留下的回归，
  适合作为 issue 评论提供给维护者，不适合直接提 PR。
- AI 政策冲突而跳过：rust-lang/*（LLM 代码需事先取得 reviewer 同意）、gleam、typst、fish-shell（禁止 AI）；
  PyO3、pyrefly、diesel、zizmor（good first issue 禁止用 AI）；astral-sh/*（禁止自主 agent）；
  biome、harper、topgrade、sharkdp/fd（要求 PR 描述由人类撰写）。
- 已有 PR、已完成或设计不明确：jj #9375（设计不明确）、oxc #22955（剩余规则都被阻塞）、git-cliff #1638/#1579、
  onefetch #1527、lldap #1202/#994、arrow-rs #11032、pixi #5672、burn #4312/#544、cargo-semver-checks #1262、
  lsd #857（最近一次提交在 8 月）、turso（大量 bot PR）。
