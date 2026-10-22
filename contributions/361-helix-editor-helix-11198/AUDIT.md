# AUDIT: helix-editor/helix @ ba40e54 (master, 2026-10-22)

同 360（同一克隆）：`tools/audit_repo.py` 命中只有 helix-term/helix-loader 的 build.rs（拉取/编译 tree-sitter 语法，已用 `HELIX_DISABLE_AUTO_GRAMMAR_BUILD=1` 关闭；git 读版本号）和 languages.toml 里的文件类型 glob，均良性。

sqls：`go install github.com/sqls-server/sqls@v0.2.48` 和 `@v0.2.27`（对照）装到 /home/user/work/sqls 私有 GOPATH，只用于本地 stdio 实测，不需要数据库，HOME 指向临时目录（没有 sqls 配置）。

临时探针测试 `helix-lsp-types/tests/zz_probe.rs`（反序列化两版 completion item）跑完已删除，不在补丁内。

结论：安全。
