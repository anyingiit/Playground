# 交接：第二轮 088–129（2026-10-22 19:00 UTC）

## 已提交（共 18 个）
- 旧会话：089 NLog#6313、090 grpc-gateway#7562、091 ipython#15448、092 pyinstaller#9555、094 OpsiMate#1293、098 PathMap#167、100 phpmyadmin#20553、102 xterm.js#6253、103 compiler-explorer#9344（未在最新上游重跑测试，需看 CI）。
- 续接会话：096 decomp.me#2167、104 highlight.js#4564、108 pyhf#2777、114 hist#740、115 commitlint#5070、116 pylint#11717、120 ron-lsp#28、125 mocha#6444、129 logos#585（均已在最新上游跑过测试）。
- 125 mocha 需 owner 签 OpenJS EasyCLA，链接已发线程。

## 待提交
| # | 状态 | 要做的事 |
|---|---|---|
| 118 sentry-laravel | 补丁已在最新上游打好 | 本机没有 php/composer，测试没跑；validate-pr bot 要求先在 issue #1070 留言；维护者 10-08 说 #1196 收集数据太多，要更安全的版本，提交前确认补丁只序列化状态码/URL 等少量字段 |
| 121 supercollider | 补丁已打好 | 本机没有 sclang，没重跑测试 |
| 128 spec-kitty | 补丁已打好，mypy --strict 通过、新增 gate 测试通过 | 先在 issue #4292 留言认领，查有没有 fleet PR，开成 draft |
| 088 Surge | 补丁和上游冲突 | 解冲突（工作区有 10 个未完成文件） |
| 099 Kotlin dataframe | 冲突 | 解冲突（45 个文件），另 yunhwane 05-27 请求认领无 PR |
| 123 OpenRCT2 | 冲突，只在 NewsItem.cpp/ScPark.cpp 调用处 | 解冲突 |

## 放弃
- 106 repowise：冲突且已被认领。
- 119 ipfs-cluster：维护者反对无索引的服务端名字过滤，已移到 `_skipped`。
- 101 protobuf：已被 #30477 合入（之前已在 `_skipped`）。

## 本地路径
- 已应用补丁的克隆：`/private/tmp/claude-501/-Users-user-laptop-Workspace/489f4e0d-c399-4d37-99d4-9b381edfb2f0/scratchpad/r2/w/<folder>`
- 提交队列：同目录 `../list.txt`（编号 仓库 base 分支名；`-` 表示用 README 里 `checkout -b` 的名字）
- 带署名的 PR 正文：同目录 `../bodies/NNN.md`
- 提交脚本：`/private/tmp/claude-501/-Users-user-laptop-Workspace/03588dd0-eda0-43ad-a518-1da4b60eba60/scratchpad/sub.sh <NNN> [--draft]`（查重、rebase、推 fork、开 PR、加 assignee/reviewer；有其他人的 open PR 提到该 issue 时退出 3，确认无关后用 `KNOWN="<url>"` 放行）
