# dry-rb/dry-schema#455 — incorrect key validation for schemas in `maybe(:array)`

| 项 | 值 |
|---|---|
| Issue | https://github.com/dry-rb/dry-schema/issues/455 |
| Tier | 自由（dry-rb） |
| Labels | bug, help wanted |
| Status | ✅ ready（复核 PASS，按复核意见修正测试后重验，未提交） |
| 重复 PR 检查 | 2026-10-22 20:50 UTC：repo open PR 只有 #520/#518/#501/#486/#458，均无关；`is:pr maybe` 只有已关闭/已合并的旧 PR。issue 只有 2023-07 一条给出 workaround 的评论，无 assignee、无关联 PR |
| AI 政策 | 无（同 271） |
| Base | `main` @ 4e19e0f |
| DCO / CLA / changeset | 无 DCO/CLA；CHANGELOG 手写条目（Unreleased/Fixed，`(@anyingiit)`，开 PR 后可补 `in #<PR号>`） |
| 需先认领 | 否 |

## 问题理解
`maybe(:array).each(NestedSchema)` 在 validate_keys 下把合法嵌套键报 "is not allowed"。根因：`Value#call` 和 `Schema#define` 只在当前类型是数组时把嵌套 schema 包成 array，`nil | array` 识别不出，键被改成 `nil | NestedSchema`（可选 hash），key map 变成 `{foo: [:bar]}`。同一错误类型还导致 Params 不转换/不清理嵌套键（issue 评论里的 "用 Params 可绕过" 只对类型检查成立，键其实没被转换）。

## 改动
- `lib/dry/schema/macros/value.rb`：新增 `maybe_array_type?`；当前类型为可选数组时构建 `array(schema)`，原有 maybe 分支再加 `optional`。
- `lib/dry/schema/macros/schema.rb`：`define` 对 `each { hash { ... } }` 块形式做同样处理（`each(:hash) { }` 在 main 上本来就正确）。
- `spec/integration/schema/macros/maybe_spec.rb`：两个新 context（validate_keys + key_map 断言，覆盖 `each(Schema)` 与 `each { hash {} }`；Params 键转换）。
- `CHANGELOG.md`。

## 验证（Ruby 3.3.6）
- 红：回退整个 lib → maybe_spec 22 ex / 4 failures（全是新测试）；只回退 schema.rb → 3 failures（块形式）
- 绿 → 22 ex / 0 failures；全量 3267 ex / 0 failures / 4 pending；rubocop 237 files no offenses
- 未修：`maybe(:array).each(...)` 遇 nil 抛 NoMethodError（main 同样），PR 正文已说明。

## 需要提交者注意
- 与 271（同仓库 #504）都改了 CHANGELOG 的 Unreleased/Fixed；第二个提交时 `git am --3way` 若冲突，两行都保留即可。

## 如何提交
```
tools/submit_pr.sh contributions/272-dry-rb-dry-schema-455 dry-rb/dry-schema main fix-maybe-array-each-schema contributions/272-dry-rb-dry-schema-455/pr_title.txt contributions/272-dry-rb-dry-schema-455/pr_body.md
```

## 独立复核（2026-10-22 21:20 UTC，独立 agent）
- #455 open、无 assignee/认领；open PR #520/#518/#501/#486/#458 均不重叠（#458 读过 diff）；`455` 搜 PR → 0。
- 新克隆 `git am` 干净；红→绿成立；全量 3266/0/4；rubocop 干净。新旧对比：define/Params/JSON、嵌套 maybe 数组、json_schema/info 输出均无回归；Params 下 `""` 现在得 `[]`（与 `maybe(:array).each(:integer)` 一致）。nil 抛 NoMethodError 的说法属实（main 同样）。
- 指出问题：原测试的 `each(:hash) {}` 在 main 上本来就对，schema.rb 改动无测试覆盖；PR/commit 措辞写错。→ 已改为 `each { hash {} }` 并加 key_map 断言，只回退 schema.rb 时 3 个用例失败；措辞已改；全量 3267/0/4、rubocop 干净。
- 结论：PASS（修正后）
