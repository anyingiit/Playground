# AUDIT — nvim-orgmode/orgmode @ 78c9928 (master)

`python3 tools/audit_repo.py orgmode`: no auto-executing hooks, no npm hooks, no pattern findings. The only "committed binary" it reports is `parser/org.so`, which is not tracked (it is ignored by `parser/.gitignore`). It is the tree-sitter grammar that `tests/test.lua` compiles locally.

| 项 | 审阅 | 结论 |
|---|---|---|
| tests/test.lua | 先装 tree-sitter 语法：git clone 官方 nvim-orgmode/tree-sitter-org 指定版本，用本机 cc 编译到 parser/org.so；再在 tests/.deps 拉 plenary.nvim 跑 plenary 测试 | 良性，已运行 |
| Makefile | test / docs 目标；只用了 test | 良性 |
| scripts/ | 生成文档脚本，未运行 | 未执行 |
| 环境 | 补装 en_US.UTF-8 locale（tests/minimal_init.lua 需要），未改仓库 | — |
