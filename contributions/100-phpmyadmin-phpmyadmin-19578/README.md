# phpmyadmin/phpmyadmin #19578 — After creating an event/procedure the shown query is missing `DELIMITER $$`

| 项 | 值 |
|---|---|
| Issue | https://github.com/phpmyadmin/phpmyadmin/issues/19578 |
| Tier | 高星 |
| Labels | Bug, help wanted |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue open、无人分配、无评论认领，页面无关联 PR。`pulls?q=19578` 只有 #19942（M393，已合并到 QA_5_2），它只修了 trigger 导出（#17285），作者在 PR 里明确说没有修 #19578。`is:pr DELIMITER` 搜索没有其他相关 open/merged PR。 |
| Base | `QA_5_2` @ 8dfc3dbf（2026-09-30）；bug 修复按 PR 模板走 QA 分支，#19942 同样合并到 QA_5_2 |

## 问题理解
用编辑器对话框新建或修改 procedure/function、event、trigger 后，成功提示里显示执行过的 SQL，但没有 `DELIMITER $$ ... $$ DELIMITER ;`。如果 body 里有 `;`（`BEGIN ...; ...; END`），把这条 SQL 复制到 SQL 页或 mysql 客户端，或者点提示里的 Edit / Edit inline 再执行，都会失败：第一个 `;` 就把语句截断了。只有显示有问题，发给服务器的查询本身没有问题。

## 合理性判断
- issue 带 Bug + help wanted 标签，无人分配，没有 PR。#19942（已合并到 QA_5_2）只修了 trigger 导出（#17285），PR 作者明确说没有覆盖 #19578。
- 仓库里已有同样的写法：RoutinesController/Triggers 导出用的是 `"DELIMITER $$\n" . $def . "$$\nDELIMITER ;\n"`，`LintController` 也以 `DELIMITER $$` 开头。本次改动沿用这个格式。
- `Generator::getMessage()` 不在服务端解析查询（`formatSql` 只做 htmlspecialchars，高亮由前端 CodeMirror 完成）。Edit 链接把整段 SQL 带到 SQL 页，导入流程支持 `DELIMITER`，所以现在可以直接重新执行。
- 修改模式下，查询是 `DROP ... ;` 加上 CREATE。DROP 放在 `DELIMITER $$` 那一行**之前**，仍然以普通的 `;` 结束；如果放进 `$$` 块里，就会和 CREATE 合并成一条语句。
- 基于 QA_5_2：PR 模板规定已发布版本的 bug 修复走 QA 分支。master 上对应的代码在 `src/Database/{Events,Routines}.php` 和 `src/Triggers/Triggers.php`，由维护者自己合并到 master。

## 改动（commit e91b72f，基于 QA_5_2 @ 8dfc3dbf）
- `libraries/classes/Util.php`：新增 `Util::getQueryWithDelimiter(string $query): string`，返回 `"DELIMITER $$\n" . $query . "$$\nDELIMITER ;\n"`。
- `libraries/classes/Database/{Routines,Events,Triggers}.php`：传给 `Generator::getMessage()` 的 `$sql_query` 改为 `Util::getQueryWithDelimiter($query)`（新建模式），以及 `$drop . Util::getQueryWithDelimiter($query)`（修改模式）。每个文件改 2 行。
- `test/classes/UtilTest.php`：新增 `testGetQueryWithDelimiter`。它检查输出字符串；用 sql-parser 解析后，新建形式是 1 条 CreateStatement、0 个错误，修改形式（DROP + 包裹后的 CREATE）是 DropStatement + CreateStatement、0 个错误。作为对照，不加 DELIMITER 的原始查询会被 parser 拆成 2 条语句并报 1 个错误。
- `ChangeLog`：在 5.2.4 (not yet released) 下加了一行 `- issue #19578 Fix missing DELIMITER in the query shown after creating or editing a routine, event or trigger`。

为什么用 helper，而不是直接测 handleEditor：QA_5_2 上显示 SQL 的路径只有 AJAX 分支，而 AJAX 分支最后都会调用 `exit`；非 AJAX 分支会直接丢弃 `$output`。所以 phpunit 没法直接测 `handleEditor()`，只能把逻辑放进一个可测的小 helper。

## 验证（PHP 8.3，composer 2.8）
- 依赖安装：`COMPOSER_ALLOW_SUPERUSER=1 composer install --no-scripts --prefer-source`。本环境中 api.github.com 的 zipball 返回 403，所以用了 `--prefer-source`。phpstan/phpstan 只有 dist 包，做法是浅克隆 tag 1.12.34，打成 zip，再通过临时的 `composer-local.json/lock`（`COMPOSER=composer-local.json`）指向这个本地 zip 安装，装完已删除这两个临时文件。这些步骤只是为了在本环境装依赖，和补丁无关。
- Red（只保留测试，还原 libraries/）：
  `git stash push libraries/ ChangeLog && vendor/bin/phpunit --no-coverage test/classes/UtilTest.php --filter testGetQueryWithDelimiter`
  → `Error: Call to undefined method PhpMyAdmin\Util::getQueryWithDelimiter()`（1 error）
- 语义对照：`new Parser("CREATE PROCEDURE `p`() BEGIN SELECT 1; SELECT 2; END")` 得到 stmts=2、errors=1；包裹后加上 DROP 前缀得到 stmts=2、errors=0。
- Green：`vendor/bin/phpunit --no-coverage test/classes/UtilTest.php test/classes/Database/` → OK (242 tests, 1507 assertions)
- 全量单元测试：`vendor/bin/phpunit --no-coverage --testsuite unit` → OK (3190 tests, 12557 assertions, 44 skipped)
- `vendor/bin/phpcs <改动的 5 个文件>`：通过（exit 0）
- `vendor/bin/phpstan analyse --memory-limit=2G <改动的 5 个文件>`：base 和改动后都是 59 行 raw 输出，按文件+消息对比完全一致（只对子集分析时 baseline 不匹配，所以有这些既有报错），没有新增问题。
- `vendor/bin/psalm --threads=2 <改动的 5 个文件>`：base 和改动后一致（3× PossiblyInvalidCast、2× MissingConstructor，都是既有问题），没有新增问题。
- **没有运行**：selenium 端到端测试（test/selenium/Database/{Procedures,Events,Triggers}Test.php），因为本机没有 MySQL/浏览器；也没有跑全仓库的 phpstan/psalm（内存和时间开销大）；yarn/JS 构建按要求不运行。

## 需要提交者注意
- 仓库要求 DCO，commit 里已有 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`。仓库没有 AI 相关政策，也不需要 AI trailer。PR 正文里按 brief 写了 disclosure 段落。
- PR 必须开到 **QA_5_2**，不是 master。
- 维护者可能更希望 helper 放在别处（比如 Generator），或者直接在 3 个类里内联字符串。如果被要求，改动很小。
- 可以考虑补充说明：修改模式下也给 DROP 前缀包裹 DELIMITER 会出问题，所以 DROP 留在前面。
- 有条件的话，提交前在本地用真实 MySQL 手动验证一次：新建 procedure，body 写 `BEGIN SELECT 1; SELECT 2; END`，确认成功提示里出现 `DELIMITER $$`，点 Edit 后直接 Go 可以执行。

## 如何提交
```bash
git clone https://github.com/phpmyadmin/phpmyadmin && cd phpmyadmin
git checkout -b fix-19578-delimiter-in-query-message origin/QA_5_2
git am /home/user/Playground/contributions/100-phpmyadmin-phpmyadmin-19578/0001-Fix-19578-Add-DELIMITER-to-the-query-shown-after-sav.patch
composer install && vendor/bin/phpunit --filter testGetQueryWithDelimiter test/classes/UtilTest.php
git push <your-fork> fix-19578-delimiter-in-query-message
gh pr create --repo phpmyadmin/phpmyadmin --base QA_5_2 --head anyingiit:fix-19578-delimiter-in-query-message \
  --title "$(cat /home/user/Playground/contributions/100-phpmyadmin-phpmyadmin-19578/pr_title.txt)" \
  --body-file /home/user/Playground/contributions/100-phpmyadmin-phpmyadmin-19578/pr_body.md
```
工作副本已在复核后删除（/home/user/work/phpmyadmin）。

## 独立复核（2026-10-01）
- 重新确认 issue 仍 open、无人分配、无评论；`pulls?q=is:pr 19578` 仍只有 #19942（只修 trigger 导出）。
- 显示链路：`Generator::getMessage()` 只对显示的 SQL 做格式化；Edit 链接到 `/database/sql`，Edit inline 提交到 `/import`（`js/src/functions.js`），导入流程支持 `DELIMITER`，包裹后可直接重新执行。
- 重新验证 red→green：只把 `libraries/` 还原到 base，`vendor/bin/phpunit --no-coverage test/classes/UtilTest.php --filter testGetQueryWithDelimiter` → 1 error（方法不存在）；恢复后 `vendor/bin/phpunit --no-coverage test/classes/UtilTest.php test/classes/Database/` → OK (242 tests, 1507 assertions)。
- `vendor/bin/phpcs` 改动的 5 个 PHP 文件：通过。
- 对最新 `origin/QA_5_2`（8dfc3db）`git apply --check` 通过；作者为 anyingiit，有 DCO Signed-off-by，补丁内无 AI 模型名。
- ChangeLog 新条目放在 5.2.4 段最上面，与仓库习惯一致（最新条目在上）。
- 修正：`pr_body.md` 改成 brief 要求的 `## Description / ## Related issue / ## Checklist` 结构，把仓库 PR 模板的检查项并入 Checklist，并注明 selenium 未运行。

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
