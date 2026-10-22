# dry-rb/dry-validation#750 — array of sum-of-hash-schema types not validated

| 项 | 值 |
|---|---|
| Issue | https://github.com/dry-rb/dry-validation/issues/750 （根因在 dry-rb/dry-schema） |
| Tier | 自由 |
| Status | ⏭️ skipped — 已有竞争 PR |
| 重复 PR 检查 | 2026-10-22 20:10 UTC：dry-schema 有 **open PR #458 "Support sum types of hashes in arrays"**（segiddins，2023-04-07，无评审、无维护者回复），做的正是这个修复 |

## 跳过原因
按 CONTRIBUTION_BRIEF 第 3 条（不重复）跳过。#458 虽已沉寂 3.5 年且未关联 #750，但内容相同。

## 已做的工作（供参考）
- 复现：`required(:things).array(Color | Book)` 编译成 `each(hash? OR hash?)`，丢掉两个 Hash schema 的键规则；`value(Color | Book)` 正常。
- 根因：`Macros::DSL#extract_type_spec` 只在 `set_type` 为真时（value/filled/maybe）展开 Sum/Intersection；`array`/`each` 传 `set_type: false`，于是走推断谓词分支。另外 `Core#new` 忽略 `klass:` 选项。
- `wip.diff`：在独立 DSL 上为 Sum/Intersection 两侧构建规则（不覆盖键类型），把 type_spec 交还给 Array 宏；新增 array/each 两个回归测试 + CHANGELOG。本地 3266 examples 全绿、rubocop 干净；去掉修复后 2 个新测试失败（红→绿成立）。
- 已知限制：Params 下 Sum 的嵌套键不做字符串→符号转换（`value(Sum)` 同样如此，key_map 不展开 Sum）。
- 可选：owner 若愿意，可在 #750 下评论指出 dry-schema#458 是对应修复、询问维护者是否愿意评审或接受更新版本。
