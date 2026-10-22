# AUDIT — hrsh7th/nvim-cmp @ 2ffe79f (main)

`python3 tools/audit_repo.py nvim-cmp`: the only auto-executing surface is `.githooks/pre-commit`; there are no npm hooks, no committed binaries and no pattern findings.

| 项 | 审阅 | 结论 |
|---|---|---|
| .githooks/pre-commit / init.sh | init.sh 把 githooks 拷进 .git/hooks；未运行 init.sh，钩子未安装 | 未执行 |
| Makefile | lint=luacheck，test=vusted | 良性 |
| rockspec | 只有元数据，依赖 lua 5.1–5.3 | 良性 |
| 测试工具 | vusted、luacheck 从 luarocks 安装（lua-term 和 mediator_lua 是 git clone 对应 tag 后 `luarocks make` 装的）；stylua v2.1.0 是官方 release 二进制；nvim 0.11.4 是官方 release | 良性 |
