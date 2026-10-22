# dry-rb/dry-validation#741 — nested filter failure stops sibling coercion（修在 dry-schema）

| 项 | 值 |
|---|---|
| Issue | https://github.com/dry-rb/dry-validation/issues/741 （PR 开在 **dry-rb/dry-schema**） |
| Tier | 自由（dry-rb） |
| Labels | bug, help wanted |
| Status | ✅ ready（复核 PASS，按建议补测试/改正文后重验，未提交） |
| 重复 PR 检查 | 2026-10-22 22:20 UTC：dry-validation 无 open PR；`org:dry-rb is:pr is:open 741` → 0；dry-schema open PR 无相关。issue 仅维护者 2025-06 一条"无法复现、请给版本"的评论，无 assignee |
| AI 政策 | 无（同 271） |
| Base | dry-schema `main` @ 4e19e0f |
| DCO / CLA / changeset | 无；CHANGELOG Unreleased/Fixed |
| 需先认领 | 否 |

## 问题理解
结果有错误时 `ValueCoercer` 逐个顶层键转换，`input.error?(name)` 对键下任意深度的错误都为真 → 嵌套 hash 里一个 filter 失败，整个 hash 都不转换。顶层同样写法只跳过失败的那个值。维护者在 dry-validation 里没复现，但直接在 dry-schema main 上能稳定复现（/home/user/work/r741.rb）。

## 改动
- `lib/dry/schema/value_coercer.rb`：错误就在该键本身 → 保持原值（原行为）；错误只在更深处 → 先转换整个值，再把各错误路径下的原始输入放回去（所以 filter 失败的值仍不被转换）。message_set 只编译一次。
- `spec/integration/schema/filter_spec.rb`：新增 "with keys in a nested hash"（2 例）+ "deeply nested"（1 例）。
- `CHANGELOG.md`。

## 验证（Ruby 3.3.6）
- 红：回退 lib → filter_spec 9 ex / 3 failures；绿 → 0 failures
- 全量 3266 ex / 0 failures / 4 pending；rubocop 无问题
- 手工（/home/user/work/r741c.rb、r741d.rb）：嵌套 hash + 数组 + 顶层组合；"must be a hash"/"must be an array" 键级错误保持原值；array 内 filter 在 main 上本就不生效（未改）。

## 需要提交者注意
- PR 开在 dry-schema，正文 `Fixes dry-rb/dry-validation#741`（跨仓库关联）。
- 与 271/272/273 同改 CHANGELOG，冲突时保留全部行。

## 如何提交
```
tools/submit_pr.sh contributions/274-dry-rb-dry-validation-741 dry-rb/dry-schema main fix-nested-filter-coercion contributions/274-dry-rb-dry-validation-741/pr_title.txt contributions/274-dry-rb-dry-validation-741/pr_body.md
```

## 独立复核（2026-10-22 23:10 UTC，独立 agent）
- #741 open、无 assignee/关联 PR；dry-validation 0 open PR；dry-schema open PR 中无相关（#521/#522 是我们的）。
- 新克隆 `git am` 干净；红 8/2 → 绿 8/0；全量 3265/0/4；rubocop 干净。
- 新旧对比：Params/JSON/define、字符串/符号/冻结输入、三层嵌套、数组兄弟、or 过滤器均按预期；键级错误、maybe(:hash) nil、改变类的 constructor、hash(Inner)、数组内 filter 均不变；不会改动调用方输入；50 键基准 83.6s → 43.7s。
- dry-validation main + 补丁版 dry-schema 跑 issue 原例：rule 收到 Date；dry-validation 全套 228/0/1。
- 建议：改正文"只在 dry-schema 复现"的措辞、补两层嵌套测试、说明 maybe(:hash) 限制 → 均已做。重验 filter_spec 9/0（回退 lib 9/3），全量 3266/0/4，rubocop 干净。
- 结论：PASS
