# Euro-Office/eurooffice-nextcloud#151: config.php 中布尔型 verify_peer_off 被忽略

| 项 | 值 |
|---|---|
| Issue | https://github.com/Euro-Office/eurooffice-nextcloud/issues/151 |
| Tier | 新锐（Euro-Office 的 Nextcloud Office 连接器，2026 年新项目，维护活跃） |
| Labels | good first issue |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 20:15 UTC：23 个 open PR 无引用 #151 / verify_peer_off；issue 0 评论、无 assignee |
| AI 政策 | 仓库无 AI 限制条款（CHANGELOG 里有 @Copilot 的 PR 被合并） |
| Base | `main` @ efa7227 |
| DCO / CLA | 无（只有 release 工作流自己 signoff） |
| 需先认领 | 否 |
| 提交规范 | Conventional Commits（有 block-unconventional-commits 工作流），PR 标题即 commit 标题 |

## 改动
- `lib/AppConfig.php`：`getVerifyPeerOff()` 的 config.php 回退改用 `self::isTrue(...)`（issue 建议的一行修复）。
- 新增 `tests/unit/lib/AppConfigTest.php`（5 个数据集）。
- 副作用：config.php 里写 "yes"/"on"/"1" 现在也算 true，与 isTrue 的其他用法一致，PR 已说明。

## 验证
- 环境同 334。红：只回退 lib → "native bool true" 失败。绿：全量 40 tests OK。
- phpcs 与 php -l 干净。

## 需要提交者注意
- 与 334（#173）同仓库，互不冲突。

## 如何提交
```
tools/submit_pr.sh contributions/335-Euro-Office-eurooffice-nextcloud-151 Euro-Office/eurooffice-nextcloud main fix/151-verify-peer-off-bool contributions/335-Euro-Office-eurooffice-nextcloud-151/pr_title.txt contributions/335-Euro-Office-eurooffice-nextcloud-151/pr_body.md
```

## 独立复核（2026-10-22 20:24 UTC）
- Issue #151：WebFetch 确认 open、无 assignee、无评论、无关联 PR；GitHub 搜索 `151`/`verify_peer_off` 无相关 PR（仅命中无关的已关闭 #178），当前 8 个 open PR 均不相关。无竞争 PR。
- 从 main（efa7227）新建分支 `git am` 包内 patch：干净应用；作者正确；Conventional Commit 标题；无 AI 模型名。
- 全量测试：OK (40 tests, 84 assertions)。仅回退 lib/ → 只有 "native bool true" 数据集失败（40 tests, 1 failure），与声明一致。phpcs 与 php -l 干净。
- 代码：一行改动正是 issue 建议的修复；isTrue() 已被水印设置（AppConfig.php:977/999、SettingsController.php:236）使用，issue 正文称其由 #150 引入。管理面板保存值的分支（`$turnOff === "true"`，值来自 json_encode(bool)）未改动，PR 描述属实。
- 副作用：config.php 中 "yes"/"on"/"1"/"TRUE"、整数 1 现在也会关闭证书校验（之前只有字符串 "true"）。这些都需要管理员显式写入，语义上即“开启”，与 isTrue 在本仓库的其他用法一致，可接受；"false"/"0"/未设置仍为 false（测试覆盖了 false/"false"/未设置）。PR 正文已说明 "yes"/"on"/"1" 被接受。
- 测试质量：数据驱动 5 例，mock IAppConfig/IConfig 合理，命名空间与现有 tests/unit/lib 一致。
- PR 正文/README 数字核对：35→40 tests、84 assertions、失败数据集名称均与实测一致。
- 结论：PASS
