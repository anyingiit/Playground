# AUDIT — microsoft/go-mssqldb @ fa8008dc (2026-10-01)

`python3 tools/audit_repo.py /home/user/work/go-mssqldb`（262 个文本文件）

| 命中 | 复核 | 结论 |
|---|---|---|
| 自动执行面（install/build/test hooks） | 无 setup.py/package.json/Makefile 钩子；Go 无安装脚本 | 良性 |
| 提交的二进制文件 | 0 | 良性 |
| long-base64-blob: msdsn/conn_str_test.go:508 | 测试用自签名 localhost 证书的 hex | 良性（测试数据） |
| long-base64-blob: integratedauth/ntlm/ntlm_test.go:93,102 | NTLM type-2 消息测试向量（hex） | 良性（测试数据） |
| secret-paths: fedauth.go:10 | 仅注释中出现 "authentication" 字样 | 良性（误报） |

额外人工检查：本次仅运行 `go build/vet/fmt` 与根包中不需要 SQL Server 的单元测试；测试不会联网（无连接串时集成测试 skip）。

结论：未发现恶意代码，可以构建与运行测试。
