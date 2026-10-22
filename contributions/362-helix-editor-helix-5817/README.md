# helix-editor/helix#5817 — Ruby 的 ]a/[a 支持方法调用实参

| 项 | 值 |
|---|---|
| Issue | https://github.com/helix-editor/helix/issues/5817 |
| Tier | 高星（helix ~45k★） |
| Labels | A-language-support, C-enhancement |
| Status | ✅ 待提交（独立复核 PASS） |
| 重复 PR 检查 | 2026-10-22 21:00 UTC：`is:pr 5817` 0 条；`ruby textobjects` 只有已合并的 #2143、#4601（2022 年的旧改动）；issue 无 assignee、无关联 PR |
| AI 政策 | 无（同 360），正文含披露 |
| Base | `master` @ ba40e54 |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
issue：Ruby 里 `]a`/`[a` 只在 def 参数间跳，`super(...)` 等调用的实参不算参数。2024 年 pascalkuthe 把标题收窄成 Ruby。另一半建议（HTML/JSX 属性）已被标题排除，不做。

## 改动
- `runtime/queries/ruby/textobjects.scm`：加 `(argument_list ((_) @parameter.inside . ","? @parameter.around) @parameter.around)`，与 python/rust 的 arguments 写法一致；覆盖带括号调用、super(...)、不带括号的命令调用。
- `helix-term/tests/test/movement.rs`：新增集成测试（3 个用例）。

## 验证
- 只编译 ruby 语法放到 runtime/grammars（见 AUDIT）。
- 红：回退 query → `cargo integration-test -- ruby_call_arguments` FAILED（光标不动）；绿：ok（1 passed）。
- `cargo xtask query-check ruby` → Query check succeeded。
- 注意：选区是 `bar,`（around 含逗号）——与 rust/python 的 `]a` 行为一致（goto 用 around）。

## 如何提交
```
D=$PWD/contributions/362-helix-editor-helix-5817
tools/submit_pr.sh $D helix-editor/helix master ruby-argument-textobjects $D/pr_title.txt $D/pr_body.md
```

## 独立复核
**PASS**（独立 agent，干净克隆 ba40e54）：git am 干净；红（仅回退 .scm，光标不动）→绿；query-check ruby 通过；无竞争 PR（搜 5817 / ruby argument / ruby textobject）。
边界探测：`super(*a, **{..}.merge(opts))`、`foo(a: 1, &blk)`、嵌套调用、`puts *a, **h`、带块调用、`[a`、`mia`/`maa` 均正确；`def f(a, b)` 旧行为不变。
已采纳：PR 正文补充 yield/return/break/next 也用 argument_list；`ma`→`maa`；测试重命名为 `tree_sitter_motions_ruby_call_arguments`（重跑通过）。
