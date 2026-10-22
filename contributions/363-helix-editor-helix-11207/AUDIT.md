# AUDIT

## helix-editor/helix @ ba40e54
同 360–362（同一克隆）：build.rs 只拉取/编译语法和读 git 哈希（已用 `HELIX_DISABLE_AUTO_GRAMMAR_BUILD=1` 关闭）。

## hankthetank27/tree-sitter-liquid @ e45dbac（MIT）
`tools/audit_repo.py`（31 个文本文件）：

| 命中 | 复核 | 结论 |
|---|---|---|
| `setup.py`、`bindings/rust/build.rs`、`package.json` install=node-gyp-build | 各语言绑定的标准构建脚本；**未执行**——helix 只用 `src/parser.c` + `src/scanner.c` 由 cc 编译 | 良性 |
| `prebuilds/darwin-arm64/tree-sitter-liquid.node` | 上游提交的 macOS 预编译 Node 绑定，未使用 | 良性（未运行） |
| `src/scanner.c` | 人工浏览：外部扫描器只处理注释/raw/doc 等内容 token，无 I/O、无系统调用 | 良性 |

语法通过本地 hx `--grammar fetch/build`（XDG_CONFIG_HOME 临时目录，`use-grammars = { only = [liquid, html, css, json, javascript, yaml] }`）拉取编译；另用临时 venv 装 py-tree-sitter 只为打印语法树。
结论：安全。
