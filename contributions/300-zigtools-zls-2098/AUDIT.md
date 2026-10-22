# AUDIT: zigtools/zls（master @ 82ba535）

`python3 tools/audit_repo.py /home/user/work/zls`：无自动执行钩子、无 npm 钩子、无二进制、无可疑模式（脚本不扫 .zig，下面人工复核）。

| 检查项 | 复核 | 结论 |
|---|---|---|
| build.zig `git describe` / `std.process` | 仅用于生成版本号；失败时 fatal | 良性 |
| build.zig `addSystemCommand("minisign")` | 只在发布签名步骤，测试不触发 | 良性 |
| build.zig.zon 依赖 known-folders / diffz / lsp-kit / tracy v0.14.1 | 固定 commit/tag + 内容哈希；用 git 拉取后 `zig fetch` 得到的哈希与 zon 完全一致 | 良性 |
| 构建期运行的生成器 `zls_gen`、`lsp-codegen` | 仓库内/依赖内 Zig 源码，生成 version_data.zig 与 lsp_types.zig，无网络/子进程 | 良性 |
| lsp-kit build.zig | 只读本地 metaModel.json，无 system command/HTTP | 良性 |

结论：未发现恶意代码，可以构建和测试。
