# 交接：200–208 新贡献（2026-10-22 19:20 UTC）

来源：重新核实 `_workers/w1.md`、`w4.md`、`w6.md` 的 42 个候选，只有 9 个仍可做（其余已关闭、已有 PR、已分配或之前做过）。编号 200–208。

本会话开 PR 被本机自动模式拦截（Create Public Surface），所以停在"可提交"状态，等新会话（bypassPermissions）提交。

| # | Issue | 状态 | 提交命令要点 |
|---|---|---|---|
| 208 | image-rs/image-png#584 | ✅ 可提交，独立复核 PASS | base `master`；无 DCO/CLA |
| 202 | vega/altair#3502 | ✅ 可提交，独立复核 PASS | base `main`；无 DCO/CLA |
| 200 | plotly/plotly.py#2059 | ✅ 可提交，独立复核 PASS | base `main`；CHANGELOG 与 201 同位置，后提交的需 rebase |
| 201 | plotly/plotly.py#4040 | ✅ 可提交，独立复核 PASS-WITH-FIXES（收紧为只替换原有的长度错误） | base `main` |
| 204 | git-ai-project/git-ai#1036 | ✅ 可提交，独立复核 PASS | 见文件夹 README |
| 206 | stackrox/kube-linter#1194 | ✅ 可提交，独立复核 PASS（仅精简 PR 文本） | |
| 207 | arxanas/git-branchless#1308 | ✅ 可提交，独立复核 PASS | |
| 203 | we-promise/sure#3352 | 已跳过：本机无 Postgres/Redis，且需维护者决定 super admin 是否绕过账户共享 | |
| 205 | kubecolor/kubecolor#88 | 已跳过：维护者要求先做 #113 大重构，#234 因此被关 | |

提交方式：`WORKDIR=/tmp/pr-submit bash tools/submit_pr.sh $PWD/contributions/<folder> <owner/repo> <base> <branch> contributions/<folder>/pr_title.txt $PWD/contributions/<folder>/pr_body.md`。提交后把 PR 链接写进 `submissions.json` 和 `SUBMISSIONS.md`，并按 README 把 CHANGELOG 里的 issue 链接改成 PR 号（plotly）。

还在跑的实现/复核结果写在原会话的本地 Playground 克隆里，完成后会由原会话推送到本分支；新会话开工前先 `git pull`，只提交 README 里写明"独立复核 PASS"的文件夹。
