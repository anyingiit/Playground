# embedded-graphics/embedded-graphics#821 — ImageRaw::draw_sub_image 边界检查整数溢出

| 项 | 值 |
|---|---|
| Issue | https://github.com/embedded-graphics/embedded-graphics/issues/821 |
| Tier | 自由 (~1k stars, 维护中, 最近提交 2026-09-26) |
| Labels | 无 |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01: /pulls?q=821 无相关；?q=overflow 仅 #824 (thick line joints, 已合并, 无关)；issue 未分配、无评论 |
| AI 政策 | 仓库内 md / .github / labels 均无 AI/LLM 相关规定 |
| Base branch | `master` (基于 9c5bbcb) |

## 问题理解
`draw_sub_image` 的边界检查 `area.top_left.x as u32 + area.size.width > self.size.width` 在 area 很大时溢出：debug 下 panic，release 下回绕后通过检查，随后 `row_skip = data_width - width` 下溢，`ContiguousPixels` 参数错误（issue 所述 DoS / 越界读取）。

## 合理性判断
确凿的 bug（debug 下可直接复现 panic）。同类修复 #824（i32 溢出）刚被合并，维护者接受此类修复。

## 改动
- `src/image/image_raw.rs`：用 `checked_add(..).map_or(true, |r| r > size)`；溢出视为越界，不绘制（与其他越界 area 行为一致）。未用 `is_none_or`（1.82 才稳定，MSRV 1.81）。
- 新增测试 `draw_sub_image_with_overflowing_area`（宽/高溢出，含 x/y = i32::MAX）。
- `CHANGELOG.md` Unreleased → Fixed 增加条目。

## 验证
（`CARGO_TARGET_DIR` 在 /home/user/work/eg-target，stable cargo 1.97）
- 红：未修复时 `cargo test --lib image::image_raw` → `draw_sub_image_with_overflowing_area` FAILED（overflow panic at image_raw.rs:227）
- 绿：修复后 20 passed
- `cargo test --workspace`：全部通过（443 + 140 + 82 + 54 + …, 0 failed）
- `cargo fmt --all -- --check`：通过
- `cargo clippy --all-targets -- --deny=warnings`（CI 同款）：通过
- 未运行：`just check-drawing-examples / check-readmes / check-links`（需额外工具，且未改动示例/文档）、交叉编译 build-targets

## 需要提交者注意
- 无 DCO、无 AI trailer 要求；commit 作者为 anyingiit (noreply)。
- 仓库 PR 模板是 checklist + "PR description"，pr_body.md 已合并两者。
- CHANGELOG 惯例是链接 **PR 号**；当前条目链接的是 issue #821。开 PR 后建议把 `[#821](.../issues/821)` 改成 `[#<PR号>](.../pull/<PR号>)` 并 amend（或等维护者意见）。
- issue 以安全漏洞口吻撰写；PR 文本保持中性技术描述即可。

## 如何提交
```bash
git clone https://github.com/embedded-graphics/embedded-graphics && cd embedded-graphics
git checkout -b fix-draw-sub-image-overflow origin/master
git am /path/to/0001-Fix-integer-overflow-in-ImageRaw-draw_sub_image-boun.patch
```
或直接：
```bash
tools/submit_pr.sh contributions/067-embedded-graphics-embedded-graphics-821 embedded-graphics/embedded-graphics master fix-draw-sub-image-overflow contributions/067-embedded-graphics-embedded-graphics-821/pr_title.txt contributions/067-embedded-graphics-embedded-graphics-821/pr_body.md
```

## PR 文本
见 `pr_title.txt` / `pr_body.md`。
