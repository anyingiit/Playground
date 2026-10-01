# rust-embedded/heapless #492 — `&mut LinearMap` should implement `IntoIterator`

| 项 | 值 |
|---|---|
| Issue | https://github.com/rust-embedded/heapless/issues/492 |
| Tier | 自由 |
| Labels | 无 |
| Status | ✅ ready — patch + PR text done |
| 重复 PR 检查 | /pulls?q=492 → 0 results；issue 无评论、无 assignee、无 cross-ref（2026-10-01 复查） |
| AI 政策 | 仓库内 grep 无 AI/LLM 规定；labels 无 human-only 描述；无 DCO 要求、无 AI trailer 要求 |
| Base | `main` @ a50891c (2026-09-15) |

## 问题理解
`&LinearMap` 实现了 `IntoIterator`，但 `&mut LinearMap` 没有，`for (k, v) in &mut map` 无法编译，虽然 `iter_mut()` 已存在。

## 合理性判断
纯增量 API，与 std `HashMap`/`BTreeMap` 行为一致，与已有的 `&LinearMapInner` impl 对称；master 上仍未实现。非 breaking。

## 改动
- `src/linear_map.rs`：新增 `impl<'a, K, V, S: LinearMapStorage<K, V> + ?Sized> IntoIterator for &'a mut LinearMapInner<K, V, S>`（`K: Eq`），返回现有 `IterMut`；同时覆盖 `LinearMap` 与 `LinearMapView`。
- 新测试 `linear_map::test::into_iter_mut`（同时测 `&mut LinearMap` 和 `&mut LinearMapView`）。
- `CHANGELOG.md` `[Unreleased]` 加一行（仓库有 changelog CI 检查）。

## 验证
- 红：仅加测试时 `cargo test --lib linear_map::test::into_iter_mut` → `error[E0277]: &mut LinearMapInner<..> is not an iterator`（2 处）。
- 绿：加 impl 后 `cargo test --lib linear_map` → 17 passed。
- `cargo test --lib` → 250 passed；`cargo test --doc --features alloc` → 197 passed。
- `cargo clippy --all-targets --features "alloc,defmt,portable-atomic-critical-section,serde,ufmt,bytes,zeroize,embedded-io-v0.7"`（host target，CI 用 i686-musl，本地未装该 target）→ 无 warning。
- `cargo fmt --all -- --check`（stable rustfmt；CI 用 nightly，本地无 nightly，改动不涉及注释/imports，预计无差异）→ clean。
- 未运行：cfail/cpass/tsan、嵌入式目标交叉编译、MSRV job。

## 需要提交者注意
- CI 的 fmt 用 nightly rustfmt，本地只用 stable 检查过。
- 仓库有 changelog 检查 workflow，已加 CHANGELOG 条目。
- 不需要 DCO / AI trailer。PR 正文已含 Claude Code 披露段落。

## 如何提交
```bash
git clone https://github.com/rust-embedded/heapless && cd heapless
git checkout -b linear-map-into-iter-mut origin/main
git am /path/to/0001-Implement-IntoIterator-for-mut-LinearMap.patch
```
或：
```bash
tools/submit_pr.sh contributions/508-rust-embedded-heapless-492 rust-embedded/heapless main linear-map-into-iter-mut contributions/508-rust-embedded-heapless-492/pr_title.txt contributions/508-rust-embedded-heapless-492/pr_body.md
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。
