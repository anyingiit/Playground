# AUDIT: vitruv-tools/methodologistUI-backend (develop @ 1d91739)

运行了 `mvn -pl app -am test-compile/test/verify`（Spotless、Checkstyle、JaCoCo、单元测试；H2，无外部服务）和 `spotless:apply`。AGENTS.md 面向 AI 代理与人类贡献者，欢迎遵守其规则的 AI 贡献，无 AI 署名限制；要求 PR 指向 develop、说明原因、链接 issue、不弱化测试。无 PR 模板、无 CLA/DCO。

扫描结论：两个 lsp jar 是仓库自带的语言服务器（应用运行时资源，测试未启动它们）；mvnw.cmd 下载是 wrapper 正常行为；docker-compose 里的 /dev/tcp 是对本地 127.0.0.1:9000 的健康检查，不是反弹 shell。均未执行。

# Audit: /home/user/work/vitruv  (268 text files scanned)

## Auto-executing surface (install/build/test hooks)
- -: none

## npm lifecycle hooks
- -: none = 

## Committed binaries
- app/src/main/resources/lsp/tools.vitruv.dsls.reactions.ide.jar (29623607 bytes)
- app/src/main/resources/lsp/vitruvocl-language-server.jar (4205363 bytes)

## Pattern findings

### powershell-download (1)
- mvnw.cmd:121: `$webclient.DownloadFile($distributionUrl, "$TMP_DOWNLOAD_DIR/$distributionUrlName") | Out-Null`

### reverse-shell (1)
- docker-compose.yaml:97: `exec 3<>/dev/tcp/127.0.0.1/9000 &&`
