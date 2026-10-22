# hanami/hanami-cli#450 — `generate struct` should generate the app/slice base class if missing

| 项 | 值 |
|---|---|
| Issue | https://github.com/hanami/hanami-cli/issues/450 |
| Tier | 自由（hanami） |
| Labels | 无（维护者 timriley 自己开的待办） |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 20:15 UTC：issue 无评论/assignee/关联 PR；7 个 open PR 都不涉及 struct |
| AI 政策 | 无 |
| Base | `main` @ 47075b2 |
| DCO / CLA | 无 |
| 需先认领 | 否 |
| 注意 | owner 在此仓库已有 open PR #464，这是第二个，不要再投第三个 |

## 改动
`Generators::App::Struct#call` 在生成 struct 前，仿照 `Generators::App::Part`：
- app 的 `app/db/struct.rb` 不存在时创建（内容与 `hanami new` 的 `struct.erb` 逐字节一致，含 `require "hanami/db/struct"`）；
- slice 的 `slices/<slice>/db/struct.rb` 不存在时创建（参数与 `generate slice` 相同）。
已存在的不覆盖。CHANGELOG Unreleased/Added 加一行。

## 验证
- struct_spec 新增 4 个例子：11/0；回退 lib/ 后 2 个 "without base struct(s)" 失败。
- spec/unit 全量前后失败集合相同（均为本地无 MySQL/Postgres 的环境性失败）。
- RuboCop 改动文件无告警。

## 如何提交
```
tools/submit_pr.sh contributions/276-hanami-hanami-cli-450 hanami/hanami-cli main generate-base-struct contributions/276-hanami-hanami-cli-450/pr_title.txt contributions/276-hanami-hanami-cli-450/pr_body.md
```

## 独立复核（2026-10-22 ~20:40 UTC，独立 agent）
- 新克隆 `git am` 干净；红→绿、全量对比、rubocop 均复现。生成文件与 hanami new / generate slice 一致；app 判断用 APP_DIR（part.rb 用 base_path 是旧 bug，未照抄）。
- 建议：CHANGELOG 加引用号并用动词开头 → 已改；正文说明 hanami-db 未装的情况、以及在 slice 目录内运行时 APP_DIR 相对路径问题（与 generate part 相同）→ 已写入正文。结论：PASS
