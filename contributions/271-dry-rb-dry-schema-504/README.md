# dry-rb/dry-schema#504 — custom `constructor` on `Types::Nominal::Any` not called

| 项 | 值 |
|---|---|
| Issue | https://github.com/dry-rb/dry-schema/issues/504 |
| Tier | 自由（dry-rb，~420★，维护活跃度中等） |
| Labels | bug, help wanted |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 20:35 UTC：`repo:dry-rb/dry-schema 504` → 0；`is:pr any`、`is:pr constructor` 只有已合并/已关闭的旧 PR；open PR 仅 #518/#501/#458（无关）。issue 无评论、无 assignee |
| AI 政策 | CONTRIBUTING、.github、hanakai-rb/.github、labels 均无 AI 规定 |
| Base | `main` @ 4e19e0f |
| DCO / CLA / changeset | 无 DCO、无 CLA；CHANGELOG.md 手写条目（已加在 Unreleased/Fixed，署名 `(@anyingiit)`，开 PR 后可改成 `(@anyingiit in #<PR号>)`） |
| 需先认领 | 否（CONTRIBUTING 只要求 PR 对应已有 issue + 带测试） |

## 问题理解
`Types::Any.constructor { ... }` 单独传给 `value/filled/maybe` 时构造器不执行。原因：`Macros::DSL#extract_type_spec` 对这种类型推断不出谓词，`return self if predicates.empty?` 在 `type(resolved_type)` 之前提前返回，键的类型留在默认 Any。加约束后能推断出谓词，不走提前返回，所以 issue 里的第二种调用正常。

## 合理性
明显 bug；2019 年 07a12ed（"Fix handling of :any type spec"）时 `type()` 在提前返回之前，2020 年 bccab38 为 Sum 类型把 `type()` 挪到后面，造成回归。

## 改动
- `lib/dry/schema/macros/dsl.rb`：提前返回前 `type(resolved_type) if set_type`。
- `spec/integration/schema/type_spec.rb`：新增 "using a constructor type built on Any"。
- `CHANGELOG.md`：Unreleased/Fixed 加条目。

## 验证（Ruby 3.3.6）
- 红：去掉 lib 改动 → `bundle exec rspec spec/integration/schema/type_spec.rb` 20 examples, 1 failure（新测试）
- 绿：→ 20 examples, 0 failures
- 全量 `bundle exec rspec` → 3264 examples, 0 failures, 4 pending；`bundle exec rubocop` → 237 files, no offenses
- 手工：`value/filled/maybe/optional(..).value` 四种写法修复前都返回 "x"，修复后 "X"。

## 需要提交者注意
- 无 PR 模板，pr_body.md 用 chefs-pick 格式。
- PR 正文附带提到另一个发现（提前返回时 keyword 谓词/块也被丢弃，如 `value(:any, included_in?: [...])`），未修，留给维护者决定。

## 如何提交
```
tools/submit_pr.sh contributions/271-dry-rb-dry-schema-504 dry-rb/dry-schema main fix-any-constructor-type contributions/271-dry-rb-dry-schema-504/pr_title.txt contributions/271-dry-rb-dry-schema-504/pr_body.md
```

## 独立复核（2026-10-22 20:55 UTC，独立 agent）
- #504 仍 open、无 assignee/评论；open PR #520/#518/#501/#486/#458 均与此无关；`repo:dry-rb/dry-schema 504` → 0。
- 新浅克隆 `git am` 干净；红：只回退 dsl.rb → type_spec 20 ex / 1 failure；绿 → 0 failure；全量 3264 ex / 0 failures / 4 pending；rubocop 237 files no offenses。
- ~35 个手工用例对比：value/filled/maybe/optional、JSON/define、嵌套 hash/array 均修复；`T::Any.default` 现在会填默认值（与 String 一致）；Params 下 `maybe(:any)` 的 `""` 现在转为 nil（与 maybe(:string) 一致）——已补进 PR 正文。array/each 不受影响。
- 结论：PASS

## 注意：与 272 同改 CHANGELOG
272（同仓库 #455）也在 Unreleased/Fixed 加了一行。先提交哪个都行；第二个提交时 `git am --3way` 可能在 CHANGELOG 冲突，按两行都保留解决即可（或先 rebase 到最新 main 再导出补丁）。
