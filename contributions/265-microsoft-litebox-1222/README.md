# microsoft/litebox#1222 — Return null instead of panicking for over-max-order allocations

| 项目 | 内容 |
|---|---|
| Status | ✅ ready — 实现完成，red→green 已验证，fmt/clippy/doc/test 通过（2026-10-01） |
| Issue | https://github.com/microsoft/litebox/issues/1222 |
| Tier | 新锐 |
| Labels | 无（维护者 @wdcui 开的 follow-up issue，来自 #1219） |
| 重复 PR 检查 | 2026-10-01 检索 `/pulls?q=1222` 与 `allocator`：只有已合并的 #1219（前置修复）；无人认领/无评论，无重复 PR |
| Base | `main` @ 9b8d757 |

## 问题理解
`litebox/src/mm/allocator.rs` 中 `SafeZoneAllocator` 的 `LockedHeapWithRescue` rescue 回调在请求块大小的 order ≥ `ORDER` 时调用 `unimplemented!()` 直接 panic。这违反 `GlobalAlloc::alloc` 的契约（OOM 应返回 null），并使 `Vec::try_reserve` 之类可失败 API 无法报告错误。

## 合理性判断
Issue 由核心维护者提出，含明确验收标准（返回 null、try_reserve 返回 Err、正常功能不受影响、测试覆盖内存不足和超 order 两种情况），是 #1219 的后续，合理。

## 改动
- rescue 回调中超 order 时直接 `return`（不向 `MemoryProvider` 要内存），`LockedHeapWithRescue::alloc` 重试失败后返回 null。
- 文档注释说明超大请求返回 null。
- `mm::allocator` 单元测试 3 个：超 order 返回 null 且不调用 provider；最大 order 以内分配正常；provider 无内存时返回 null。
- 集成测试 `litebox/tests/safe_zone_allocator.rs`：把 `SafeZoneAllocator` 设为 `#[global_allocator]`，验证 `Vec::try_reserve_exact` 返回 `Err`。

## 验证（/home/user/work/litebox，cargo 1.97.0 stable）
- Red（还原 `unimplemented!()`）：`cargo test --locked -p litebox --lib mm::allocator` → `over_max_order_allocation_returns_null` FAILED（panicked at allocator.rs:68）；集成测试卡死（持有 spin lock 时 panic，panic 处理又分配内存 → 死锁），手动 kill。
- Green：`cargo test --locked -p litebox --lib mm::allocator` → 3 passed；`--test safe_zone_allocator` → 1 passed。
- `cargo fmt --check` OK；`cargo clippy --locked --all-targets --all-features -p litebox` 0 warning；`RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features --document-private-items -p litebox` OK。
- `cargo test --locked -p litebox -- --skip nine_p` → 110 + 1 + 3 doc 全通过。不加 skip 时 24 个 `fs::nine_p` 测试失败，原因是本环境没有 `diod`（`failed to start diod – is it installed?`），与本改动无关。
- 未运行：其他 crate（如 `litebox_platform_linux_kernel`，仅调用 `SafeZoneAllocator::new()`，API 未变）、nextest、Windows/LVBS/SNP CI 任务。

## 需要提交者注意
- 微软项目需签 CLA（CLA-bot 会在 PR 上提示，签一次即可）。不要求 DCO，无需 Signed-off-by。
- 仓库没有禁止 AI 的规定（有 `.github/copilot-instructions.md`，近期提交也含 Copilot co-author），无需 AI trailer；PR 正文已含 disclosure 段落。
- 无 PR 模板、无 CHANGELOG。
- 集成测试在“未修复”时会卡死而非失败——修复后不会出现，PR 正文已说明；如维护者不想要集成测试，可只保留单元测试。

## 如何提交
```bash
git clone https://github.com/microsoft/litebox && cd litebox
git checkout -b fix-over-order-alloc-null origin/main
git am /path/to/265-microsoft-litebox-1222/0001-Return-null-instead-of-panicking-for-over-max-order-.patch
cargo test --locked -p litebox -- --skip nine_p
# 推送到 fork 并开 PR：
tools/submit_pr.sh contributions/265-microsoft-litebox-1222 microsoft/litebox main fix-over-order-alloc-null contributions/265-microsoft-litebox-1222/pr_title.txt contributions/265-microsoft-litebox-1222/pr_body.md
```

PR 标题：见 `pr_title.txt`；PR 正文：见 `pr_body.md`。
