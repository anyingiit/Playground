# jam1garner/binrw#370 — Stream borrowed after a move

| 项 | 值 |
|---|---|
| Issue | https://github.com/jam1garner/binrw/issues/370 |
| Tier | 自由 |
| Labels | 无 |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01: /pulls?q=370 无结果; issue open、无指派、无评论、timeline 无关联 PR |
| AI 政策 | CONTRIBUTING.md / .github / labels 均无 AI 限制 |
| Base | `master` @ 585d481 |

## 问题理解
`#[binread] #[br(stream = reader)]` 用在**数据枚举**上时，顶层 prelude 生成 `let reader = __binrw_generated_var_reader;`（move 原 reader），但每个 variant 被转成独立的 `Struct` 生成代码，其 `stream_ident` 为 None，仍然引用原 reader 变量 → E0382。issue 里用 `count` 触发（其错误分支在闭包里调用 `stream_position`），实测普通字段的 variant 同样报错。

## 合理性判断
明确的编译错误 bug；结构体已有同类测试 `move_named_stream_with_count`，说明预期是支持的。

## 改动
- `binrw_derive/src/binrw/codegen/read_options/enum.rs`：`generate_variant_impl` 中若 variant 未指定 stream_ident，则继承枚举的 `stream_ident`。
- `binrw/tests/derive/enum.rs`：新增回归测试 `enum_named_stream_with_count`。
- 写入端（`#[bw(stream = w)]` 枚举）手动验证本来就正常，未改动。

## 验证（Rust 1.97.0 stable）
- Red：未修复时 `cargo test -p binrw --test derive enum_named_stream` → E0382 编译失败。
- Green：修复后同命令 1 passed。
- `cargo fmt -- --check` OK
- `cargo clippy --all-targets -- -D warnings`、`--all-features` 版本均无告警
- `cargo test`（workspace 全部）全部通过，0 failed
- 未运行：`cargo llvm-cov`（CI 覆盖率步骤）、nightly 下的 trybuild UI 测试。

## 需要提交者注意
- 仓库无 DCO、无 AI trailer 要求，commit 未加 Signed-off-by / Assisted-by。
- 仓库无 CHANGELOG 文件。
- CONTRIBUTING 建议改动前先在 issue 讨论；本 issue 已描述清楚，可直接提 PR，也可先在 issue 留言。
- PR body 含 AI 辅助披露段落。

## 如何提交
```bash
tools/submit_pr.sh contributions/509-jam1garner-binrw-370 jam1garner/binrw master fix-enum-stream-ident contributions/509-jam1garner-binrw-370/pr_title.txt contributions/509-jam1garner-binrw-370/pr_body.md
```
手动方式：fork 后 `git checkout -b fix-enum-stream-ident origin/master && git am 0001-*.patch && git push`，以 pr_title.txt / pr_body.md 开 PR。
