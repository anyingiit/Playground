# 390 — pydantic/monty#1101 `monty -` 从标准输入读程序

| 项 | 值 |
|---|---|
| Issue | https://github.com/pydantic/monty/issues/1101 |
| Tier | 新锐（2025 年创建，Pydantic 出品，增长快，测试完善） |
| Labels | 无 |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 **PASS**） |
| 重复 PR 检查 | 2026-10-22 20:20 UTC：pulls `is:pr stdin` 无相关开放 PR；issue 无评论、无 assignee、Development 为空；open PR 第一页无相关 |
| AI 政策 | 仓库自带 CLAUDE.md/AGENTS.md，项目本身面向 LLM 代码；无禁止 AI 规定 |
| Base | `main` @ 9ccbaff |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
`python -` 从 stdin 读程序；monty CLI 把 `-` 当文件路径，报 `reading -: No such file or directory`。issue 要求 `-` 读 stdin 并以脚本模式运行，保留其他 CLI 选项。

## 改动
- `crates/monty-runtime/src/run.rs`：文件分支里 `-` → `read_stdin()`，文件名用 `<stdin>`（与 `-c` 的 `<string>` 一致）。
- `src/main.rs` help 文案、`README.md`、`README-crate.md` 用法列表。
- 新增 `crates/monty-runtime/tests/cli.rs`：4 个测试（输出、traceback 名 `<stdin>`、资源限制选项生效、`-t -` 诊断名 `<stdin>`）。

## 验证
- 红：回退 src 改动 → 新测试全部失败；绿：全部通过
- `cargo test -p monty-runtime`：全过（101 + 7 + 4 等）
- `cargo clippy -p monty-runtime --tests --no-deps -- -D warnings` 干净（不加 `--no-deps` 时 `monty` lib 有一个 rust 1.97 clippy 的既有告警 `unnecessary_box_returns`，与本补丁无关）
- `cargo fmt --all -- --check`（stable）干净
- 独立复核 agent：VERDICT PASS；采纳了它的两条小建议（`-i` 文案提到 stdin、补 `-t -` 测试）

## 需要提交者注意
- 本仓库提交信息风格是普通句子 + `(#PR)`，无 Conventional Commits 要求。
- 仓库 PR 很多（94 open），维护者活跃合并外部 PR。

## 如何提交
```
git clone https://github.com/pydantic/monty && cd monty
git checkout -b cli-stdin-dash origin/main
git am /path/to/0001-Support-monty-to-read-the-program-from-standard-inpu.patch
```
PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。
