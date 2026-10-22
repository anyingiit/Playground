# AUDIT — thephpleague/openapi-psr7-validator @ b9ee232 (master)

| 项 | 审阅 | 结论 |
|---|---|---|
| composer.json scripts | test/analyze/cs 三个别名，无安装钩子 | 良性 |
| .github/workflows | CI（phpunit/phpstan/phpcs），未运行 | 未执行 |
| tests | 纯 PHPUnit，读 tests/stubs 下的 OpenAPI yaml/json | 良性 |
| 依赖 | 用去掉 phpstan/* 的临时 composer.local.json 安装（--prefer-source --no-scripts，root 下插件禁用；phpstan 包只有 dist，被拦）；仓库 composer.json/lock 未改 | 良性 |
