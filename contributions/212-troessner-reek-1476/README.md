# 212 — troessner/reek#1476: TooManyMethods 把嵌套 Struct 里的方法算进外层类

| 项 | 内容 |
|---|---|
| Issue | https://github.com/troessner/reek/issues/1476 |
| 层级 | 自由（Ruby，约 4k stars） |
| Labels | defect |
| Base 分支 | `master`（补丁基于 e8511a3） |
| 状态 | ✅ 可提交 |
| 重复检查 | 2026-10-22：无指派、无关联 PR；`/pulls?q=Struct` 无 open PR |
| AI 政策 | 无 AI 条款 |
| CLA/DCO | 无 |
| 与 211 关系 | 同仓库、改不同文件，可独立合入 |

## 问题理解
`Foo = Struct.new(:a) do def x; end end` 里的方法被算进外层类。维护者 mvz 2019 年确认是要修的 bug，2023 年 troessner 再次确认没修过。本地复现：max_methods 3 时外层类被报 5 个方法。

## 改动
`ModuleContext#node_instance_methods`：排除位于"定义模块的常量赋值"（`defines_module?`，即 `Struct.new` / `Class.new` / `Data.define`，与 ContextBuilder 判定一致）里的 def 节点；按 object_id 比较，避免误删外层同形方法。
- 第一版用 `local_nodes(:def, [:casgn])` 忽略所有常量赋值，独立复核指出会漏算 `X = class_eval do def..end`、`X = def foo; end`、`L = lambda do def..end` 等确实属于外层类的方法（假阴性），已改为只排除定义模块的常量赋值，并加用例。
- 改用 `defined_instance_methods` 会改变 `class << self` / `module_function` 计数，放弃。
- 嵌套迭代器写法触发 reek 自检 NestedIterators，改为 object_id 列表。
- `Module.new` 不在 reek 现有 `defines_module?` 范围内，维持现状（不在本 issue 范围）。

## 验证
- 新增 4 个 spec：Struct.new、Class.new（master 上失败→修复后通过）；非模块常量赋值仍计数；外层同形方法仍计数。
- 对照样例：含 `class << self`、`def self.x`、`module_function`、`private` 的类计数前后一致；`W = (def foo; @v; end)` 的 InstanceVariableAssumption 仍报。
- `bundle exec rake ci` exit 0：spec 1121/0、features 125 scenarios、rubocop 0、quality 134/0。

## 需要提交者注意
- CHANGELOG 发版时由维护者写，未改。
- 开着的 PR #1845（按可见性计数）也改 TooManyMethods 检测器；本补丁改的是 ModuleContext，应可共存。

## 如何提交
```
git clone https://github.com/troessner/reek && cd reek && git checkout -b too-many-methods-nested-struct origin/master
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22，两轮）
第一轮：指出初版忽略全部常量赋值会漏算（class_eval/begin/`X = def`/lambda 等），需修改。已按建议改为只排除 `defines_module?` 的常量赋值。
第二轮：`git am` 成功；`rake ci` 全绿（1121/125/0/134）；master 上 3 个新用例失败（Struct、Class.new、同形外层方法），非模块常量赋值用例在两边都通过（保持原行为）；第一轮所有回归样例恢复。结论：OK。
