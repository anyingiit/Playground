# vyncint/termlens#594: CLI panics (exit 101) on a closed stderr, a non-UTF-8 argument or a huge --timeout

| 项 | 值 |
|---|---|
| Issue | https://github.com/vyncint/termlens/issues/594 |
| Tier | 自由 |
| Labels | bug, good first issue |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 PASS，标题已按 ≤72 字符缩短） |
| 重复 PR 检查 | 2026-10-22 19:50 UTC：`repo:vyncint/termlens 594` → 0；issue 无评论、无 assignee、Development 为空 |
| AI 政策 | CONTRIBUTING §6：**欢迎 AI 协助，但禁止 AI 署名**——commit 不得有 AI Co-Authored-By、"Generated with" 脚注、机器人 emoji、bot 身份；CI（commit-policy.yml）强制检查。PR 正文也按此处理：**不要加 Generated 脚注 / 🤖 / 🙂 等 emoji**，披露段落是纯文字 |
| Base | `main` @ 06cd15d |
| DCO / CLA | **需要 DCO（CI 强制）**：commit 已带 `Signed-off-by: anyingiit <…noreply>`；无 CLA |
| 需先认领 | 否 |

## 问题理解
CLI 承诺退出码 0/1/2，但三种输入会 panic（101）：stderr 关闭或写满时 `eprintln!` panic；`std::env::args` 遇到非 UTF-8 参数 panic；`Instant::now() + --timeout` 在超大值时溢出（且在子进程已 spawn 之后）。另外 `render --out ""` 只打印文件系统报错，没有像 `--out=` 那样提示需要 PATH（#451）。

## 改动
- `crates/termlens-cli/src/main.rs`：`report()` 检查写入 stderr；`fail` 忽略写入失败但保持 exit 2；trailer 写不出 → exit 2；`args_os` + `utf8()`（自身选项/操作数非 UTF-8 → exit 2 并点名，inspect 运行的程序参数原样透传）；`timeout_secs` 用 `checked_add` 在 spawn 前拒绝；`--out ""` 报 `--out needs a PATH argument`。
- `crates/termlens/examples/inspect.rs`：同样修法，另外 `--help`/`--version` 在 `| true` 下不再 panic。
- `crates/termlens-cli/tests/cli.rs`：5 个新测试（closed stderr、/dev/full、非 UTF-8 参数、超大 timeout、`--out ""`）。
- `CHANGELOG.md`：`[Unreleased]` → `### Fixed`。

## 验证
- 红：只回退 main.rs/inspect.rs → 5 个新测试全失败（exit 101 / 文案不符）
- 绿：恢复后全过
- `cargo test --workspace` 全过；`cargo clippy --workspace --all-targets --all-features -D warnings` 干净；`cargo fmt --all --check` 干净
- `.github/scripts/check-dco.sh main..HEAD`、`check-no-ai-attribution.sh main..HEAD` 均 OK
- `tools/preflight.sh`：唯一失败的 `attribution-gate-selftest` 的 "bot author identity" 用例在**未改动的 main 上同样失败**（本机环境原因），与补丁无关；`cargo-semver-checks` 等未安装的 gate 跳过

## 如何提交
```
tools/submit_pr.sh contributions/245-vyncint-termlens-594 vyncint/termlens main fix-cli-no-panics contributions/245-vyncint-termlens-594/pr_title.txt contributions/245-vyncint-termlens-594/pr_body.md
```
（不要加 `--trailer`；patch 已签 DCO，`--reset-author` 后签名邮箱与作者一致。手动：fork → `git checkout -b fix-cli-no-panics origin/main` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR）

## 独立复核（2026-10-22 19:55 UTC）
- 新克隆 main@06cd15d，`git am` 干净；红（回退 main.rs/inspect.rs → 5 个新测试失败）→ 绿（49 passed）。
- fmt / clippy `-D warnings` / `cargo test --workspace`（含 `--all-features`）/ check-dco / check-no-ai-attribution / check-cli-contract 全过。
- 手工验证：非 UTF-8 程序参数透传 exit 0；`--out ""` 与 `--out=` 同文案；超大 `--timeout` 点名拒绝 exit 2；`--help >/dev/full`、`diff 2>/dev/full`、`inspect 2>/dev/full` 均 exit 2。
- 竞争 PR：无。
- 发现：标题 97 字符超过 CONTRIBUTING §4 的 72 上限 → 已改为 66 字符并重生成 patch；pr_body 补充了未跑 stress.yml / Windows clippy、以及非 UTF-8 路径改为 exit 2 拒绝的说明。
- 结论：修正后 PASS。
