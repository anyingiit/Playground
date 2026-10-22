# AUDIT — phpmyadmin/motranslator @ 7536000 (master)

`python3 tools/audit_repo.py motranslator`: no auto-executing hooks, no npm lifecycle hooks, no committed binaries, no pattern findings.

| 项 | 审阅 | 结论 |
|---|---|---|
| composer.json scripts | 仅 phpcs/phpstan/phpunit 别名，无安装钩子 | 良性 |
| benchmark*.php | 手动基准脚本，未运行 | 未执行 |
| tests | 纯 PHPUnit，读 tests/data 下的 .mo | 良性 |
| 依赖 | 用去掉 phpstan/psalm 的临时 composer.local.json 安装（--prefer-source --no-scripts；psalm 要求 PHP ≥8.3.16，本机 8.3.6）；仓库内未改动 composer.json | 良性 |
