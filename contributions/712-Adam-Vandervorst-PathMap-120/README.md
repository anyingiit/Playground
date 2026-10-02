# Adam-Vandervorst/PathMap #120 — to_prev iteration should be a thing

| 项 | 值 |
|---|---|
| Issue | https://github.com/Adam-Vandervorst/PathMap/issues/120 |
| Tier | 自由 |
| Labels | enhancement, good first issue |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue 仍 open，没有 assignee，也没有评论。`pulls?q=120` 只搜到无关的 #45（已合并），`pulls?q=to_prev` 只搜到 #111（修 `to_prev_sibling_byte`，已合并，与本 issue 无关）。master 上没有 `to_prev_step` / `to_prev_val`。 |
| Base | `master` @ ec818cf6（2026-09-27） |

## 问题理解
维护者 luketpeterson 在 issue 里要求：给 zipper 增加 `to_prev_step`、`to_prev_val`，与现有的 `to_next_step`、`to_next_val` 对称。第一版可以只做 trait 默认实现，同时补上 benchmark。他明确表示**不要**加 `to_prev_k_path` 和 `descend_last_k_path`，除非下游有需求。

## 合理性判断
- issue 由维护者本人提出，带 enhancement 和 good first issue 标签，范围也写清楚了，不需要先讨论设计。
- 仓库没有 CONTRIBUTING、AGENTS.md、CLAUDE.md 或 PR 模板，labels 描述里也没有 AI 相关限制，不需要 DCO，也没有 CHANGELOG。

## 改动
- `src/zipper.rs`
  - `ZipperMoving::to_prev_step` / `to_prev_step_observed`（默认实现）：
    - 当前位置有前一个兄弟节点时，移到该兄弟，再沿 `descend_last_byte` 一直下到叶子；
    - 没有前一个兄弟时，上移一个字节，回到 root 时返回 false；
    - 在 root 调用时，移到整棵 trie 的最后一个位置。
    - 遍历顺序正好是 `to_next_step` 的逆序，反复调用会循环。
  - `ZipperIteration::to_prev_val` / `to_prev_val_observed`（默认实现）：经过的位置与反复调用 `to_prev_step` 相同，但用 `descend_last_path_observed` 一次下到子树最后的叶子，比直接循环 `to_prev_step` 快约 1.8 倍。
  - `zipper_impl_lens!` 宏里把这两个方法转发给内部 zipper，做法与 `to_next_*` 相同。
  - 测试：`zipper_moving_tests!` 加 `to_prev_step_test1`，`zipper_iteration_tests!` 加 `zipper_prev_iter_test1/2`。这些宏覆盖所有 zipper 类型。
- `src/path_tracker.rs`：转发两个新方法，并同步更新 path buffer。
- `benches/{binary_keys,sparse_keys,superdense_keys}.rs`：各加一个 prev val bench 和一个 prev step bench，与已有的 forward bench 对应。
- `pathmap-book/src/1.02.05_zipper_iter.md`、`api_links.md`：补充文档。
- 没有改 `pathmap-derive`（PolyZipper derive）。它本来就不转发 `to_next_step`，派生出的类型会直接使用默认实现，测试里 poly_zipper 也全部通过。

## 验证（rustc/cargo 1.97.0，`CARGO_TARGET_DIR=/home/user/work/PathMap-target`，`-j2`）
- Red：把 `to_prev_step_observed` 和 `to_prev_val_observed` 的函数体改成直接 `false`，运行 `cargo test --release --lib prev`，结果 `22 passed; 28 failed`。失败的正好是所有 zipper 类型上的 28 个新测试，通过的 22 个是原有的 prev_sibling 测试。不打桩、直接删掉这两个方法时，测试无法编译。
- Green：`cargo test --release --lib prev` 结果 50 passed。加上 `--features arena_compact,random` 后结果 60 passed。
- 与 CI 相同的检查：
  - `cargo build --release --all-targets`：OK，改动的文件没有新增 warning
  - `cargo test --release`：lib 1058 passed，0 failed，1 ignored；integration 和 doc 测试都 OK
  - `cargo test --release --features arena_compact,random`：lib 1220 passed，0 failed；其余测试也 OK
  - `cargo doc --no-deps`：OK。唯一的 warning 在 `src/write_zipper.rs:201`，base 上已经存在
- Bench：`cargo bench --bench <b> -- prev`，三个 bench 都能运行。数据见 pr_body.md 的表格。反向 step 与正向基本相同；`to_prev_val` 比 `to_next_val` 慢，原因是正向走的是 native 的 `descend_first_byte` / `descend_until`。PR 正文已说明，后续可以补 native 实现。
- **独立复核（2026-10-01）**：在新的浅克隆（master @ ec818cf6）上 `git am` 能干净应用。Red/Green 结果一致（打桩后 22 passed / 28 failed，恢复后 50 passed）。CI 的四项检查（build all-targets、test、test arena_compact+random、doc）全部通过，数字与上面相同。另外用一个临时的随机 trie 测试（300 个 trie，未提交）确认：`to_prev_val` / `to_prev_step` 正好是 `to_next_*` 的逆序，从任意值调用 `to_prev_val` 都会落在前一个值上。复核时再次确认 issue 仍 open、没有 assignee、没有评论、没有相关 PR。
- **没有运行**：CI 的 fuzz/Lean differential job（需要 elan/Lean 工具链和 self-hosted runner），以及 CI 的 bench A/B 对比 job。

## 需要提交者注意
- 仓库没有 AI 政策、PR 模板和 CHANGELOG，也不需要 DCO。
- 本机 bench 数据有噪声（共享 4 核），PR 里只作参考，CI 的 bench A/B job 会给出正式对比。
- `pathmap-book/src/api_links.md` 里新链接用的是 `#method.`（默认方法在 docs.rs 上的锚点），原有条目用的是 `#tymethod.`，这是故意的，不是不一致。
- 如果维护者希望 PolyZipper derive 也显式转发 `to_prev_val`，需要改 `pathmap-derive`（独立发布的 crate），所以这次没做。

## 如何提交
```bash
git clone https://github.com/Adam-Vandervorst/PathMap && cd PathMap
git checkout -b to-prev-iteration origin/master
git am /home/user/Playground/contributions/712-Adam-Vandervorst-PathMap-120/0001-Add-to_prev_step-and-to_prev_val-iteration-methods.patch
cargo test --release && cargo test --release --features arena_compact,random
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/712-Adam-Vandervorst-PathMap-120 Adam-Vandervorst/PathMap master to-prev-iteration contributions/712-Adam-Vandervorst-PathMap-120/pr_title.txt contributions/712-Adam-Vandervorst-PathMap-120/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
