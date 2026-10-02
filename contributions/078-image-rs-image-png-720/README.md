# image-rs/image-png#720: invalid cICP values make read_info() fail

| 项 | 值 |
|---|---|
| Issue | https://github.com/image-rs/image-png/issues/720 |
| Tier | 自由 (image-rs/image-png，Star 数 <5k) |
| Labels | 无 |
| Status | ✅ ready (patch + PR 文本已就绪，未提交) |
| 重复 PR 检查 | 2026-10-01：issue open、未指派、无评论；`/pulls?q=720` 无相关 PR；cICP 相关只有 #719 (encoder 端写 cICP/mDCV/cLLI，不改 decoder 的 `parse_cicp`)，不重复 |
| AI 政策 | 仓库内 md/CONTRIBUTING/labels 中均无 AI/LLM 限制 |
| Base | `master` @ b2f10c6 |

## 问题理解
`parse_cicp` 把 matrix_coefficients≠0、full-range flag∉{0,1}、多余尾字节都报成 `DecodingError::IoError(InvalidData)`。
`parse_chunk` 只把 `DecodingError::Format` 降级为 `BadAncillaryChunk`（跳过辅助块），所以 IoError 一路冒泡导致 `read_info()` 失败，违背 #525 的约定（辅助块错误不应致命）。

## 合理性判断
合理：cICP 是辅助块，同文件 sRGB/gAMA 等的值错误都用 `FormatErrorInner::*` 并被跳过；issue 附有可复现样例。

## 改动
- `src/decoder/stream.rs`：新增 `FormatErrorInner::InvalidCicpFullRangeFlag(u8)` 和 `InvalidCicpMatrixCoefficients(u8)`（含 Display）；`parse_cicp` 三处 IoError 改为 Format 错误（尾字节用 `ChunkLengthWrong { kind: cICP }`）。
- 新测试 `test_cicp_with_invalid_values_is_ignored`（3 种错误 payload，检查 read_info + next_frame 成功且 cicp 为 None）。
- `CHANGES.md`：Unreleased → Fixes 条目 + `[#720]` 链接。
- 未改 mDCV/cLLI/bKGD 中同类 IoError（PR 描述里作为 side note 提出）。

## 验证
- 红：修复前 `cargo test --lib cicp` → `read_info failed for cICP payload [9, 16, 1, 1]: invalid data`（FAILED）
- 绿：修复后 `cargo test --lib cicp` → 2 passed
- `cargo test --workspace --all-targets` → lib 102 passed / 1 ignored，其余 target 全过
- `cargo test --doc` → 8 passed
- `cargo check --tests --no-default-features` → OK
- `cargo fmt -- --check` → 干净（CI 没有 clippy）

## 需要提交者注意
- 仓库不要求 DCO，也不要求 AI trailer；commit 作者为 anyingiit (noreply 邮箱)。
- PR 描述含 AI 使用披露段。
- 如维护者希望一并处理 mDCV/cLLI，可再追加一个 commit。

## 如何提交
```
tools/submit_pr.sh contributions/078-image-rs-image-png-720 image-rs/image-png master fix-cicp-invalid-values contributions/078-image-rs-image-png-720/pr_title.txt contributions/078-image-rs-image-png-720/pr_body.md
```
（手动：fork → `git checkout -b fix-cicp-invalid-values origin/master` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR）
