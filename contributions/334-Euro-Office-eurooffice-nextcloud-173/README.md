# Euro-Office/eurooffice-nextcloud#173: users() 遇到已删除用户时 TypeError → 500

| 项 | 值 |
|---|---|
| Issue | https://github.com/Euro-Office/eurooffice-nextcloud/issues/173 |
| Tier | 新锐（Euro-Office 的 Nextcloud Office 连接器，2026 年新项目，维护活跃） |
| Labels | good first issue |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 20:15 UTC：23 个 open PR 无引用 #173 / filterUser；issue 0 评论、无 assignee |
| AI 政策 | 仓库无 AI 限制条款（CHANGELOG 里有 @Copilot 的 PR 被合并） |
| Base | `main` @ efa7227 |
| DCO / CLA | 无（只有 release 工作流自己 signoff） |
| 需先认领 | 否 |
| 提交规范 | Conventional Commits（有 block-unconventional-commits 工作流），PR 标题即 commit 标题 |

## 改动
- `lib/Controller/EditorController.php`：access list 与 group folder 两处 `userManager->get()` 结果为 null 时 `continue`。
- 新增 `tests/unit/lib/Controller/EditorControllerTest.php`。
- 其他调用点（EmailManager 已判空；EditorApiController 只传给 setVolatileActiveUser）不改，PR 正文已说明。

## 验证
- 环境：nextcloud/server stable34 + SQLite 安装 + app:enable eurooffice + server vendor-bin/phpunit，与 CI 相同。
- base：35 tests OK。红：只回退 lib → 新测试 TypeError。绿：36 tests OK。
- phpcs（ruleset.xml）与 php -l 干净。
- 未跑：stable33/35/36 矩阵、psalm（仓库尚未启用）。

## 需要提交者注意
- 与 335（#151）同仓库，互不冲突。

## 如何提交
```
tools/submit_pr.sh contributions/334-Euro-Office-eurooffice-nextcloud-173 Euro-Office/eurooffice-nextcloud main fix/173-users-null-user contributions/334-Euro-Office-eurooffice-nextcloud-173/pr_title.txt contributions/334-Euro-Office-eurooffice-nextcloud-173/pr_body.md
```

## 独立复核（2026-10-22 20:24 UTC）
- Issue #173：WebFetch 确认 open、无 assignee、无评论、Development 栏无关联 PR；GitHub 搜索 `173`/`filterUser` 只命中已关闭的 #170（issue 中明确说与本问题无关）、#178、#214，当前 8 个 open PR 均不相关。无竞争 PR。
- 从 main（efa7227）新建分支 `git am` 包内 patch：干净应用；作者 anyingiit <49945850+anyingiit@users.noreply.github.com>；标题符合 Conventional Commits（仓库有 block-unconventional-commits / conventional-commits 工作流）；commit 与 patch 中无 AI 模型名。
- 全量测试：OK (36 tests, 70 assertions)。仅回退 lib/ → 新测试报 `TypeError: ...filterUser(): Argument #1 ($user) must be of type OCP\IUser, null given`（36 tests, 1 error），红→绿成立。phpcs（ruleset.xml）与 php -l 均干净。
- 代码：两处 `continue` 正确且最小，保持 filterUser() 非空签名，与 issue 推荐的方案一致。EmailManager 第 70/82/119 行确已 `empty()` 判空；EditorApiController 只把 $user 传给接受 ?IUser 的 setVolatileActiveUser()——PR 正文描述属实。另有 issue 未列出的未判空点（Notifier.php:94、EditorController.php:532 sendNotify 中的 recipient），与本 issue 路径无关，保持不改合理，不需写入 PR。
- 测试：只覆盖 access list 分支，group folder 分支（需 GroupFolderStorage + folderManager）未覆盖，可接受。mock `OC\Files\Node\File` 有必要：getFileInfo() 只定义在 OC\Files\Node\Node，OCP\Files\File/Node 接口中没有，且 OC\Files\Node\File 非 final；PHPUnit 11 已不推荐 addMethods()，故无更干净的 OCP 写法，正文已说明原因。测试命名空间与现有测试一致。
- PR 正文/README 数字核对：35→36 tests、70 assertions、TypeError 文本均与实测一致。小瑕疵：README 中重复 PR 检查时间写作 20:30 UTC，略晚于实际时间（不影响提交）。
- 结论：PASS
