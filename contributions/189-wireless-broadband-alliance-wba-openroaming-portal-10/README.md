# 189 — wireless-broadband-alliance/wba-openroaming-portal#10：PHP 基础镜像 alpine3.21 → alpine3.23

| 项目 | 内容 |
|---|---|
| Issue | https://github.com/wireless-broadband-alliance/wba-openroaming-portal/issues/10 |
| 专题 | PHP2Shell（CVE-2026-109618 / CVE-2026-109619） |
| 层级 | 自由（13 stars，WBA 官方项目，2026-10 仍在发版） |
| 竞争 PR | 2026-10-22 检查：仓库从未有过 PR；issue 下唯一评论误判为"浮动标签，重建即可" |
| Status | ✅ 已提交 https://github.com/wireless-broadband-alliance/wba-openroaming-portal/pull/11 （2026-10-22，base develop，独立复核 PASS；已在 issue #10 更正"重建即可"并链接 PR） |
| AI 政策 | 无 AGENTS/CLAUDE/CONTRIBUTING，无相关规定 |
| 注意 | 主开发在 GitLab（GitHub 是镜像，从没收过 PR），PR 可能不被处理；目标分支 develop |

## 问题理解
`php:8.4-fpm-alpine3.21` 标签 2025-11-22 起停更，重建仍是 PHP 8.4.15（已实测），issue 评论"重建即可"是错的。

## 改动
三个 Dockerfile 共 5 处 `alpine3.21`→`alpine3.23`。alpine3.24 试过：gpgme 2.x 缺 trust-list API，pecl gnupg-1.5.0 编译失败。

## 验证（红→绿）
- 红：发布镜像 1.14.1 与 alpine3.21 标签都是 PHP 8.4.15。
- 绿：新镜像 PHP 8.4.27，扩展列表与发布镜像完全一致。
- 两镜像同条件（MySQL 8.0 + memcached）：迁移、fixtures、首页 200、/login 跳转、后台登录到 2FA/安装向导跳转，全部一致。
- 三个 Dockerfile 均构建成功（DockerfileDev 由独立复核构建）。仓库没有测试用例（tests/ 只有 bootstrap.php）。

## 顺带发现（公开代码，非未披露漏洞）
三个 Dockerfile 都用 `wget --no-check-certificate` 从 tetrapi.pt 下载 PaloAlto SSL 检查 CA 并装为受信根证书，会进入发布镜像。这是公开仓库里的现有做法，不属于本次范围，未在 PR 中提。
