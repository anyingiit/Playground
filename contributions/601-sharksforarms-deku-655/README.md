# sharksforarms/deku#655 — id_pat 变体在 enum 使用 `id = "..."` 时首字段 ctx 未被写出

| 项 | 值 |
|---|---|
| Issue | https://github.com/sharksforarms/deku/issues/655 |
| Tier | 自由（~1.3k stars） |
| Labels | （无） |
| Status | ✅ ready — patch + PR 文案已完成 |
| 重复 PR 检查 | 2026-10-01：`/pulls?q=655` → 0 results；`/pulls?q=is:pr id_pat` → 只有已合并的旧 PR（#664/#544/#540/#534/#479/#454/#75），均无关；issue 无 assignee、无评论、无关联 PR |
| AI 政策 | 仓库无 AGENTS/CLAUDE/CONTRIBUTING；grep LLM/AI-generated/Copilot/ChatGPT 无命中；issue 无 label |

## 问题理解
enum 设置 `id = "..."`（通常来自 ctx）时 id 不从输入读取，`id_pat` 变体不存在 "id 存储字段"。
读端 (`deku_read.rs`) 只在 `id.is_none()` 时设置 `pad_id`，是正确的；写端 (`deku_write.rs`)
却对所有 `id_pat` 变体都把首字段当成 id 存储字段，用 enum 的 endian/bits/bytes 写出并丢掉字段自身属性：
- 首字段带 `ctx` → 编译错误（issue 中的 `expected u8, found ()`）
- 首字段带自己的 `endian` 等 → 静默写错字节

## 合理性判断
明确的 bug，读写不对称；上游 HEAD (1d3258a) 仍存在。issue 建议的改法（把 `f.ctx` 传进 id-storage 分支）
只能修编译错误，不能修第二种情况（已验证：测试仍失败 `[128,0,18,52]` vs `[128,0,52,18]`），因此采用与读端一致的条件。

## 改动
- `deku-derive/src/macros/deku_write.rs`：`emit_field_writes(..., variant.id_pat.is_some() && id.is_none(), ...)`
- `tests/test_attributes/test_ctx.rs`：新增 `test_enum_id_pat_ctx_id_first_field_attributes`
- `CHANGELOG.md`：`[Unreleased] / Fixed` 加一条

## 验证（rustc/cargo 1.97.0）
- RED：未修复时 `cargo test --test mod test_enum_id_pat_ctx` → `error[E0308]: mismatched types ... expected u8, found ()`
- 仅用 issue 建议改法：测试运行失败（字节序错）
- GREEN：修复后该测试通过
- `cargo fmt --all -- --check` ✅；`cargo clippy --all-targets -- -D warnings` ✅
- `cargo test --all` ✅（含 trybuild 110 个）；`cargo test --all-features` ✅；`cargo test --no-default-features --features=bits,alloc` ✅
- 未跑：CI 中其余 feature 组合、examples 循环、ensure_no_std / wasm 构建（与改动无关）

## 需要提交者注意
- 仓库不要求 DCO，也不要求 AI trailer；commit 作者 anyingiit（noreply 邮箱）。
- PR 描述中含 Claude Code 披露段落。
- CHANGELOG 条目链接的是 issue #655；如维护者习惯链 PR 号，可在提 PR 后改为 PR 链接。

## 如何提交
base 分支：`master`（检查：`git ls-remote --symref https://github.com/sharksforarms/deku HEAD`）

```bash
tools/submit_pr.sh contributions/601-sharksforarms-deku-655 sharksforarms/deku master fix-id-pat-ctx-id-write contributions/601-sharksforarms-deku-655/pr_title.txt contributions/601-sharksforarms-deku-655/pr_body.md
```
手动：fork → clone → `git checkout -b fix-id-pat-ctx-id-write` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR。
