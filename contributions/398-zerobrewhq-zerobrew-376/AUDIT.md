# AUDIT — 398 zerobrew#376 `zb bundle check`

- 范围：`zb_cli/src/cli.rs`、`zb_cli/src/commands/bundle.rs`、`README.md`、`CHANGELOG.md`。无依赖变更，无 unsafe，无网络访问（只读本地 SQLite）。
- 安全：Brewfile 路径来自用户参数，只读；输出仅打印 Brewfile 中的条目名。无命令执行、无文件写入。
- 行为兼容：新增子命令，不改 `bundle install`/`dump`/默认 `zb bundle` 行为。
- 错误路径：Brewfile 不存在或为空 → 沿用 `load_manifest` 的 FileError；条目非法（如 `cask:` 空 token）→ 返回 `normalize_formula_name` 的错误；有缺失 → ExecutionError，主程序打印 `error:` 并退出 1。
- 已知局限：别名/改名的 formula（如 Brewfile 写别名，DB 记规范名）会被报告为缺失；`bundle install` 同样按写法安装，检查不联网所以无法解析别名。属保守方向（多报缺失 → 用户再跑一次 install，不会漏装）。
- 测试：hermetic，临时目录 + 临时 SQLite；ApiClient 指向 127.0.0.1:9 且不会被调用。
- 提交信息：`feat(zb_cli): add zb bundle check`，与 #218 等前例一致；`Closes #376`；`Assisted-by: Claude Code`；无模型名。
