# AUDIT — stevearc/oil.nvim @ d3733d9 (master)

`python3 tools/audit_repo.py oil.nvim`: no auto-executing hooks, no npm hooks, no committed binaries, no pattern findings.

| 项 | 审阅 | 结论 |
|---|---|---|
| run_tests.sh | 在 .testenv 下 git clone plenary.nvim（官方仓库），然后 headless nvim 跑 PlenaryBustedDirectory | 良性，已运行 |
| .github/pre-commit、pre-push | 调用 make fastlint，未安装 | 未执行 |
| Makefile doc/lint | 会建 venv 并拉 nvim_doc_tools 等，未运行；只单独跑了 luacheck、stylua | 未执行 |
| 测试的文件操作 | files_spec 等在 tests/tmpdir.lua 建的临时目录里操作 | 良性 |
