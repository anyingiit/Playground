# AUDIT — crazy-goat/tikv-php @ 5012ebf（同 330）

`python3 tools/audit_repo.py tikv-php`: no auto-executing hooks, no npm lifecycle hooks, no committed binaries, no pattern findings.

| 项 | 审阅 | 结论 |
|---|---|---|
| composer.json `scripts` | 仅 lint/test/phpstan 等手动脚本，无 post-install/post-update 钩子 | 良性 |
| composer 插件 | `dealerdirect/phpcodesniffer-composer-installer`、`infection/extension-installer`（知名包；本次 composer 以 root 运行插件被自动禁用） | 良性 |
| phpunit.xml bootstrap | `vendor/autoload.php` | 良性 |
| bin/*.sh、scripts/*.sh、Makefile | 只在手动 lint / E2E（Docker）时运行，本次未运行 | 良性 / 未执行 |

依赖安装：`composer install --prefer-source --ignore-platform-req=ext-grpc`（api.github.com 被拦，phpstan 2.3.1 从 git tag 打包后用本地 zip 安装，commit 与 lock 中的 6155239 一致）。
