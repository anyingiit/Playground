# XAGI-Lab/melra#388: `melra help` omits MELRA_PAYLOAD_KEY and MELRA_HARNESS_TOOLS

| 项 | 值 |
|---|---|
| Issue | https://github.com/XAGI-Lab/melra/issues/388 |
| Tier | 自由 |
| Labels | area: docs, documentation, good first issue |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 19:45 UTC：`repo:XAGI-Lab/melra 388` → 0；`help MELRA_PAYLOAD_KEY` → 0；issue 无评论、无 assignee、无关联 PR |
| AI 政策 | CONTRIBUTING / docs/CONTRIBUTING_GUIDE / CLAUDE.md 无 AI 贡献限制（提到 LLM 的地方都是产品定位） |
| Base | `main` @ 330625b |
| DCO / CLA | **需要 DCO（CI 强制）**：commit 已带 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`；无 CLA |
| 需先认领 | 否 |

## 问题理解
`docs/INSTALLATION.md` 的环境变量表有 18 个变量，`melra help` 的 Environment 块只列了 16 个，正好缺 `MELRA_PAYLOAD_KEY` 和 `MELRA_HARNESS_TOOLS`。现有 `check-env-docs.mjs` 只校验代码↔文档，不管 help。

## 改动
- `apps/cli/src/index.ts`：help() Environment 块末尾加两项（沿用长名列的 35 列对齐，行宽 < 80），文案取自 issue 建议。
- `scripts/check-env-docs.mjs`：解析 help() 模板字面量中 `Environment:` 到 `` `); `` 之间以两个空格开头的 `MELRA_*` 名称，要求文档表中每个变量都出现；顶部注释同步说明；成功信息加 "and listed by 'melra help'"。
- `CHANGELOG.md`：`[Unreleased]` → 现有 `### Fixed` 首条。
- commit：`fix(cli): …`，带 DCO 签名。

## 验证
- 红：只回退 index.ts → `node scripts/check-env-docs.mjs` rc=1，报两条缺失
- 绿：恢复后 rc=0，"All 18 … listed by 'melra help'"
- `pnpm build` 成功；`node apps/cli/dist/bin.js help | grep -c …` → 2
- `pnpm docs:check`（links + env + changelog）全过；`check-readme-examples` 20 blocks OK；`check-dist` OK
- `apps/cli`：`tsc -p tsconfig.test.json` OK；`vitest run` 7 files / 137 passed
- 未跑：其他 package 的测试、`versions:check`、`release.test.mjs`、`python:check`（与改动无关）

## 如何提交
```
tools/submit_pr.sh contributions/243-XAGI-Lab-melra-388 XAGI-Lab/melra main fix-help-env-vars contributions/243-XAGI-Lab-melra-388/pr_title.txt contributions/243-XAGI-Lab-melra-388/pr_body.md
```
（手动：fork → `git checkout -b fix-help-env-vars origin/main` → `git am 0001-*.patch` → push → 用 pr_title.txt / pr_body.md 开 PR）

## 独立复核（2026-10-22 20:05 UTC）
- 上游：#388 open、未指派、无评论；PR 搜索 `388` → 0，`help environment` → 只有无关的已关闭 #300。
- 新浅克隆 main@330625b，`git am` 干净；作者/Signed-off-by 为 anyingiit noreply。
- 红→绿确认（回退 index.ts → check-env-docs rc=1 并点名两个变量；补丁 → rc=0）；check-changelog / check-links 通过；pnpm install+build 成功；cli tsc OK，vitest 137 passed。
- help 输出与 35 列对齐，新行最长 77 字符；正则只匹配两空格缩进的变量行，Environment 块结构变化时会显式报错而不是静默通过。
- 结论：PASS
