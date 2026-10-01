# orium/rpds#113 — HashTrieMap::new_with_degree(1) stack overflow

| 项 | 值 |
|---|---|
| Issue | https://github.com/orium/rpds/issues/113 |
| Tier | 自由（约 1.4k stars） |
| Labels | 无 |
| Status | ✅ ready |
| 重复 PR 检查 | 2026-10-01：/pulls?q=113、q=degree 均无相关 PR；issue open、未分配、无评论 |

## 问题理解
`new_with_hasher_and_degree_and_ptr_kind` 只断言 degree 是 2 的幂且 ≤ DEFAULT_DEGREE。1 是 2 的幂，
但 degree=1 时 `index_from_hash` 每层使用 0 位 hash（shift 恒为 0、mask 为 0），两个不同 key 永远分不开，
`insert` 无限递归导致栈溢出。

## 合理性判断
Issue 期望构造时拒绝 degree=1，与现有断言风格一致；修复极小且不影响其他 degree。仓库无 AI 政策（CONTRIBUTING、全仓 grep 无结果）。

## 改动
- `src/map/hash_trie_map/mod.rs`：增加 `assert!(degree >= 2, "degree must be at least 2")`（HashTrieSet 构造也经由此处）。
- `src/map/hash_trie_map/test.rs`：新增 `#[should_panic]` 回归测试 `test_new_with_degree_one_panics`。
- 提交信息风格与仓库一致（句子+句号）。

## 验证（RUSTFLAGS=-Dwarnings，rustc/cargo 1.97）
- red：未修复时 `cargo test --lib test_new_with_degree_one` → FAILED "test did not panic as expected"
- green：修复后 1 passed
- `cargo test --all-targets --all-features` 277 passed；`--no-default-features` 259 passed；`cargo test --doc --all-features` 29 passed
- `cargo fmt -- --check`、`cargo clippy --all-targets -- -D warnings`、`cargo doc --no-deps --all-features` 均通过
- 未运行：`cargo hack`（未安装，已分别跑 all/no-default features 替代）、`cargo msrv verify`、`cargo rdme --check`（未改文档）、bench

## 需要提交者注意
- 仓库不要求 DCO，也无 AI trailer 要求，commit 中未加任何 trailer。
- 未更新 `release-notes.md`（维护者似乎在发版时统一写，当前版本 1.2.2-pre 尚无条目）；PR 里表示可按需补充。
- PR 描述含 AI 辅助披露段落。

## 如何提交
基于 `main`：
```
tools/submit_pr.sh contributions/617-orium-rpds-113 orium/rpds main fix-hash-trie-map-degree-one contributions/617-orium-rpds-113/pr_title.txt contributions/617-orium-rpds-113/pr_body.md
```
（手动：fork → `git checkout -b fix-hash-trie-map-degree-one origin/main && git am 0001-*.patch` → push → 开 PR，标题/正文见 pr_title.txt / pr_body.md）
