# 190 — ploi/roadmap：Docker 开发环境 php:8.4-fpm-alpine3.21 → alpine3.24

| 项目 | 内容 |
|---|---|
| Issue | 无（代码搜索发现；README 的 "Docker Support" 一节让用户用 docker/ 自建） |
| 专题 | PHP2Shell（CVE-2026-109618 / CVE-2026-109619） |
| 层级 | 自由（567 stars，维护者每周合并 PR） |
| 竞争 PR | 2026-10-22 检查：无相关 PR / issue |
| Status | ✅ 已提交 https://github.com/ploi/roadmap/pull/389 （2026-10-22，独立复核 PASS） |
| AI 政策 | CONTRIBUTING 欢迎贡献；AGENTS.md 是 Laravel Boost 给 agent 的编码规范，无禁止 AI 贡献条款（"改依赖需批准"——PR 本身就是请求批准） |

## 改动
`docker/Dockerfile` 一行：`php:8.4-fpm-alpine3.21` → `php:8.4-fpm-alpine3.24`。

## 验证（红→绿）
- 红：main 构建的镜像 PHP 8.4.15。绿：本分支镜像 PHP 8.4.27，扩展列表相同。
- 两个镜像里 composer install、npm ci && npm run build 后跑 pest：都是 1150 passed（不 build 前端时两边都是同样的 116 个 Vite manifest 失败）。
