# 393 — zerobrewhq/zerobrew#414 把 keg 的 Frameworks 链接进 prefix

| 项 | 值 |
|---|---|
| Issue | https://github.com/zerobrewhq/zerobrew/issues/414 |
| Tier | 新锐（Rust 写的 Homebrew 替代，两年内创建，增长快，测试全） |
| Labels | status: accepted, priority: medium |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 **PASS**，已采纳其建议） |
| 重复 PR 检查 | 2026-10-22：issue 无认领；无相关开放 PR；sbin 部分已被维护者 commit 修好，Frameworks 部分仍缺 |
| AI 政策 | 无禁止 AI 规定 |
| Base | `main` @ c24141a |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
issue 指出 zerobrew 不链接 `sbin` 和 `Frameworks`。`sbin` 已在 main 修好；`Frameworks` 仍不在 `LINK_DIRS`，macOS 上 Python 的 framework build 不会出现在 `$PREFIX/Frameworks`。

## 改动
- `LINK_DIRS` 加 `Frameworks`；`dir_mode` 按 Homebrew `Keg#link` 规则：`[^/]*\.framework(/Versions)?$` 建真实目录（多 keg 共享），其余整体链接。
- `Linker::new` 不预建 `Frameworks`（大多数 prefix、所有 Linux 都用不到），首次链接时创建。
- 新测试 3 个；`zb_cli/tests/parity.rs` 目录清单加 `Frameworks`；CHANGELOG `[Unreleased] / Fixed` 加一条。
- 提交信息按 CONTRIBUTING 的 `fix($crate): …` 格式。

## 验证
- 红：回退 link.rs → `links_frameworks_the_way_homebrew_does` 失败；绿：34 个 link 测试全过。
- `cargo test --workspace --no-fail-fast`：仅 4 个失败，与 baseline（stash 后）完全相同，原因是以 root 运行（只读目录测试、installer 测试）。
- 独立复核 agent：VERDICT PASS（核对了 Homebrew keg.rb 的正则等价性、unlink、Linker::new 不预建目录的安全性）；采纳：补卸载后目录被清理的断言、补嵌套/边界识别用例、PR 正文说明两个 framework keg 冲突与 Homebrew 一致。
- clippy `-D warnings`、`fmt --check` 干净。未在 macOS 上用真实 bottle 测试。

## 如何提交
```
git clone https://github.com/zerobrewhq/zerobrew && cd zerobrew
git checkout -b link-frameworks origin/main
git am /path/to/0001-fix-zb_io-link-Frameworks-into-the-prefix.patch
```
无 PR 模板；pr_body.md 已含披露段落。
