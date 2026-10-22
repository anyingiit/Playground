# phpmyadmin/motranslator#59: Translator::exists() 查不到复数条目

| 项 | 值 |
|---|---|
| Issue | https://github.com/phpmyadmin/motranslator/issues/59 |
| Tier | 自由（phpMyAdmin 组织下的 MO 翻译库） |
| Labels | bug, help wanted（维护者 williamdes 2026-10-12 加） |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 20:40 UTC：issue 无关联 PR、无 assignee；2 条评论（维护者要复现 + 报告者给复现），无人认领 |
| AI 政策 | CONTRIBUTING / .github 无 AI 条款 |
| Base | `master` @ 7536000（也可能希望 5.4.x/6.0.x，PR 里已说明可改） |
| DCO | 维护者提交都带 Signed-off-by；补丁 commit 已用 `-s` 签 anyingiit noreply（owner 规则允许代签） |
| CLA | 无 |
| 需先认领 | 否 |

## 问题理解
复数条目在缓存中的 key 是 `msgid . "\0" . msgid_plural`（ngettext 同款），`exists($msgid)` 只查单数 key，所以复数条目永远 false；报告者试的 `exampleexample+` 少了 NUL。

## 改动
- `src/Translator.php`：`exists(string $msgid, string|null $msgidPlural = null)`，给了复数就拼成同 ngettext 的 key；docblock 说明。
- `tests/MoFilesTest.php`：`testExistsWithPlural`（全部 .mo fixture）。
- 未改 CHANGELOG（条目引用 PR 号），PR 正文说明。
- 不做"只给单数也能查到复数"的方案：需要遍历缓存，ApcuCache 做不到，PR 正文说明。

## 验证
- 绿：`vendor/bin/phpunit --no-coverage` → 127 tests OK（21 skipped = APCu）。
- 红：只回退 src → 新测试 6 个数据集全失败。
- phpcs（PhpMyAdmin 规则）对改动文件干净。PHPStan 2.3.1 phar（无 phpstan 扩展）输出与 master 完全一致。
- 未跑：psalm（本机 PHP 版本不满足）。

## 如何提交
```
tools/submit_pr.sh contributions/336-phpmyadmin-motranslator-59 phpmyadmin/motranslator master exists-plural contributions/336-phpmyadmin-motranslator-59/pr_title.txt contributions/336-phpmyadmin-motranslator-59/pr_body.md --signoff
```

## 独立复核

- Issue：已通过网页读取 #59（报告者 `exists("event")` 对 msgid "event"/msgid_plural "event+" 返回 false；标签 bug、help wanted；无 assignee、无关联 PR），与补丁要解决的问题一致。GitHub API 在本会话不可用，只用网页读取。
- 正确性：`ngettext()` 用 `$msgid . "\u{0}" . $msgidPlural` 作 key 并调用 `cache->has()`，新的 `exists($msgid, $msgidPlural)` 拼出完全相同的 key。`InMemoryCache::has()` 是 `array_key_exists`；`ApcuCache::has()` 是对加前缀的 key 调用 `apcu_exists`（key 二进制安全，ngettext 本来就依赖这一点）。所以两种缓存对含 NUL 的 key 都有效。默认参数为 null，原有单参数调用的行为不变。
- 红→绿：在 fix-exists-plural 上运行 `vendor/bin/phpunit --no-coverage`，127 个测试通过（21 个跳过，都是 APCu，本机没有 apcu 扩展）。只回退 src/Translator.php 后，`testExistsWithPlural` 的 6 个数据集全部失败（Failures: 6）。复核完已还原，仓库仍在 fix-exists-plural 分支，工作区干净（只有未跟踪的 composer.local.*）。
- phpcs：全仓 `vendor/bin/phpcs` 干净。可空类型写成 `string|null`、docblock 参数对齐、`"\u{0}"` 写法都与仓库现有代码一致。
- pr_body：127/21/6 这几个数字都核对无误。CHANGELOG 条目确实引用 PR 号，所以 PR 里的说明属实。包含动机/披露段落。PHPStan 的结论未复跑（只看到 /tmp/phpstan 缓存残留），按原作者的记录采信。没发现夸大。
- 提交：作者和提交者都是 anyingiit <49945850+anyingiit@users.noreply.github.com>，带 Signed-off-by。包里的补丁与 `git format-patch -1` 的输出逐字节一致。全包 grep 没有模型名（只在披露段提到工具名 Claude Code，这是要求的）。
- 小提示（不阻塞）：`Translator` 不是 final。如果有下游子类覆写了 `exists(string $msgid)`，新签名会让它在 PHP 里报签名不兼容。这个影响很小，提交时可留意维护者是否在意，或者按 PR 里说的改投 6.0.x。
- 未改动任何包文件（本节除外）。

结论：PASS
