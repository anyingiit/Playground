# uutils/acl #21 — getfacl: implement --absolute-names

| 项 | 值 |
|---|---|
| Issue | https://github.com/uutils/acl/issues/21 |
| Tier | 自由 |
| Labels | good first issue |
| Status | ✅ ready（patch + PR 文本已就绪） |
| 重复 PR 检查 | 2026-10-01 复核：issue open、无 assignee、无评论；仓库 0 个 open PR，按 "absolute" 搜索只有 renovate 的依赖 PR |
| Base | `main` @ 2340e96 |

## 问题理解
`getfacl` 已经定义了 `-p/--absolute-names` 参数，但没有实现：绝对路径总是原样打印。GNU getfacl 的默认行为是在 `# file:` 头中去掉开头的 `/`（以及开头的 `./`），去完为空时用 `.`，并且整个运行期间只向 stderr 打印一次 `getfacl: Removing leading '/' from absolute path names`。加 `-p` 时保留原名。

## 合理性判断
issue 由维护者开，带 good first issue 标签；参数在 `uu_app()` 中已经声明，只差实现。仓库内（AGENTS/CONTRIBUTING/.github）没有 AI 相关规定，标签描述中也没有限制。但 uutils 组织（coreutils）的 AI policy 允许 AI 辅助，条件是：提交者理解每一行、不能抄 GNU 代码、patch 要小、PR 描述简短且用自己的话写。

## 改动
- `src/uu/getfacl/src/getfacl.rs`：`Config` 新增 `absolute_names`；新增 `strip_leading_slash()`，按上面的 GNU 规则处理；`uumain` 中计算显示名并只警告一次（用 `show_error!`，不改变退出码）。新增单元测试。
- `tests/by-util/test_getfacl.rs`：新增 3 个集成测试（绝对路径，两个文件只警告一次；`-p`/`--absolute-names`；`./file`）。

## 验证
（`CARGO_TARGET_DIR` 设在工作目录内，用完已删除）
- Red：只回退 src 改动后运行 `cargo test --test tests test_getfacl`：6 passed，2 failed（`test_absolute_path_strips_leading_slash`、`test_relative_path_strips_dot_slash`）。`-p` 测试在 base 上也会通过，因为 base 本来就保留斜杠。
- Green：`cargo test`：11 passed，0 failed；`cargo test -p uu_getfacl`：1 passed。
- `cargo fmt --all -- --check`：OK；`cargo clippy --all-targets -- -D warnings`：clean（CI 实际跑的是不带 `--all-targets` 的版本，更宽松）。
- 手动：`acl getfacl /etc/hostname` → stderr 出现警告，stdout 为 `# file: etc/hostname`。
- 本机没有 GNU `getfacl`，没法逐字节对比，GNU 行为是按记忆中的 acl 源码 `do_print()` 写的。

## 需要提交者注意
- ⚠️ uutils 的 AI policy：**PR 描述要简短，用你自己的话写**；回复 reviewer 必须你本人来；提交前自己过一遍 diff。下面的 PR 正文已经尽量简短，建议按自己的话改一改。
- 实现基于对 GNU 行为的理解，不是复制 GNU 代码（uutils 禁止参考 GNU 源码），代码是独立写的。如果 reviewer 问起，可以说是按 GNU getfacl 的观察行为实现的。
- 对 `./` 的剥离是 GNU 行为，但超出了 issue 标题的字面范围；如果 reviewer 不想要，可以删掉 `strip_leading_slash` 中 `strip_prefix("./")` 分支，以及 `test_relative_path_strips_dot_slash`。
- 不需要 DCO / Signed-off-by。commit 作者为 anyingiit <49945850+anyingiit@users.noreply.github.com>。

## 如何提交
```bash
git clone https://github.com/anyingiit/acl && cd acl   # 先在 GitHub fork uutils/acl
git remote add upstream https://github.com/uutils/acl && git fetch upstream
git checkout -b getfacl-absolute-names upstream/main
git am /path/to/0001-getfacl-implement-absolute-names.patch
cargo test && cargo fmt --all -- --check && cargo clippy -- -D warnings
git push origin getfacl-absolute-names
gh pr create --repo uutils/acl --head anyingiit:getfacl-absolute-names \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR Title
getfacl: implement --absolute-names

## PR Body
见 `pr_body.md`。
