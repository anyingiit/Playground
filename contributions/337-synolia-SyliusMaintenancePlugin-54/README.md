# synolia/SyliusMaintenancePlugin#54: 无匹配渠道的主机上 /_profiler、/_wdt 维护期间 500

| 项 | 值 |
|---|---|
| Issue | https://github.com/synolia/SyliusMaintenancePlugin/issues/54 |
| Tier | 自由（Synolia 的 Sylius 插件） |
| Labels | bug |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 21:20 UTC：issue 无评论、无关联 PR、无 assignee；仓库最近 PR 为 #53（2025-12），无竞争 PR |
| AI 政策 | CONTRIBUTING / .github 无 AI 条款 |
| Base | `main` @ 16fbb40 |
| DCO / CLA | 都不需要（历史提交无 Signed-off-by） |
| 需先认领 | 否 |
| PR 模板 | .github/PULL_REQUEST_TEMPLATE.md 的 Q/A 表已照填 |

## 问题理解
维护模式下，检查器按优先级依次跑：Enabled 100 → Ip/Bot 90 → Scheduled 80 → Admin 70 → Channel 60 → Profiler 30 → Token 20。多渠道时 ChannelChecker 调 `getChannel()`，主机名不匹配任何渠道就抛 `ChannelNotFoundException`，后面的 Profiler/Token 检查器跑不到，直接 500。

## 改动
- `src/Checker/ChannelChecker.php`：把原判断包进 try，catch `ChannelNotFoundException` 后返回 ACCESS_DENIED（交给后续检查器）。原逻辑不变。
- 新增 `tests/PHPUnit/Checker/ChannelCheckerTest.php`：3 个用例（不在维护的渠道→放行；在维护的渠道→不放行；无匹配渠道→不放行且不抛异常）。`count()` 不在接口上（仓库 phpstan.neon 也忽略了这一点），所以用 `addMethods(['count'])` mock。
- 选 issue 里的方案 2 而不是只调高 ProfilerChecker 优先级：方案 2 同时修好了 token 访问。

## 验证
- 绿：harness 里 `phpunit --bootstrap vendor/autoload.php tests/PHPUnit/Checker/` → OK (3 tests, 3 assertions)。
- 红：只回退 src → 无渠道用例报 ChannelNotFoundException，另 2 例通过。
- PHPStan 2.3.1 phar level max（仓库 ignore 规则，无 strict-rules 扩展）对改动文件 No errors；`php -l` 通过。
- 未跑：ECS（symplify 包只能 dist 下载，被拦）、仓库原有功能测试（需完整 Sylius 测试应用和数据库）。PR 正文已说明。

## 独立复核
- Issue #54 已读（WebFetch）：两种建议修法，补丁取方案 2（ChannelChecker 捕获 ChannelNotFoundException），与 issue 一致。
- 正确性：检查器优先级 Enabled 100 → Ip/Bot 90 → Scheduled 80 → Admin 70 → Channel 60 → Profiler 30 → Token 20；Voter 只在某检查器返回 ACCESS_GRANTED 时短路，ACCESS_DENIED 即“我不放行，交给下一个”，与原先单渠道分支返回值相同，所以无渠道时返回 ACCESS_DENIED 语义正确且保守（不会因主机不匹配而绕过维护）。`CachedPerRequestChannelContext` 会缓存并重抛首次查找的异常（issue 中栈指向 RequestLocaleSetter 正是此原因），补丁在 ChannelChecker 内捕获即可覆盖。请求路径上其余部分：EventSubscriber、其他检查器、maintenance.html.twig 均不调用渠道上下文，插件内不再有可抛该异常的位置。改动最小，只多一个 use 和 try/catch。
- 红→绿：打补丁 OK (3 tests, 3 assertions)；仅回退 src 后无渠道用例报 ChannelNotFoundException（2 过 1 错）；已恢复，工作树干净。PHPStan level max（仓库 ignore 规则）对两个文件 No errors。
- 风格：无变量 catch 与仓库 ConfigurationFileManager 写法一致（php ^8.2）；`git diff --check` 无空白问题。测试位于 tests/PHPUnit/Checker，命名空间 `Tests\Synolia\SyliusMaintenancePlugin\PHPUnit\Checker` 符合 autoload-dev；repo 用 phpunit ^9.5，`addMethods(['count'])` + `getMockForAbstractClass()` 对接口 mock 用法正确，且与 phpstan.neon 中对 count() 的忽略一致。
- PR 正文：模板 Q/A 表已填，表述与实测相符、无夸大，含动机/披露段（仅提及工具名 Claude Code，无模型名）。
- 提交身份 anyingiit <49945850+anyingiit@users.noreply.github.com>（author 与 committer 一致），提交信息无 AI 署名；包内 patch 与分支 HEAD 的 format-patch 输出逐字一致；main 仍在 16fbb40。
- 未作任何修改。

结论：PASS
