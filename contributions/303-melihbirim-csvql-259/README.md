# 303 — melihbirim/csvql#259 Shell completions follow-ups

| 项 | 内容 |
|---|---|
| Issue | https://github.com/melihbirim/csvql/issues/259 |
| Tier | 新锐（2026-02 创建，30★，Zig，维护活跃） |
| Labels | enhancement, good first issue |
| Status | ✅ ready（独立复核 PASS，第 2 轮） |
| 重复/竞争检查 | 10-22：issue 无评论、无指派、无关联分支/PR；3 个开放 PR（#261–263，jadhavgaurav）都是 SQL 聚合/字符串修复，无关 |
| AI 政策 | CONTRIBUTING 无 AI 条款；项目本身面向 AI agent（有相关博客），无禁止 |

## 问题理解
维护者 review #250/#251（bash/zsh 补全）时列的非阻塞后续项：bash `--root=dir` 不补全；zsh 排斥组比二进制更严、`--root` 不支持逗号列表；drift 测试在全文（含注释）匹配 flag；README 的 macOS/zsh 安装说明。

## 合理性 / 取舍
- 前 3 项（zsh 两项 + 测试）和 README 照做。
- **bash `--root=dir` 故意没做**：二进制只解析 `--root <dir>`，`--root=/home` 实测不生效（放在查询后面时能读到根目录外的文件、exit 0），补全 `=` 形式会把用户引向静默失去沙箱的写法。PR 正文说明并提议后续两种做法。所以写 "Part of #259" 而非 Closes。

## 改动（3 文件 +88/−16）
- `completions/_csvql`：`--json/--jsonl` 只排斥 `--markdown`；`--table/--no-table` 无排斥；`--markdown` 排斥 `--json --jsonl --no-header`；`--no-header` 排斥 `--markdown`。`--root` 动作改 `{_dir_list -s ,}`（裸写法在 `_arguments` 中逗号后不补全，实测）。
- `tests/completions_test.zig`：新增 `isSpecLine`/`specNames`/`specContainsWord`，只在 bash `compgen -W` 行、zsh 以 `'` 开头的 spec 行和 `compadd` 行匹配；zsh spec 去掉开头排斥组和 `[描述]` 只看选项名（issue 原文还要求“出现在别的 spec 排斥组里也不算”）；加 2 个单测。
- `README.md`：macOS `~/.bash_profile`；zsh `mkdir -p` + `fpath=(...)` 在 compinit 前。

## 验证
- Zig 0.15.2（与 CI 一致）：`zig build test --summary all` → 35/35 steps，1066/1066 tests passed；`zig fmt --check src tests build.zig` 干净。
- 红→绿：把 bash 里的 `--strict` 从 compgen 列表移到注释：旧测试 1064/1064 通过（漏检），新测试失败 `completions/csvql.bash is missing --strict`。删除 zsh `--markdown` 或 `--no-header` spec 行（它们仍出现在别的排斥组里）：新测试分别报 missing。
- zsh 5.9 pty 捕获补全（脚本在 scratchpad）：
  - 旧：`--json --` 不给 `--jsonl/--table/--no-table/--markdown`；`--root da,d` 无结果。
  - 新：`--json --` 给 `--jsonl --table --no-table`，不给 `--markdown`；`--markdown --` 不给 `--json --jsonl --no-header`；`--table --` 全给；`--root da,d` → `da,da da,db`；`--root d` → `da db`。

## 如何提交
```
git clone https://github.com/melihbirim/csvql && cd csvql   # base main @ c1030e9
git checkout -b completions-follow-ups
git am /path/to/0001-fix-shell-completion-follow-ups-from-250-review-259.patch
```
PR 标题见 pr_title.txt，正文见 pr_body.md。无 DCO、无 CLA、无需认领。

## 需要提交者注意
- 提交信息格式跟仓库（`fix: ... (#259)`），维护者 squash 合并。

## 独立复核
- 第 1 轮 **FAIL**（1 条阻塞）：zsh spec 整行匹配，flag 只出现在别的选项排斥组里时仍能通过（删掉 `--markdown`/`--no-header` 的 spec 行测试照样过），而 issue 原文明确要求这种情况也要失败。已修：`specNames` 去掉排斥组和描述，补单测，红测试两例均失败，全套 1066/1066。
- 采纳可选建议：`--root=` 说明改用更有力的例子（放在查询后面能读到根目录外的文件）。
- 第 1 轮其余检查都通过：exclusion 与二进制一致；`{_dir_list -s ,}` 选法正确（裸写法会被 `_arguments` 插入参数，分隔符退回 `:`）；install/文件补全无回归；无竞争 PR。
- 第 2 轮 **PASS**：新克隆全套 1066/1066、fmt 干净；9 个红测试（注释/排斥组/描述/brace 形式/install/--print）全部按预期失败；`specNames` 对现有每行 spec 都不丢选项名；PR 正文数字与 `--root=` 例子复现无误。
