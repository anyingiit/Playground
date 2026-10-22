# AUDIT — Euro-Office/eurooffice-nextcloud @ efa7227 (main)

`python3 tools/audit_repo.py eo`: no auto-executing hooks, no npm lifecycle hooks, no committed binaries, no pattern findings.

| 项 | 审阅 | 结论 |
|---|---|---|
| composer.json `post-install-cmd` | `composer bin all install`（bamarni bin 插件）+ `vendor/bin/mozart compose`（给 firebase/php-jwt 加命名空间前缀）+ `dump-autoload`；均为知名工具，按 CI 流程执行 | 良性 |
| vendor-bin/mozart | 只 require coenjacobs/mozart | 良性 |
| package.json scripts | 未运行 npm（本次只改 PHP） | 未执行 |
| 测试环境 | nextcloud/server stable34 浅克隆 + 3rdparty 子模块，`occ maintenance:install --database sqlite`；server 的 vendor-bin/phpunit 安装 PHPUnit；与 CI（nextcloud/setup-server-action）一致 | 良性 |
