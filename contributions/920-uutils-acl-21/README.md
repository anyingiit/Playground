# uutils/acl#21 — getfacl: implement --absolute-names

| 项 | 值 |
|---|---|
| Issue | https://github.com/uutils/acl/issues/21 |
| Tier | 自由 |
| Labels | good first issue |
| Status | ✅ ready（补丁 + PR 文本已完成） |
| 独立审核 | ✅ 2026-10-02：fresh clone `git am` 通过；red 4 failed/6 passed → green 10 passed；fmt/clippy --all-targets/cargo test 13 passed；issue 仍开放、无评论、仓库 0 open PR |
| 重复 PR 检查 | Issue 开放、无 assignee、无评论、无关联 PR；仓库 0 个 open PR，PR 搜索 "absolute" 只有 renovate 依赖更新（2026-10-01 核查） |
| AI 政策 | 仓库内未找到 AI/LLM 相关规定（grep LLM/AI-generated/Copilot/ChatGPT 无结果；`good first issue` 标签描述为 "Good for newcomers"） |
| Base | `main` @ 2340e96 |

## 问题理解
`getfacl` 已经声明了 `-p/--absolute-names` 参数，但实现里完全没有用到。GNU getfacl 的默认行为是：去掉 `# file:` 头里路径开头的 `/`，并向 stderr 输出一次 `getfacl: Removing leading '/' from absolute path names`；同时也会去掉开头的 `./`，结果为空时显示 `.`。加上 `-p` 就原样保留路径。

## 合理性判断
Issue 由维护者 sylvestre 提出，属于 uutils 对齐 GNU 行为的工作，范围很小，合理。

## 改动
- `src/uu/getfacl/src/getfacl.rs`：`Config` 增加 `absolute_names` 字段；新增 `display_name()` 计算头部显示名（警告只打印一次）。读 metadata 和 xattr 时仍使用原始路径。
- `tests/by-util/test_getfacl.rs`：新增 5 个测试。

## 验证
- Red：先只加测试，运行 `cargo test --test tests getfacl`，结果 4 failed / 6 passed（strip、warning once、root→`.`、`./` 这 4 个失败；`-p` 那个在修复前本来就能通过）。
- Green：同一条命令 10 passed。
- 全量（CI 对应的命令）：`cargo fmt --all -- --check` OK；`cargo clippy -- -D warnings` 和 `cargo clippy --all-targets -- -D warnings` 均无警告；`cargo test` 13 passed。
- 未运行：CI 中需要 root 或 GNU 对比的 job（如有）。

## 需要提交者注意
- 仓库没有 DCO 或 CLA 要求，也没有 CHANGELOG 或 PR 模板；commit 风格为 `<util>: <description>`，补丁已按这个风格写。
- 行为已对照 GNU acl v2.3.2 发布版 `tools/getfacl.c` 源码核实（审核时 2026-10-02）：去掉开头 `/`、只警告一次、去掉 `./`、空结果显示 `.`、警告措辞均一致；GNU 在判断 `opt_comments` 之前就做 strip，所以 `-c` 时也会打印警告，与本补丁一致。注：GNU acl 的 git master（未发布）已重写为只去 `/`，不再处理 `./` 和 `.`；如维护者以 master 为准可删掉这两点。

## 如何提交
```bash
git clone https://github.com/uutils/acl && cd acl
git checkout -b getfacl-absolute-names origin/main
git am /path/to/0001-getfacl-implement-absolute-names.patch
cargo fmt --all -- --check && cargo clippy -- -D warnings && cargo test
git push <your-fork> getfacl-absolute-names
gh pr create --repo uutils/acl --head anyingiit:getfacl-absolute-names --title "$(cat pr_title.txt)" --body-file pr_body.md
```
