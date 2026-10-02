# arxanas/git-branchless#498 — Revsets don't support `#` in branch names

| 项 | 值 |
|---|---|
| Issue | https://github.com/arxanas/git-branchless/issues/498 |
| Tier | 自由 |
| Labels | bug, good first issue |
| Status | ✅ ready — patch + PR text done, red→green verified (2026-10-01) |
| 重复 PR 检查 | 2026-10-01：issue 无评论、无指派、无关联 PR；`/pulls?q=498` 只有无关 dependabot PR；标题含 revset 的 PR 全部检查过，无处理 `#` 的 |
| Base | `master` @ 03d6ab8 |

## 问题理解
`#` 是合法的 Git 分支名字符，但 revset 词法中未加引号的 Name 只允许 `[a-zA-Z0-9_$@/-]`（以及单个 `.`），所以 `stack(mr/1229#crc)` 报 `Invalid token`。

## 合理性判断
维护者打了 bug + good first issue；`#` 不是任何 revset 运算符，加入字符集无歧义。仓库无 AI 政策（AGENTS/CLAUDE/CONTRIBUTING/labels 均未提及）。

## 改动
- `git-branchless-revset/src/grammar.lalrpop`：Name 正则字符集加入 `#`。
- `git-branchless-revset/src/parser.rs`：新测试 `test_revset_parse_hash_in_name`（insta 内联快照，用 `r##"..."##` 因内容含 `"#`）。
- `CHANGELOG.md`：Unreleased → Fixed 加一条 `(#498)`。
- Commit：Conventional 风格 `fix(revset): allow \`#\` in branch names`，作者 anyingiit <49945850+anyingiit@users.noreply.github.com>。

## 验证
环境：rust 1.86（rust-toolchain.toml），git 2.43，`TEST_GIT=/usr/bin/git TEST_GIT_EXEC_PATH=$(git --exec-path)`（eval 测试需先 `cargo build -p git-branchless`）。
- RED（只加测试）：`cargo test -p git-branchless-revset --lib parser::` → `test_revset_parse_hash_in_name FAILED`，`"Invalid token at 7"`。
- GREEN：`cargo test -p git-branchless-revset` → 16 passed；`cargo test -p git-branchless-query` → 6 passed。
- 手工：建分支 `mr/1229#crc` 加两个提交，`git branchless query 'stack(mr/1229#crc)'` 正确输出两个提交。
- `cargo fmt --all -- --check` OK；`cargo clippy -p git-branchless-revset --all-features --all-targets -- --deny warnings --allow renamed_and_removed_lints` 无警告。
- 未跑：全 workspace 测试（CI 会跑；改动只影响 revset 词法）。

## 需要提交者注意
- 仓库不要求 DCO，也无 AI trailer 要求；PR 正文已含 Claude Code 披露段落。
- CHANGELOG 条目用的是 issue 号 `(#498)`；如维护者习惯写 PR 号，可在开 PR 后改。

## 如何提交
```bash
git clone https://github.com/anyingiit/git-branchless.git && cd git-branchless   # 先 fork
git remote add upstream https://github.com/arxanas/git-branchless.git && git fetch upstream
git checkout -b fix-revset-hash-in-branch-names upstream/master
git am /path/to/contributions/058-arxanas-git-branchless-498/0001-*.patch
cargo test -p git-branchless-revset
git push origin fix-revset-hash-in-branch-names
```
或使用脚本：
```bash
tools/submit_pr.sh contributions/058-arxanas-git-branchless-498 arxanas/git-branchless master fix-revset-hash-in-branch-names contributions/058-arxanas-git-branchless-498/pr_title.txt contributions/058-arxanas-git-branchless-498/pr_body.md
```
PR 标题：见 `pr_title.txt`；PR 正文：见 `pr_body.md`。
