# jj-vcs/jj#7816 — FR: Add `sparse()` function to fileset DSL

| 项 | 值 |
|---|---|
| Issue | https://github.com/jj-vcs/jj/issues/7816 |
| Tier | 高星 |
| Labels | good first issue, polish🪒🐃 |
| Status | ✅ ready — patch + PR text done (not submitted); independently re-reviewed 2026-10-01 |
| Base | `main` @ 0cb02a8 (2026-10-01) |
| Duplicate-PR check | 2026-10-01: issue open、未分配、0 条评论。`pulls?q=7816` 只有 #9614（Metbcy，"fileset: add `sparse()` function"），已于 2026-09-28 被作者本人以 "stale" 关闭、未合并；关键词 `sparse` 搜索其余 PR（#9760 fileset 化 sparse checkout 草稿、#9996 设计文档、#10246/#10221 等）均不实现 `sparse()` 函数，也不引用 #7816 |

## 问题理解

用户用 `jj sparse set --clear --add foo.txt` 只检出部分文件后，`jj log` 仍然显示大量只修改 sparse 范围外文件的提交。Issue 提议增加 fileset 函数 `sparse()`，表示“当前工作副本的 sparse patterns”，于是可以写 `jj log -r 'files(sparse())'`（或 issue 里的 `files(sparse()) | empty()`）只看与 sparse 范围相关的提交。

## 合理性判断

- 维护者标了 `good first issue` + `polish`，需求明确。
- 之前的 PR #9614 收到 yuja（核心维护者）的评审，没有否定功能本身，只建议“在 `WorkspaceCommandEnvironment::new()` 里加载 sparse patterns，而不是作为函数参数传递”；本补丁正是按该建议实现。该 PR 因作者自己清理队列而关闭，不是被拒。
- AI 政策：仓库无 AGENTS.md/CLAUDE.md；PR 模板里有两项 LLM 相关自查（“完全理解提交的代码，包括 LLM 起草的代码”、“LLM 生成的文字已校对”）→ 允许 AI 辅助，但要求提交者本人理解并校对。
- 正在进行的 #9760（草稿）计划把 sparse patterns 改为 fileset 表达式；本补丁只读取现有 `sparse_patterns()`（prefix 列表），与之不冲突，未来若 sparse patterns 变为 FilesetExpression，`sparse()` 可直接返回该表达式。

## 改动

- `lib/src/fileset.rs`
  - `FilesetParseContext` 新增 `sparse_patterns: Option<&'a [RepoPathBuf]>`。
  - 内置函数签名由 `&RepoPathUiConverter` 改为 `&FilesetParseContext`；`resolve_expression`/`resolve_function` 同步改为传 context。
  - 新函数 `sparse()`：无参数；`Some(patterns)` → 各 pattern 的 `prefix_path` 的并集（空列表 → `None`，默认 `.` → 根前缀即全部）；`None` → 报错 "Sparse patterns are not available in this context"。
  - 新单测 `test_parse_sparse_function`；其余 6 处测试 context 补 `sparse_patterns: None`。
- `lib/src/revset.rs`：`RevsetWorkspaceContext` 新增 `sparse_patterns`，`LoweringContext::fileset_parse_context()` 透传（`files(sparse())` 可用）。
- `cli/src/cli_util.rs`：`WorkspaceCommandEnvironment::new()` 通过 `workspace.working_copy().sparse_patterns().ok()` 加载一次；命令行参数的 fileset/revset 上下文传入；`fileset_parse_context_for_config()` 传 `None`（配置里的 fileset 用不了 `sparse()`）。
- `cli/src/commit_templater.rs`：模板 `diff(files)` 的 fileset 上下文从 revset workspace context 取 sparse patterns；测试构造补字段。
- `lib/tests/test_revset.rs`：构造补字段。
- `cli/tests/test_sparse_command.rs`：新 CLI 测试 `test_sparse_fileset_function`（`jj file list sparse()`、`jj log -r 'files(sparse())'` 过滤掉只改 bar.txt 的提交、`~sparse()`、空 patterns、`snapshot.auto-track='sparse()'` 报错）。
- `docs/filesets.md` 函数列表、`CHANGELOG.md` New features 各加一条。

## 验证

工具链：仓库 MSRV 为 1.97.1（testutils 要求），本机 stable 是 1.97.0，所以另装了 `rustup toolchain install 1.97.1 --profile minimal -c clippy -c rustfmt`；rustfmt 用 CI 同款 `nightly`。`CARGO_TARGET_DIR`/`CARGO_HOME` 都在 `/home/user/work/s2-1250` 下，`-j2`。

| 命令 | 结果 |
|---|---|
| **Red**：只保留新 CLI 测试（`git checkout -- lib/src cli/src lib/tests`），`cargo +1.97.1 test -j2 -p jj-cli --test runner -- test_sparse_fileset_function` | **FAILED**：parse 错误 ``Function `sparse` doesn't exist``（snapshot 不匹配，line 236）。新 lib 单测在无修复时因 `sparse_patterns` 字段不存在而无法编译 |
| **Green**：`cargo +1.97.1 test -j2 -p jj-cli --test runner -- test_sparse` | 3 passed |
| `cargo +1.97.1 test -j2 -p jj-lib --lib -- fileset revset` | 88 passed |
| `cargo +1.97.1 test -j2 -p jj-lib --test runner -- test_revset` | 78 passed |
| `cargo +1.97.1 test -j2 -p jj-cli --lib` | 250 passed |
| `cargo +1.97.1 test -j2 -p jj-cli --test runner -- --test-threads 3`（全部 CLI 集成测试） | 1132 passed, 0 failed |
| `cargo +nightly fmt --all -- --check` | clean |
| `cargo +1.97.1 clippy -j2 -p jj-lib -p jj-cli --all-targets -- -D warnings` | clean（CI 用 `--all-features --workspace`，此处未跑全部 feature） |
| 补丁在干净的 base（0cb02a8）上 `git am` | 成功 |

未运行：jj-lib 全量测试（只跑了 fileset/revset 单测与 test_revset 集成测试）、`--all-features` clippy、Windows/macOS CI。

## 需要提交者注意

- **Google CLA**：jj 要求签 Google CLA（https://cla.developers.google.com/），提交前确认已签。无 DCO/Signed-off-by 要求。
- **PR 模板里两个 LLM 自查框**（理解代码、校对 LLM 文字）在 `pr_body.md` 中**故意未勾选**——请你自己读过补丁和文字后再勾。
- jj 习惯：PR 描述可以很简短，主要信息在 commit message（已写，含 `Closes #7816`）；评审意见通过改写提交 + force-push 处理，而不是追加提交。
- 设计上的权衡（已在 PR 描述中说明）：本地工作副本的 `sparse_patterns()` 会加载整个 tree state，所以每个 workspace 命令会多一次 tree-state 读取（即使不用 `sparse()`）。这是按 yuja 在 #9614 的建议做的；若维护者在意，可改成惰性加载。
- 读取 sparse patterns 失败时静默降级为 `None`（`sparse()` 报 "not available in this context"），不会让其它命令失败。
- 错误信息措辞、函数名均可按评审调整；`snapshot.auto-track` 等配置中的 fileset 不支持 `sparse()`。

## 如何提交

```bash
git clone https://github.com/jj-vcs/jj && cd jj
git checkout -b fileset-sparse origin/main
git am /path/to/0001-fileset-add-sparse-function.patch
cargo test -p jj-cli --test runner -- test_sparse   # 可选复核
git push <your-fork> fileset-sparse   # PR 目标分支: main
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。

## 独立复核（2026-10-01）

在全新 depth-1 克隆（base 仍为 `0cb02a8`）上复核：`git am` 成功，作者为 `anyingiit <49945850+anyingiit@users.noreply.github.com>`，补丁中无 AI 模型名；
Red：回退非测试部分后 `test_sparse_fileset_function` 失败（``Function `sparse` doesn't exist``）；Green：`test_sparse*` 3 passed、`jj-lib --lib fileset` 31 passed（含 `test_parse_sparse_function`）、`jj-cli --lib` 250 passed、`test_fileset/test_file_/test_log` 86 passed；
`cargo +nightly fmt --all -- --check` 与 `cargo +1.97.1 clippy -p jj-lib -p jj-cli --all-targets -- -D warnings` 均 clean。
Issue 仍 open、无指派、无关联 PR；唯一实现同功能的 #9614 已关闭未合并。未做改动。
