# oxc-project/oxc#684 — unicorn/prefer-math-abs（已跳过）

| 项 | 值 |
|---|---|
| Issue | https://github.com/oxc-project/oxc/issues/684 （☂️ eslint-plugin-unicorn 规则跟踪 issue） |
| Tier | 高星 |
| Labels | A-linter, E-Help Wanted, good first issue |
| Status | ⏭️ skipped — 维护者在跟踪表中把该规则标为 🚫（不打算实现） |
| 检查时间 | 2026-10-01 23:10 UTC，oxc `main` @ 36fb60f |

## 跳过原因

- #684 是一个跟踪 issue，正文表格的图例是 “✅ = Implemented, 🚫 = Not intending to implement, ⏳ = Fix pending”。
  在 recommended 规则表中，`unicorn/prefer-math-abs`（链接到 eslint-plugin-unicorn v76.0.0 文档）的状态一栏是 **🚫**，
  没有写原因（同表中还有约 44 条 🚫 规则，部分有原因、部分没有）。我分三次 WebFetch 该 issue，结果一致。
- 因此该规则不是“开放待认领”的工作，而是维护者明确决定不实现，按 brief 的“合理性判断”要求跳过。
- 补充：oxc 现有的 `unicorn/prefer-modern-math-apis`（`crates/oxc_linter/src/rules/unicorn/prefer_modern_math_apis.rs`）
  已经会对 `Math.sqrt(x ** 2)` 报 “Prefer `Math.abs(x)`”。上游新规则 prefer-math-abs 检查的是
  `x < 0 ? -x : x` 这类三元式和 `n > MAX || n < -MAX` 这类对称范围判断（只给 suggestion，不做 autofix，因为 `-0` 和类型转换有差异）。
  维护者可能认为收益低或与现有规则重叠，但表中没写原因。
- AI 政策（供参考）：CONTRIBUTING.md 的 “AI Usage Policy” 允许使用 AI，但要求披露；低质量 PR 会被关闭，反复提交者会被封禁。不是跳过原因。

## 需要提交者注意
- 如果确实想做这条规则，应先在 issue/Discord 询问维护者为什么标 🚫、是否接受实现，不要直接提 PR。
- 没有做任何代码改动，也没有生成 patch；没有运行仓库里的任何代码（只做了浅克隆和 grep，克隆已删除）。
