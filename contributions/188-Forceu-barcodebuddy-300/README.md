# 188 — Forceu/barcodebuddy#300：Docker 镜像升到 Alpine 3.24 / PHP 8.3 以修复 PHP2Shell

| 项目 | 内容 |
|---|---|
| Issue | https://github.com/Forceu/barcodebuddy/issues/300 （镜像在 Forceu/barcodebuddy-docker，PR 投到那里） |
| 专题 | PHP2Shell（CVE-2026-109618 / CVE-2026-109619） |
| 层级 | 自由（主仓库 610 stars，2026-09 仍在发版；docker 仓库 37 stars） |
| 竞争 PR | 2026-10-22 检查：两个仓库都没有相关 PR；issue 无评论 |
| Status | ✅ 已提交 https://github.com/Forceu/barcodebuddy-docker/pull/39 （2026-10-22，独立复核 PASS；已在 issue #300 留言链接 PR） |
| AI 政策 | 两个仓库都没有 AGENTS/CLAUDE/CONTRIBUTING，无相关规定 |

## 问题理解
官方镜像 `f0rc3/barcodebuddy:latest` 基于 `alpine:3.15`，PHP 8.0.25。Alpine 3.15 和 PHP 8.0 都已停止维护，重新构建拿不到任何修复，只能换基础镜像和 PHP 大版本。

## 改动
两个 Dockerfile：`alpine:3.24`，`php8-*`→`php83-*`（redis 扩展改名 `php83-pecl-redis`），相关路径改 php83，去掉 3.24 上已不存在的 `libressl3.4-libssl`；`root/etc/php8`→`root/etc/php83`；Go supervisor 里 php8/php-fpm8/php.ini 路径改为 php83。

## 验证（红→绿）
- 红：已发布镜像 PHP 8.0.25 / Alpine 3.15.11。
- 绿：新镜像 PHP 8.3.36 / Alpine 3.24.3。
- 两镜像连同一个 Grocy（linuxserver/grocy v4.7.1）对比：建用户、登录、Grocy 设置、system/info、设置页、API 管理页、screen.php、扫未知条码（在线查名）、购买模式扫已知条码使 Grocy 库存 +1、cron.php、错误日志，全部一致通过；TZ 写入 php.ini、bbuddy-local.ini 生效。
- Dockerfile.dev 构建成功，PHP 8.3.36。
- 386 / arm v6 / arm v7 / arm64 上 `apk add --simulate` 包列表全部可解析；只实际运行了 amd64。
- 仓库无测试套件。

## 需要注意
docker 仓库自 2023-05 无提交，issue #38（新版本没推到 Docker Hub）也未处理；合并后需维护者手动触发发布工作流。
