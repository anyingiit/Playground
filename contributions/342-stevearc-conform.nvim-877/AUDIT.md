# AUDIT — stevearc/conform.nvim @ 016802d (master)

`python3 tools/audit_repo.py conform.nvim`: no auto-executing hooks, no npm hooks, no committed binaries, no pattern findings.

| 项 | 审阅 | 结论 |
|---|---|---|
| run_tests.sh | 在 .testenv 下 git clone plenary.nvim 和 nvim-treesitter（官方仓库），headless nvim 跑测试 | 良性，已运行 |
| tests/minimal_init.lua | 用 nvim-treesitter 安装 5 个 parser；本环境下载 parser 时 403，只影响 3 个依赖 parser 的用例（基线同样失败） | 良性 |
| tests/fake_formatter.sh | 测试用假 formatter，只读写 stdin/stdout | 良性 |
| .github/pre-commit、pre-push | make fastlint，未安装 | 未执行 |
| 工具 | nvim 0.12.6 和 tree-sitter 0.27.1 都是官方 release 二进制；luacheck 来自 luarocks；stylua v2.1.0 官方 release | 良性 |
