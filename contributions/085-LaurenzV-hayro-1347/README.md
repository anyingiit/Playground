# LaurenzV/hayro #1347 — Stack overflow in Pdf::new on deeply nested arrays

| 项 | 值 |
|---|---|
| Issue | https://github.com/LaurenzV/hayro/issues/1347 |
| Tier | 新锐 |
| Labels | (none) |
| Status | ✅ ready — patch + PR text done |
| Duplicate-PR check | /pulls?q=1347 → 0 results；关键词 (depth/recursion/overflow) 搜索无针对本 issue 的 PR（#1301 resource limits 是解压/图像尺寸，不涉及嵌套）(2026-10-01)；issue 无 assignee、无评论 |
| Base | `master` @ febaff5 |
| Patch | `0001-hayro-syntax-Limit-nesting-depth-of-arrays-and-dicti.patch` |

## 问题理解
`hayro-syntax` 跳过数组/字典时递归 (`Array::skip`/`Dict::skip` → `Object::skip` → …) 且无深度上限，几千层 `[` 的 PDF 会让 `Pdf::new` 栈溢出直接 abort（不是 panic，`catch_unwind` 拦不住）。与 lopdf 的 RUSTSEC-2026-0187 同类。

另外发现第二条无界递归路径：`parse_dict_with` 在 key 位置遇到垃圾（如 `<< << << …`）时调用 `Object::read` → `Dict::read` → `parse_dict_with` …

## 合理性判断
安全/健壮性 bug，repo 已有大量同类 hardening PR（#347/#350/#1194 等），维护者明显欢迎。repo 内无 AI 政策（无 CONTRIBUTING/AGENTS.md，README 未提），issue 无标签。

## 改动
- `object/mod.rs`：新增 `MAX_NESTING_DEPTH = 256`、`skip_object(r, cs, depth)`、`skip_nested_value`（非 content stream 时先试 ObjRef）；`Object::skip` 委托给它。
- `object/array.rs` / `object/dict.rs`：新增 `skip_array` / `skip_dict` 带 depth，超限返回 None；trait impl 以 depth 0 调用。公共 trait 不变。
- `parse_dict_with` 垃圾 key 分支：`read::<Object>` → `skip::<Object>`（结果本来就被丢弃）。
- 测试：`pdf.rs` 4 个（数组/字典/垃圾字典 10 000 层 + 100 层正常解析），`array.rs` 1 个（256 ok / 257 拒绝）。

## 验证
- Red：在 master 源码（stash 掉 object/ 改动）上 `cargo test -p hayro-syntax --lib deeply_nested_arrays|deeply_nested_dicts|garbage` → 均 `has overflowed its stack`, SIGABRT；只修 skip 不改 parse_dict_with 时 garbage 测试仍溢出。
- Green：`cargo test -p hayro-syntax --lib nested` 全过；`cargo test -p hayro-syntax` 204 passed (含 nesting_depth_limit) / 2 failed（`pdf_version_header/catalog` 需要 `hayro-tests/downloads` 语料，未下载，与改动无关）。
- CI 的 `cargo test -p hayro-tests -- "load::"` → 112 passed。
- `cargo fmt --check --all` OK；`cargo clippy -p hayro-syntax --tests --examples`：仅 1 条已存在的 `xref.rs:460 sort_by_key`（本地 rustc 1.97 比 CI 的 1.92 新，jpeg2000 等也有新 lint，均为既有）；`cargo doc -p hayro-syntax --no-deps` -D warnings OK；`cargo check -p hayro-syntax --no-default-features [--features std|images|unsafe]` -D warnings OK。
- 未跑：thumbv6m no_std 目标（本机未装该 target；已用 --no-default-features 代替），完整渲染快照测试（需下载语料）。

## 需要提交者注意
- repo 无 DCO、无 AI trailer 要求，commit 未加 Signed-off-by / Assisted-by。
- commit 风格 `crate: Message`，已遵循。
- 256 这个上限是自选值（规范 Annex C 建议 28）；若维护者想要别的值改常量即可。
- 深层嵌套字典测试在 debug 下约 1–2 s（fallback xref 扫描在每个 `<<` 处 probe，复杂度 O(n·256)；修复前是 O(n²) 或直接溢出）。

## 如何提交
```bash
git clone https://github.com/LaurenzV/hayro && cd hayro
git checkout -b fix-nesting-depth master
git am /path/to/0001-hayro-syntax-Limit-nesting-depth-of-arrays-and-dicti.patch
# 或者直接：
tools/submit_pr.sh contributions/085-LaurenzV-hayro-1347 LaurenzV/hayro master fix-nesting-depth contributions/085-LaurenzV-hayro-1347/pr_title.txt contributions/085-LaurenzV-hayro-1347/pr_body.md
```
PR 标题/正文见 `pr_title.txt` / `pr_body.md`。
