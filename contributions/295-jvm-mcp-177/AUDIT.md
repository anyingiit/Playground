# AUDIT: oscarbol09/jvm-mcp (main @ 68e7fc7)

运行了 `mvn verify`（全部模块的单元测试、JaCoCo；未用 mvnw 以免下载 wrapper）。CONTRIBUTING 要求 Conventional Commits、不要 AI 填充段落（正文已保持简洁，只留一句 disclosure）；有 PR 模板，已按结构填写；无 CLA/DCO。仓库根目录有 install.sh 等安装脚本，未运行。

扫描结论：maven-wrapper.jar 为标准 wrapper；46 字节的 test 资源 jvm-mcp-agent.jar 是测试用占位文件（非真实 jar）；powershell 下载是 mvnw.cmd 与官方安装脚本的正常行为；1.1.1.1 是测试里故意不可达的地址。均与本补丁无关、未执行。

# Audit: /home/user/work/jvm-mcp  (142 text files scanned)

## Auto-executing surface (install/build/test hooks)
- -: none

## npm lifecycle hooks
- -: none = 

## Committed binaries
- .mvn/wrapper/maven-wrapper.jar (63093 bytes)
- core/src/test/resources/agent/jvm-mcp-agent.jar (46 bytes)

## Pattern findings

### powershell-download (3)
- mvnw.cmd:148: `"[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $webclient.DownloadFile('%WRAPPER_URL%', '%WRAPPER_JAR%')"^`
- install.ps1:76: `Invoke-WebRequest -Uri $DownloadUrl -OutFile $ZipPath -UseBasicParsing`
- install.ps1:77: `Invoke-WebRequest -Uri $ShaUrl -OutFile $ShaPath -UseBasicParsing`

### raw-ip-url (2)
- mcp-server/src/test/java/dev/jvmmcp/BeansCommandTest.java:283: `// It will fail with exit code 1 because https://1.1.1.1:9999 won't be open,`
- mcp-server/src/test/java/dev/jvmmcp/BeansCommandTest.java:285: `int exitCode = cmd.execute("beans", "--actuator", "https://1.1.1.1:9999",`
