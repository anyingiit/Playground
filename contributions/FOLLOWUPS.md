# 已开 PR 的跟进（2026-10-22 22:00 UTC 起盘点）

本地提交员按行执行。"推补丁"= 在本地 fork 分支上 `git am <patch>` 后 `git push`（不 force）；"回复"= 把 reply.md 原文贴为 PR 评论（`gh pr comment <url> -F reply.md`）。做完在行尾标 ✅。

| PR | 文件夹 | 操作 | 说明 |
|---|---|---|---|
| [XAGI-Lab/melra#393](https://github.com/XAGI-Lab/melra/pull/393) | contributions/243-XAGI-Lab-melra-388 | 推补丁 `followup-0001-keep-help-out-of-read-scan.patch` 到 `anyingiit/melra:fix-help-env-vars`，再回复 reply.md | Bhavana Sanal CHANGES_REQUESTED 三点全改；红→绿（release.test.mjs 7/8→8/8），她的复现现在正确报错 ✅ 10-22 推送 dd1c457，已回复（release.test 8/8） |
| [git-ai-project/git-ai#2436](https://github.com/git-ai-project/git-ai/pull/2436) | contributions/204-git-ai-project-git-ai-1036 | 推补丁 `followup-0001-remove-dropped-array-table.patch` 到 `anyingiit/git-ai:fix/codex-toml-preserve-comments`，再回复 reply.md | svarlamov 问能否不加依赖：解释 toml_edit 只新增一个 crate，并提出可改；同时修 Devin 指出的卸载丢注释（红→绿，新测试） ✅ 10-22 推送 514bf18，已回复（lib codex 145、integration codex 64、clippy 干净） |
| [infection/infection#3699](https://github.com/infection/infection/pull/3699) | contributions/150-infection-infection-2582 | 推 `followup-0001-TEMP-escaped-mutant-demo.patch` 到 `anyingiit/infection:color-gha-diffs`，再回复 reply.md。**之后**等 theofidry 看过（或 CI 跑完后 1 天），再推 `followup-0002-revert-demo.patch` | theofidry：需加一个未杀死的变异才能看到效果。临时提交让 mt-annotations 打印彩色 diff（该 job 会故意变红） ✅ 10-22 改为不推演示提交：本地加 pcov 跑出彩色 diff（18 变异 1 逃逸），日志摘录已贴评论；0001/0002 均未推，除非 theofidry 要求看 CI |
| [getsentry/sentry-laravel#1204](https://github.com/getsentry/sentry-laravel/pull/1204) | contributions/118-getsentry-sentry-laravel-1070 | 推 `followup-0001-psr-reason-phrase.patch` 到该 PR 的 head 分支，再回复 reply.md。**推前请在本机跑** `vendor/bin/phpunit test/Sentry/Features/HttpClientResponseSerializerTest.php` | Cursor Bugbot：`reason()` 仅 Laravel ≥8.76 有，已核实 7.x 的 Response 无此方法；改用 `toPsrResponse()->getReasonPhrase()`。云端 composer 拉不到依赖，只做了 `php -l` ✅ 10-22 推送 3eef48c，已回复（phpunit 6 tests OK、php-cs-fixer/phpstan 干净；已核实 reason() 自 8.76 起才有） |
| [hrsh7th/nvim-cmp#2234](https://github.com/hrsh7th/nvim-cmp/pull/2234) | contributions/339-hrsh7th-nvim-cmp-2232 | 推 `followup-0001-col-offset-fit.patch` 到 `anyingiit/nvim-cmp:fix-2232-menu-clamp`，再回复 reply.md | Codex P2：适配检查未计入 col_offset。已用 nvim 0.11.4 headless 复现（修前 col=0，修后 col=7 贴右边）并新增 spec；vusted 未装，spec 本身未跑 ✅ 10-22 推送 68701b9，已回复（vusted 77/77，新 spec 红→绿，luacheck 0） |
| [bpmn-io/dmn-migrate#63](https://github.com/bpmn-io/dmn-migrate/pull/63) | contributions/432-bpmn-io-dmn-migrate-60 | 推 `followup-0001-all-namespace-prefixes.patch` 到 `anyingiit/dmn-migrate:migrate-imported-typerefs`，再回复 reply.md。CLA 仍待 owner 签 | Copilot 请求修改：同一命名空间多个前缀。红→绿（新测试，21 passing），eslint 通过 ✅ 10-22 推送 f27a1f1，已回复（mocha 21 passing；注意补丁文件把 CRLF 文件改成 LF，推送时已保留 CRLF）；CLA 仍待 owner 签 |
| [tuProlog/2p-kt#1046](https://github.com/tuProlog/2p-kt/pull/1046) | contributions/284-tuProlog-2p-kt-945 | 推 `followup-0001-kdoc-exception.patch` 到 `anyingiit/2p-kt:fix/945-theory-deobjectifier-errors`；回复 reply.md 可选 | Codex：KDoc 仍写 ClassCastException。纯文档 ✅ 10-22 推送 f9e27e8（仅 KDoc），未回复（提交信息已说明） |
| [ipython/ipython#15448](https://github.com/ipython/ipython/pull/15448) | contributions/091-ipython-ipython-12164 | 按顺序推 `followup-0001-TST-*.patch`、`followup-0002-Hold-back-*.patch` 到 `anyingiit/ipython:fix-system-interrupt-during-spawn`（两个提交，不 rebase），再回复 reply.md | Codex 3 条 P1 全处理：测试先提交且在断言上失败；^C 在 fork 后到达时子进程会被终止（红→绿，test_process 22 passed） ✅ 10-22 推送 e35f2f4、9bddbb8，已回复（test_process 22 passed） |

## 只需登记状态（无需操作）

| PR | 状态 |
|---|---|
| fadyehabamer/qr-zero#13 | ✅ 已合并（10-22） |
| uutils/acl#356 | ✅ 已合并（10-22，sylvestre） |
| hgrecco/pint#2517 | ✅ 已合并（10-22，andrewgsavage） |
| pyinstaller/pyinstaller#9555 | 已关闭（rokm：反对用 AI 做 good first issue）。不回复 |
| supercollider/supercollider#7812 | 已关闭（Spacechild1：good first issue 留给新人，维护者自己实现）。不回复 |
| decompme/decomp.me#2167 | 已关闭（mkst，无评论） |
| mochajs/mocha#6444 | 已被 bot 自动关闭并标 "spam: automated account"。不要再向 mocha 提 PR |
| rust-embedded/heapless#692 | sgued 批评"扔过墙的 PR"，zeenix 已批准；已 rebase，无需再回复 |
| zitadel/oidc#994 | 仍暂缓（维护者 10-02），无新动态 |
| go-git/go-git#2423 | 已按 pjbgf 要求 rebase 并回复，等复审 |

## 机器人提出、尚未处理（价值较低或需更多时间）

- jasonjmcghee/ron-lsp#28：Codex 多条 P1（src 路径推导、别名解析、嵌套类型元数据）。 ✅ 10-22 四条全修，推送 40de065 并回复（cargo test 75 通过）
- stackrox/kube-linter#1280：Codex 指出跳过的锚点。 ✅ 10-22 推送 c313b64（被忽略键下的锚点在首次别名处检查）并回复
- KnockOutEZ/wigolo#663：CodeRabbit 指出 CDP 存储状态未应用、池回退泄漏、认证上下文无上限。 ✅ 10-22 三条全修，推送 29afe80 并回复（vitest fetch 904 通过），PR 描述同步修正
- OpsiMate/OpsiMate#1293：CodeRabbit 建议空 PUT 测试也比较 updatedAt（小）。 ✅ 10-22 推送 5d0d238 并回复
- synolia/SyliusMaintenancePlugin#55、devonfw/IDEasy#2737、bpmn-io/dmn-migrate#63、bpmn-io/bpmn-to-image#70：CLA 待 owner 签。
