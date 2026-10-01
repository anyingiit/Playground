# symfony/ai #2430 — [Platform] Nothing enforces that a new result type can become assistant content

| 项目 | 内容 |
|---|---|
| Status | ✅ ready — patch + PR 文本已完成，red→green 已验证（2026-10-01） |
| Issue | https://github.com/symfony/ai/issues/2430 |
| Tier | 新锐 |
| Labels | Bug, Platform, Status: Needs Review |
| 重复 PR 检查 | `github.com/symfony/ai/pulls?q=2430` 只有已合并的 #2382（引出此 issue 的 PR）；issue 无 assignee、无评论认领 → 无重复 |
| Base | `main` @ 9209a92 |

## 问题理解
新增 `Result\XResult` 时必须同时新增 `Message\Content\X` 和 `Message::toContent()` 分支，否则只有在应用代码调用 `Message::ofAssistant($result)` 时才抛异常；bridge 测试覆盖不到。issue 建议：marker interface 或"遍历所有 Result 类的 allow-list 测试"，放在 `Message::toContent()` 附近。

## 合理性判断
合理。当前 HEAD 上 `CustomToolCallResult` 已补了 `CustomToolCall` content 和映射（issue 中的具体缺口已修），但"强制机制"仍不存在，issue 仍 open，所以本 PR 只做强制测试。选测试方案（无 API 变更、最小改动）。

## 改动
新增 `src/platform/tests/Message/AssistantContentMappingTest.php`（仅测试）：
- 扫描 `src/Result/*.php` 中所有实现 `ResultInterface` 的非抽象类；
- 每个类必须出现在 data provider（含示例实例，跑 `Message::ofAssistant()` 必须成功）或 `NOT_ASSISTANT_CONTENT` 显式列表中（Batch/Choice/Job/Object/RealtimeSession/Reranking/Vector），且不能同时出现在两边。
- 不扫描 bridge 内的 Result 类（HuggingFace Output 等不是 assistant 消息内容；issue 只针对 `Result\` 命名空间）。

## 验证
- 新测试：`cd src/platform && vendor/bin/phpunit tests/Message/AssistantContentMappingTest.php` → OK (18 tests, 56 assertions)
- RED 1：删掉 `Message::toContent()` 中 `CustomToolCallResult` 分支 → Errors: 1（`Unsupported assistant message part of type "...CustomToolCallResult"`）；恢复后 GREEN。
- RED 2：临时新增 `src/Result/FooResult.php` → Failures: 1（`... is neither mapped to assistant content ... nor listed in NOT_ASSISTANT_CONTENT`）；删除后 GREEN。
  （本 PR 本身就是"检测器"，因此用这两种注入缺陷证明 red→green。）
- `cd src/platform && vendor/bin/phpunit tests` → OK (1072 tests, 2279 assertions, 2 skipped)
- `vendor/bin/php-cs-fixer fix --dry-run --diff <新文件>`（根目录）→ 0 个需修复
- `cd src/platform && vendor/bin/phpstan analyse tests/Message/AssistantContentMappingTest.php src/Message` → No errors
- 未运行：platform 全量 phpstan、各 bridge 测试（与改动无关）。
- 环境备注：api.github.com zipball 下载被代理 403，用 `--prefer-source` + 本地 path 仓库提供 phpstan/phpstan（2.3.x 分支）完成安装；未改动仓库文件。

## 需要提交者注意
- 仓库有 AGENTS.md（面向 AI agent 的指导），未禁止 AI 贡献；规则："Never add Claude as co-author in the commits" —— 补丁无任何 AI trailer/co-author，已遵守。无 DCO 要求。
- Symfony 惯例：PR 正文以 PR 模板表格（Bug fix?/New feature?/Issues: Fix #2430）开头，pr_body.md 已包含。
- 仅测试改动：changelog workflow 规定 bug fix/非 feature 不得改 CHANGELOG，故未加条目。
- Symfony 维护者可能偏好 marker interface 方案，PR 中已表示可改。
- 提交作者：anyingiit <49945850+anyingiit@users.noreply.github.com>。

## 如何提交
```bash
git clone https://github.com/symfony/ai && cd ai
git checkout -b platform-assistant-content-mapping-test origin/main
git am /path/to/contributions/250-symfony-ai-2430/0001-Platform-Guard-that-every-result-type-is-classified-.patch
git push <your-fork> platform-assistant-content-mapping-test
```
或者：
```bash
tools/submit_pr.sh contributions/250-symfony-ai-2430 symfony/ai main platform-assistant-content-mapping-test contributions/250-symfony-ai-2430/pr_title.txt contributions/250-symfony-ai-2430/pr_body.md
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。

## 独立复核（2026-10-01）
- issue #2430 仍 open、无 assignee/评论；`pulls?q=2430` 仅已合并的 #2382 → 无竞争 PR。
- 补丁在 main@9209a92 新浅克隆上 `git am` 干净应用；新测试 OK (18 tests, 56 assertions)。
- RED 复现：禁用 `CustomToolCallResult` 分支 → Errors: 1；新增 `Result\FooResult` → Failures: 1（"neither mapped…"）；恢复后 GREEN。`tests/Message` 全部通过。
- 符合 AGENTS.md（测试方法无 void、`$this->assert*`、无 AI co-author）。
- 修正：pr_body.md 去掉与模板重复的 "Related issue" 段和 n/a 的未勾选项，Checklist 改为 Verification。补丁未改动。
- 注：`git am`（无 `-k`）会去掉提交主题里的 `[Platform]` 前缀，对 Symfony（按 PR 标题合并）无影响。
