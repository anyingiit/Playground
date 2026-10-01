# GREsau/schemars#536 — tuple struct ignores `serde(default)` / `skip_serializing_if` in minItems

| 项 | 值 |
|---|---|
| Issue | https://github.com/GREsau/schemars/issues/536 |
| Tier | 自由 |
| Labels | (none) |
| Status | ✅ ready — patch + PR text done |
| 重复 PR 检查 | /pulls?q=536: 0 results; issue 无评论、无 assignee、无 linked PR (2026-10-01) |
| AI 政策 | 仓库无 CONTRIBUTING/AGENTS 等文件，grep LLM/AI/Copilot/Claude 无结果 → 未禁止 |

## 问题理解
`#[derive(JsonSchema)]` 对 tuple struct 总是输出 `minItems = 元素数`。但 serde 反序列化 tuple struct 时，
序列提前结束后，带 `#[serde(default)]`（字段级或容器级）的尾部字段会用默认值补齐，所以 `["abc"]` 对
`struct Skippy(String, #[serde(default)] u32)` 是合法输入，而 schema 拒绝它。

## 合理性判断
确认是 bug：serde_derive 1.0.229 `de.rs::expr_is_missing_seq` 在字段/容器有 default 时返回默认值，否则
`invalid_length(index)`；`check.rs::check_default_on_tuple` 保证 default 字段只能在尾部。命名结构体已对
default 字段做 required 处理，tuple struct 遗漏了。标题里的 `skip`：`skip_deserializing` 字段本来就从 de schema
中排除，加了组合测试确认；`skip_serializing_if` 在 serde_derive `ser.rs::serialize_tuple_struct_visitor` 中会让元素在序列化时被省略，ser schema 原来仍要求 minItems=元素数 → 一并修复（review 时补充）。

## 改动
`schemars_derive/src/schema_exprs.rs::expr_for_tuple_struct`：运行时维护 `min_len`；deserialize contract 下
只有无 default 的元素才计入 `min_len`；serialize contract 下只有无 `skip_serializing_if` 的元素才计入；`min_len == 0` 时不输出 `minItems`。
测试：`schemars/tests/integration/default.rs` 新增 4 个测试 + 8 个快照（de/ser）。

## 验证（Rust stable，/home/user/work/schemars）
- Red：只加测试，`cargo test --test integration default` → 3 个新测试失败
  （"deserialize schema should allow value accepted by deserialization: [\"abc\"]" / `[]`）。
- Review 复核：新 `skip_serializing_if_tuple_struct` 在无该部分修复时快照失败（ser minItems=2）。
- Green：加修复后 default:: 5/5 通过，integration 142/142 通过；原始提交时 `cargo test --all-features --no-fail-fast` 全部通过（当时 141 integration + 其它 suites + doctests），
  现有快照无变化。
- `cargo clippy --all-targets -- -D warnings` 和 `--all-features` 版本：干净。
- `cargo fmt --check`：仓库本身在当前 rustfmt 下有既有 diff（与本改动无关，CI 不跑 fmt）；改动的两个文件已 rustfmt 干净。

## 需要提交者注意
- 无 DCO、无 AI trailer 要求；commit 作者为 anyingiit (noreply 邮箱)。
- CHANGELOG 由维护者发版时写（无 Unreleased 节），未改动。
- 快照文件名带 `~`（仓库惯例），`git am` 能正常处理。

## 如何提交
```bash
git clone https://github.com/anyingiit/schemars && cd schemars   # 先在 GitHub 上 fork
git checkout -b fix-tuple-struct-default-min-items origin/master
git am /path/to/0001-Respect-serde-default-and-skip_serializing_if-in-tup.patch
# 或使用脚本：
tools/submit_pr.sh contributions/503-GREsau-schemars-536 GREsau/schemars master fix-tuple-struct-default-min-items contributions/503-GREsau-schemars-536/pr_title.txt contributions/503-GREsau-schemars-536/pr_body.md
```
PR 标题/正文：见 `pr_title.txt` / `pr_body.md`。
