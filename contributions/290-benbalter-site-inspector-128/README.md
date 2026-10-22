# benbalter/site-inspector#128 — README 的 CLI 选项和 "What's checked" 过时

| 项 | 值 |
|---|---|
| Issue | https://github.com/benbalter/site-inspector/issues/128 （good first issue） |
| Tier | 自由 |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 22:30 UTC：仓库无 open PR，issue 无评论/assignee/关联 PR |
| AI 政策 | CLAUDE.md 只限制 agent 发版，无 AI 禁令；正文含 disclosure 段 |
| Base | `main` @ 6cd7b30（与 289 不冲突：289 改 hsts.rb/spec/CHANGELOG，本包只改 README.md） |
| DCO / CLA / 认领 / CHANGELOG | 无 / 无 / 不需要 / 不需要（文档改动，#127 修复也没加） |

## 改动
只改 README.md：选项块换成真实 `--help` 输出（10 个 `--<check>`）；每个检查列出 `to_h` 的 key，新增 Cookies、Well-known、Whois 小节，Headers 改为真实 header 名，Content 补 6 个 key，HSTS 补 `preload_list_status`。

## 验证
纯文档。用假 pa11y/wappalyzer 让 `--help` 输出全部检查；用 ruby 单行核对 `WellKnown.keys`、`Content.paths`。

## 如何提交
```
tools/submit_pr.sh contributions/290-benbalter-site-inspector-128 benbalter/site-inspector main readme-checks contributions/290-benbalter-site-inspector-128/pr_title.txt contributions/290-benbalter-site-inspector-128/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
PASS：新克隆干净应用；--help 输出与 README 字节一致；逐个核对各检查 `to_h` 的 key 全部正确，issue 三条验收标准全满足；无竞争 PR，无需 CHANGELOG。建议正文注明用的是假脚本 → 已改。Domain/Endpoint 小节的旧错误超出 issue 范围，未动。
