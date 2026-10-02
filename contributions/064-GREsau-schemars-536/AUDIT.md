# AUDIT — GREsau/schemars @ ed61863 (v1.2.2)

`python3 tools/audit_repo.py /home/user/work/schemars` (321 text files)

| 检查项 | 结果 | 结论 |
|---|---|---|
| 自动执行面 (build.rs / setup / hooks) | 无（`find -name build.rs` 为空） | benign |
| npm lifecycle hooks | 无 | benign |
| 已提交二进制 | 无 | benign |
| 可疑模式 | 无 | benign |

Verdict: 纯 Rust 库 + proc-macro，无构建脚本，可以安全运行 `cargo test`。
