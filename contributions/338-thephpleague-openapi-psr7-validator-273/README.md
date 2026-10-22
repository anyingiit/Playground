# thephpleague/openapi-psr7-validator#273: `format: byte` 遇到非法 Base64 抛 TypeError

| 项 | 值 |
|---|---|
| Issue | https://github.com/thephpleague/openapi-psr7-validator/issues/273 |
| Tier | 新锐（The PHP League 下的 OpenAPI PSR-7 校验库，~540★） |
| Labels | 无 |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 21:45 UTC：issue 无评论、无关联 PR、无 assignee；PR 列表第一页（到 2024-05）无 StringByte/base64 相关 PR |
| 活跃度 | 维护者 shadowhand 2026-05 连续合并 #266/#267/#272；有不少旧 PR 未处理 |
| AI 政策 | 仓库无 CONTRIBUTING，无 AI 条款 |
| Base | `master` @ b9ee232 |
| DCO / CLA | 都不需要 |
| 需先认领 | 否 |

## 问题理解
`base64_encode(base64_decode($value, true))`：严格模式下非法输入解码得 false，PHP 8 下 `base64_encode(false)` 在 strict_types 文件里抛 TypeError，整个校验崩掉而不是返回格式不符。

## 改动
- `src/Schema/TypeFormats/StringByte.php`：先解码，false 就返回 false，否则沿用原来的往返比较（同 StringDate 写法）。语义对合法输入不变（未补齐 padding 的输入仍按原逻辑判 false，没碰）。
- 新增 `tests/Schema/TypeFormats/StringByteTest.php`：仿 StringURITest 的 green/red data provider。
- 仓库无 CHANGELOG。

## 验证
- 绿：`vendor/bin/phpunit` 全量 → OK (438 tests, 519 assertions)；新测试 5 tests OK。
- 红：只回退 src → `%%%`、`U3=dhZ2dlcg=` 两例抛 TypeError。
- phpcs（Doctrine 标准，手动设 installed_paths）改动文件干净。PHPStan 2.3.1 phar level 6（无扩展）改动文件 No errors。

## 独立复核
- 修复：`StringByte` 先判 `base64_decode(..., true) === false` 再走原往返比较，写法同 `StringDate`，改动最小；合法输入走的路径与原来完全一致。`Type.php` 只有在 `is_string($data)` 时才会匹配到 string 格式，所以不需要 issue 里提的非字符串分支。其余格式里，`StringDate` 已有同样的判断；DateTime/Email/Hostname/IP/URI/UUID 的参数都是 `string`，内部不会把 false 传给类型严格的函数；Number* 只对已确认是数字的值做 `+ 0`。没有别处需要一起修。
- 红→绿（PHP 8.3.6）：全量 `OK (438 tests, 519 assertions)`，新测试 5 个全过。只回退 src 后，`%%%` 和 `U3=dhZ2dlcg=` 两例抛 `TypeError: base64_encode(): Argument #1 ($string) must be of type string, false given`，与 PR 描述一致。已经用 `git checkout` 恢复，工作区只剩原来就有的 composer.local.* 两个未跟踪文件。
- 风格：phpcs 退出码 0；PHPStan phar level 6 No errors。测试的写法和 StringURITest 一致：非静态 public data provider，带 `@return array<array<string>>`，用 green/red 命名。
- pr_body：数字（438/519、两个红例）属实，没有夸大；动机/披露段落在。正文里的 "Claude Code" 是披露段有意写的工具名，不是模型名；commit 和 patch 里都没有 AI 名称，也没有 Co-Authored-By。
- 身份：author/committer 都是 anyingiit <49945850+anyingiit@users.noreply.github.com>；master 仍在 b9ee232；patch 与 `git format-patch -1` 的输出逐字节一致。
- 本次复核没有改动任何东西。

结论：PASS
