# samber/ro #74 — Operator(filtering): add "NotZero" operator

| 项目 | 内容 |
|---|---|
| Issue | https://github.com/samber/ro/issues/74 |
| Tier | 新锐 |
| Labels | core, good first issue, operator |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | `/pulls?q=74`、`/pulls?q=is:pr NotZero` 均无相关 PR；issue 未分配、无评论（2026-10-01）；代码里也没有 `NotZero` |
| Base | `main`（基于 2026-09-14 的 HEAD，#381 之后） |

## 问题理解
Issue 只有标题：在 filtering 类别新增 `NotZero` 操作符——只放行不是其类型零值的元素。

## 合理性判断
维护者自己开的 issue，带 `good first issue` / `operator` / `core` 标签；与 samber/lo 风格一致（`lo.Compact` 等）；核心包实现，无第三方依赖，合理。

## AI 政策
仓库自带 `AGENTS.md` / `CLAUDE.md`（给 Claude Code 的指南），docs/contributing、hacking 中无禁止 AI 的条款，无 DCO 要求，无 AI trailer 要求。

## 改动
- `operator_filter.go`：`func NotZero[T comparable]() func(Observable[T]) Observable[T]`，结构同 `Distinct`，`value != zero` 才 `NextWithContext`。
- `operator_filter_test.go`：`TestOperatorFilterNotZero`（int / string / struct / 指针 / 全零 / Empty / Throw）。
- `ro_example_test.go`：`ExampleNotZero_ok`、`ExampleNotZero_error`。
- `docs/data/core-notzero.md`（position 65，位于 DistinctBy 62 与 IgnoreElements 70 之间）、`docs/static/llms.txt` 一行。
- 按 docs/CLAUDE.md 要求同步 15 个 filtering 文档的 `sourceRef` 行号（脚本校验每个都指向对应 `func` 行）。

## 验证
- Red：先写测试，`go test -run TestOperatorFilterNotZero .` → `undefined: NotZero`（编译失败）。
- Green：`go test -race -run 'NotZero|Filter|Distinct|IgnoreElements' -v .` → PASS（含两个 Example）。
- `go test -race .`（根模块全量）→ `ok github.com/samber/ro 31.5s`。
- `golangci-lint run .`（v2.6.2，本机自带 v2.5.0 不认识 `modernize`）→ 0 issues。
- `headercheck --config ./licenses/headercheck.yaml .` → 仅 `plugins/exp/simd/*`、`bench/benchmark_test.go` 报错，均为既有文件，与本改动无关。
- `go vet .` 在 `operator_context.go` 报 lostcancel，base 上同样存在，非本改动引入。
- 未跑：plugins 各模块的 `make test`（本改动不触及插件）、docs 的 npm build。

## 需要提交者注意
- 没有 `// Play:` 链接（未发布的代码在 Playground 跑不了；空 `// Play:` 行会触发 godot lint），`playUrl` 留空。维护者可能会在发版后补。
- 维护者可能希望以 `Filter` 组合实现或更名（如 `Compact`）——按评审意见调整即可。
- 不需要 DCO / Signed-off-by，不需要 AI trailer。

## 如何提交
```bash
tools/submit_pr.sh contributions/081-samber-ro-74 samber/ro main feat/not-zero-operator contributions/081-samber-ro-74/pr_title.txt contributions/081-samber-ro-74/pr_body.md
```
或手动：fork → `git checkout -b feat/not-zero-operator origin/main` → `git am 0001-feat-filtering-add-NotZero-operator.patch` → push → 用 pr_title.txt / pr_body.md 开 PR。

## PR
- 标题：见 `pr_title.txt`
- 正文：见 `pr_body.md`
