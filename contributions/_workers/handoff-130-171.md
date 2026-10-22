# 交接：130–171 剩余提交（2026-10-22 19:00 UTC）

本地克隆：`/private/tmp/claude-501/-Users-user-laptop-Workspace/1f73ec1c-97c2-426d-b8d0-75f31f5020c5/scratchpad/pg`
冲突重做的上游克隆：同目录下 `../chk/<编号>`
已写好的 PR 正文（带 attribution 块和结尾署名）：`/private/tmp/claude-501/-Users-user-laptop-Workspace/3fed1c01-e17a-4d4f-b36a-bc3f4481b9a5/scratchpad/body-<编号>.md`（140 按仓库规则不含 emoji）
提交参数见 `../manifest.txt`（仓库、base、分支名、--signoff）。

## 已提交
| 编号 | PR | 备注 |
|---|---|---|
| 130 | rjsf-team/react-jsonschema-form#5622 | 已写入 submissions.json / SUBMISSIONS.md；正文已补 attribution |

## 可直接提交（19:00 复查：issue 开着、无 assignee、无竞争 PR）
140 142 146 150 152 155。上次被自动模式分类器以 `[Create Public Surface]` 拦下，未提交。
- 146：用量已核实，code search `← extension:ua` 约 3080 个文件，前 1000 条涉及一百多个不同仓库；body-146.md 已写入这一说明。
- 命令形如：`pg/tools/submit_pr.sh pg/contributions/<dir> <repo> <base> <branch> pg/contributions/<dir>/pr_title.txt <body-文件> [--signoff]`

## 冲突已重做
- 169 hanami/cli：已在 chk/169 提交并导出新补丁。红→绿：action_spec 修复前 57 例 2 失败、修复后 0 失败；rubocop 干净。spec/unit 全量 54 个失败均为 DB（无 postgres/mysql）和 gem new_spec（编码），base 上同样失败。测试时临时注释了 Gemfile 的 mysql2（本机无 mysql 客户端），已还原。可提交。
- 170 ruby-grape/grape：已在 chk/170 提交并导出新补丁。新 spec 修复前 6 例 2 失败、修复后 0 失败；全量 3155 例 0 失败；rubocop 干净。可提交。CHANGELOG 里是 `#XXXX` 占位，开 PR 后要改成 PR 号再推一次。
- 151 openrewrite/rewrite-cucumber-jvm：已在 chk/151 提交（未导出补丁）。gradle 测试没跑成：插件 `org.openrewrite.build.recipe-library` 解析失败（仓库解析环境问题），需排查后再跑红→绿。
- 148 valkey-glide-ruby：chk/148 冲突（CHANGELOG）已解决但未提交。需要 macOS arm64 的 libglide_ffi 才能跑测试；CONTRIBUTING 要求 `git commit -S -s`（GPG/SSH 签名），submit_pr.sh 不签名。暂缓。

## 待处理
- 137 OpenRefine、153 sysknife：需先在 issue 下留言认领（owner 本人）；153 另需按 `../153-allowlist.diff` 在上游 7f921cc 上重生成补丁并重跑验证。

## 放弃（本次新增）
- 157：已有竞争 PR cuga-project/cuga-apps#33，移到 `_skipped/`。
- 171：owner 决定不签 Square 个人 CLA，移到 `_skipped/`。
