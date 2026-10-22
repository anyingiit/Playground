# dry-rb/dry-schema#468 — schema from struct reports errors on extra fields

| 项 | 值 |
|---|---|
| Issue | https://github.com/dry-rb/dry-schema/issues/468 （同时修复 #424，已验证） |
| Tier | 自由（dry-rb） |
| Labels | bug, help wanted |
| Status | ✅ ready（复核 PASS，按复核意见补测试/改正文后重验，未提交） |
| 重复 PR 检查 | 2026-10-22 21:50 UTC：open PR 仅 #521（我们的 271）/#520/#518/#501/#486/#458，均无关；`is:pr struct` 只有已合并旧 PR。issue 唯一回复是 flash-gordon 2023-09-11 说"看起来是 struct 里用 coercion 导致的"，之后无进展，无 assignee |
| AI 政策 | 无（同 271） |
| Base | `main` @ 4e19e0f |
| DCO / CLA / changeset | 无 DCO/CLA；CHANGELOG Unreleased/Fixed 条目 |
| 需先认领 | 否 |

## 问题理解
struct 扩展里 `Hash#call` 先用 struct 属性定义嵌套 schema（逐键类型、逐键 coercion），又额外 `type(types[name].constructor(schema))` 把整个 hash 先过一遍 struct 的 hash schema。后者全有或全无：任何一个属性失败就整体返回原值，其他属性都不被转换，于是合法的 42（Integer）被判 "must be a decimal"。

## 改动
- `lib/dry/schema/extensions/struct.rb`：删掉多余的 constructor 一行。
- `spec/extensions/struct_spec.rb`：新增 "struct with coercible attributes"（5 个用例：非法输入 2、array(struct)、maybe(struct) nil、合法输入）。
- `CHANGELOG.md`。

## 验证（Ruby 3.3.6）
- 红：回退 lib → `bundle exec rspec spec/extensions/struct_spec.rb` 13 ex / 4 failures；绿 → 0 failures
- 全量 3268 ex / 0 failures / 4 pending；rubocop 无问题
- 手工对比（/home/user/work/r468b.rb）：Params/define/JSON × value/hash/maybe/array，struct 含 transform_keys、attribute?、数组、嵌套 hash schema、默认值：合法输入输出不变；非法输入时其余属性现在被正确转换且不再误报。

## 如何提交
```
tools/submit_pr.sh contributions/273-dry-rb-dry-schema-468 dry-rb/dry-schema main fix-struct-partial-coercion contributions/273-dry-rb-dry-schema-468/pr_title.txt contributions/273-dry-rb-dry-schema-468/pr_body.md
```
注意：与 271/272 同改 CHANGELOG Unreleased/Fixed，`git am --3way` 冲突时保留全部行。

## 独立复核（2026-10-22 22:25 UTC，独立 agent）
- #468 open、无 assignee、无关联 PR；open PR 无相关；`468` 搜 PR → 0。
- 新克隆 `git am` 干净；红 11/2 → 绿 11/0；全量 3266/0/4；rubocop 干净。
- 大量新旧对比（Params/JSON/define × value/hash/maybe/array/each；嵌套 struct、transform_keys 含 camelCase proc、默认值、attribute?、constructor 包装、key_map/json_schema/info）：合法 hash 输入输出不变；变化全是修复：array(Struct) 合法可转换元素不再误报、maybe(Struct) 接受 nil、JSON/define 下 nil 报 "must be a hash"。
- 指出：PR 正文"合法输入输出不变"不准确 → 已按建议改写；建议补 array/maybe 两个测试 → 已补（回退 lib 时失败），CHANGELOG 同步补充。重验：struct_spec 13/0（回退 lib 13/4），全量 3268/0/4，rubocop 干净。
- 结论：PASS（修正后）

## 追加（22:55 UTC）：同时修复 #424
#424（struct 扩展下数组里一个元素非法导致合法元素也报错，2022 年起 open、无 PR）根因相同。main 上 `["m","1"]` 报 0 和 1，修复后只报 0。新增 "struct with an array of coercible values" 用例（回退 lib 时失败）；commit 和 PR 正文加 `Fixes #424`。重验：struct_spec 14/0（回退 lib 14/5），全量 3269/0/4，rubocop 干净。
