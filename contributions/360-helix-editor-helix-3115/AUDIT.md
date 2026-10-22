# AUDIT: helix-editor/helix @ ba40e54 (master, 2026-10-22)

`python3 tools/audit_repo.py helix`（568 个文本文件）

| 命中 | 复核 | 结论 |
|---|---|---|
| `helix-term/build.rs` | 调 helix-loader 的 fetch_grammars/build_grammars（按 languages.toml 里的 git 源拉取 tree-sitter 语法并编译）；用 `HELIX_DISABLE_AUTO_GRAMMAR_BUILD=1` 关闭；Windows 下调 rc.exe 嵌图标 | 良性（已关闭语法拉取） |
| `helix-loader/build.rs` | 调 `git` 读当前提交哈希做版本号 | 良性 |
| secret-paths：`languages.toml` 里 `.kube/config`、`.npmrc` | 只是文件类型 glob（yaml / ini 识别） | 良性 |
| `.envrc`、`flake.nix`、`shell.nix` | nix 开发环境，未使用 | 良性 |

另：`@cucumber/language-server` 1.7.0 从 npm 安装时用 `--ignore-scripts`，装在 /home/user/work/cukeglobal，只用于本地 LSP 实测；bin 脚本只是启动 vscode-languageserver 连接、加载自带的 tree-sitter wasm。

结论：可以安全构建和运行测试。
