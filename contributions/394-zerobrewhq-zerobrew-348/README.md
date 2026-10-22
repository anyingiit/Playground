# 394 — zerobrewhq/zerobrew#348 shim 提供 `MacOS`，并把缺失 API 的报错改成可读信息

| 项 | 值 |
|---|---|
| Issue | https://github.com/zerobrewhq/zerobrew/issues/348 |
| Tier | 新锐（Rust 写的 Homebrew 替代，两年内创建，增长快，测试全） |
| Labels | type: bug, area: install, area: formula resolution, priority: medium, status: accepted |
| Status | ✅ ready（patch + PR 文本就绪，未提交；独立复核 **PASS**，已采纳其建议） |
| 重复 PR 检查 | 2026-10-22 20:50 UTC：issue 无评论、无认领；Development 空；仓库仅 2 个开放 PR（我们的 #479、#466 man 命令），均无关 |
| AI 政策 | 无禁止 AI 规定 |
| Base | `main` @ c24141a |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
sketchybar 的 formula 调用 `MacOS.version`，shim 没有 `MacOS` 常量，构建直接抛 Ruby `NameError` 加整段 backtrace。issue 期望：给出包装后的用户可读错误，backtrace 只在 verbose/debug 下显示。

## 改动
- `shim.rb`：`MacOS = OS::Mac`（Homebrew os/mac.rb 的 `::MacOS = OS::Mac`）；`load FORMULA_FILE` 和 `instance.install` 外包 `rescue NameError`（含 NoMethodError），输出 “Error: <formula> uses `<name>`, which zerobrew can't build from source yet (<file>:<line>)” + Ruby 原消息；仅当 `ZEROBREW_BACKTRACE` 存在时打印 backtrace。
- `executor.rs`：`tracing::enabled!(INFO)`（即 `zb -v` 以上）时给 shim 设 `ZEROBREW_BACKTRACE=1`；测试 helper 增加 `run_shim_formula_with_env`；新增 6 个测试。
- CHANGELOG `[Unreleased] / Fixed` 两条。

## 验证
- 红：换回 main 的 shim.rb → 6 个新测试全部失败；绿：`build::` 29 个测试全过。
- `cargo test --workspace --no-fail-fast`：仅 4 个失败，与 baseline 相同（root 运行导致）。clippy `-D warnings`、fmt 干净。
- 独立复核 agent：VERDICT PASS；采纳：NoMethodError 只有接收者是 formula 或 shim 模块时才说“uses X”，其余报“formula failed”；行号改用 backtrace_locations（路径含冒号不出错）；补 class body 与 nil 方法两个测试；PR 正文说明 stderr 重复显示不在本 PR 范围。
- 手动：用 sketchybar 式 formula 跑 shim，输出见 pr_body。未在 macOS 上实测 sketchybar 完整构建。

## 需要提交者注意
- 与 393（同仓库）改的文件不同，可任意顺序提交，互不冲突。

## 如何提交
```
git clone https://github.com/zerobrewhq/zerobrew && cd zerobrew
git checkout -b shim-macos-and-name-errors origin/main
git am /path/to/0001-fix-zb_io-provide-MacOS-in-the-shim-and-name-the-API.patch
```
无 PR 模板；pr_body.md 已含披露段落。
