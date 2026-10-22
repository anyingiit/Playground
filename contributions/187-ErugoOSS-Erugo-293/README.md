# 187 — ErugoOSS/Erugo#293：Docker 镜像升到 Alpine 3.24 以修复 PHP2Shell

| 项目 | 内容 |
|---|---|
| Issue | https://github.com/ErugoOSS/Erugo/issues/293 （另见 #292） |
| 专题 | PHP2Shell（CVE-2026-109618 / CVE-2026-109619） |
| 层级 | 自由（1.1k stars，自托管文件分享） |
| 竞争 PR | 2026-10-22 检查：无相关 PR（只有用户在 issue 里贴自建镜像和手动修法） |
| AI 政策 | 仓库无 AGENTS/CLAUDE/CONTRIBUTING，无相关规定 |
| Status | ✅ 已验证，**未提交**（协调者要求本线程停止提交，交给 PHP 专题续接会话） |

## 问题理解
生产镜像 `FROM alpine:3.19`。3.19 已于 2025-11-01 停止维护，`php83` 永远停在 8.3.14，维护者即使重新构建也拿不到 PHP2Shell 修复。issue #292/#293 里多名用户请求升级基础镜像并重新发布，几位用户已自行用 3.23/3.24 构建成功。

## 改动
`docker/alpine/Dockerfile`、`docker/dev/Dockerfile`：`alpine:3.19`→`alpine:3.24`，community 源 `v3.19`→`v3.24`。包列表不变。

## 验证（红→绿）
- 红：`wardy784/erugo:latest`（当前发布版）`php -v` = 8.3.14；`alpine:3.19` 仓库里 php83 = 8.3.14-r0。
- 绿：新镜像 `php -v` = 8.3.36；`php-fpm83 -t` 通过；扩展列表一致。
- 两个镜像同条件对比：health 200、首个用户建立、登录、tus 上传→建分享→下载内容一致，均通过。
- dev Dockerfile：包列表在 3.24 上 `apk add --simulate` 全部可解析（完整 dev 镜像构建被本机自动模式拦截，未执行）。
- 仓库自带 phpunit：生产镜像不含 xmlwriter 扩展，新旧镜像都无法跑，非本改动引起。

## 需要提交者注意
维护者自 2026-03 以来没有提交；合并后还需维护者重新构建并推送 Docker Hub 镜像才对用户生效。
