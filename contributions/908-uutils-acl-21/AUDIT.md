# AUDIT — uutils/acl @ 2340e96 (shallow clone)

`python3 tools/audit_repo.py /home/user/work/acl`：22 个文本文件，0 个 pattern 命中，无二进制，无 npm hook。

| 命中 / 自动执行面 | 已审阅 | 结论 |
|---|---|---|
| `build.rs`（cargo 构建脚本） | 全文阅读 | 良性：只读取 `CARGO_FEATURE_*` 环境变量，用 `phf_codegen` 在 `OUT_DIR/uutils_map.rs` 生成工具映射表；无网络、无进程调用、无 OUT_DIR 以外的写入 |
| `tests/tests.rs` | 阅读 | 良性：设置 `UUTESTS_BINARY_PATH`，用 `Command` 只运行本仓库编译出的 `acl` 二进制 |
| `util/publish.sh` | 阅读 | 发布脚本（curl crates.io API），测试/构建不会调用；本次未运行 |
| 依赖 | `Cargo.lock` 全部来自 crates.io（uucore/uutests/clap/xattr/uzers 等 uutils 常用依赖） | 良性 |

结论：未发现恶意代码，可以 `cargo build/test`。
