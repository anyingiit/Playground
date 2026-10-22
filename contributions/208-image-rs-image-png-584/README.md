# image-rs/image-png#584: encoder writes invalid PNG for too-large palette

| 项 | 值 |
|---|---|
| Issue | https://github.com/image-rs/image-png/issues/584 |
| Tier | 自由 (image-rs/image-png) |
| Labels | 无 |
| Status | ✅ ready (patch + PR 文本已就绪，未提交) |
| 重复 PR 检查 | 2026-10-22：issue open、未指派；评论只有 fintelia 建议 `assert!` + 邀请 PR、kornelski 提 RGBA palette 想法，无人认领；`gh pr list --search 584` / `palette` / `set_palette` 均无相关 PR（#702 是 decoder 端块顺序，不重复） |
| AI 政策 | 仓库 md/.github/CONTRIBUTING 无 AI/LLM 限制（与 078 一致） |
| Base | `master` @ b2f10c6 |
| DCO / CLA / changeset | 均不需要；有 `CHANGES.md`，已加条目 |

## 问题理解
`Encoder::set_palette` 不做任何检查，`encode_header` 直接写 PLTE。传入 1024 字节（RGBA 风格的 256×4）就写出 341.33 个条目的 PLTE，pngcheck 报错。规范要求 PLTE 为 1..=256 个 RGB 条目（长度为 3 的倍数，3..=768）。

## 合理性判断 / 行为选择
- fintelia（维护者）在 issue 里：“Seems reasonable to `assert!` that the provided palette doesn't exceed the maximum size … Want to make a PR?”——确认要拒绝而非截断。
- #611 (encoder 性能跟踪) 只把 #584 列为已知问题，没有说明行为。
- 选用 **返回 `EncodingError::Format` 错误** 而不是 panic：`set_palette` 无返回值，而 `write_header` → `Writer::init` 已对 ZeroWidth/InvalidColorCombination/Interlace 做同类校验并返回 Format 错误；`write_image_data` 对缺少 palette 也是返回 `NoPalette` 错误。PR 描述里说明了若维护者更想要 assert 可改。
- 未做截断（会静默改变用户数据）；未加 “palette 条目数 ≤ 2^bit_depth” 检查（规范是 shall-not，但范围超出 issue，保持最小）。

## 改动
- `src/encoder.rs`：新增私有 `FormatErrorKind::InvalidPaletteLength(usize)` + Display；`Writer::init` 中校验 `info.palette` 长度；`set_palette` 文档注明长度要求；新测试 `expect_error_on_invalid_palette_length`。
- `CHANGES.md`：Unreleased → Fixes 条目 + `[#584]` 链接。

## 验证（CARGO_TARGET_DIR 在工作目录）
- 红：修复前 `cargo test --lib invalid_palette_length` → `expected Format error for a palette of 0 bytes, got None` FAILED
- 绿：修复后同命令 → 1 passed
- `cargo test --workspace --all-targets` → lib 102 passed / 1 ignored，bugfixes/check_testimages/partial_decode/examples 全过
- `cargo test --doc` → 8 passed（注意：text_metadata 的 doctest 会写 `./target/text_chunk.png`，若设置了外部 CARGO_TARGET_DIR 需先 `mkdir target`，否则 base 上也会失败，与本改动无关）
- `cargo check --tests --no-default-features` → OK
- `cargo fmt -- --check` → 干净（CI 无 clippy）
- 未跑：powerpc cross 测试、MSRV 1.81 构建（改动只用了基础语法）

## 需要提交者注意
- 不需要 DCO/CLA；不需要 AI trailer；commit 作者为 anyingiit noreply 邮箱。
- PR 描述含 AI 披露段，并说明选了“返回错误”而非 issue 里提到的 `assert!`，维护者若要 panic 可改。
- 小发现（未改）：`Writer` 的 `Drop` 会在 `init` 失败后仍写入 IEND，所以错误时输出里会残留签名外的 IEND 字节；这是已有行为，测试只断言没有写出 PLTE。

## 如何提交
```
tools/submit_pr.sh contributions/208-image-rs-image-png-584 image-rs/image-png master reject-invalid-palette-length contributions/208-image-rs-image-png-584/pr_title.txt contributions/208-image-rs-image-png-584/pr_body.md
```
（手动：fork → `git checkout -b reject-invalid-palette-length origin/master` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR）

## 独立复核（2026-10-23）
- 上游复查：#584 仍 open、未指派，评论仍只有 fintelia/kornelski 两条；无相关 open/merged PR（#702 只改 decoder/stream.rs）。master 仍为 b2f10c6。
- 新浅克隆 + `git am` 干净应用，作者 anyingiit noreply。
- 红→绿：回退非测试改动后 `cargo test --lib invalid_palette_length` FAILED；恢复后 1 passed。
- `cargo fmt -- --check` 干净；`cargo test --workspace --all-targets` 全过（lib 102 passed / 1 ignored）；`cargo test --doc` 8 passed（已 `mkdir target`）；`cargo check --tests --no-default-features` OK；`cargo clippy --all-targets` 对 encoder.rs 无告警。
- 代码审阅：`encode_header` 对任意颜色类型只要有 palette 就写 PLTE，所以校验放在 `Writer::init` 对所有颜色类型生效是一致的；`with_info` 路径同样覆盖。PR 文本准确、有披露。无需修改。
- 结论：PASS
