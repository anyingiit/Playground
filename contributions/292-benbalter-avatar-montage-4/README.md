# benbalter/avatar-montage#4 — script/download 留下旧头像、把 404 页存成图片

| 项 | 值 |
|---|---|
| Issue | https://github.com/benbalter/avatar-montage/issues/4 （good first issue） |
| Tier | 自由 |
| Status | ✅ ready（独立复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 22:50 UTC：无 open PR；已关闭的 #1 是硬编码 handle、与本 bug 无关；issue 无评论/assignee |
| AI 政策 | 无 CLAUDE.md/AGENTS.md，无 AI 禁令；正文含 disclosure 段 |
| Base | `main` @ bd44090 |
| DCO / CLA / 认领 / CHANGELOG | 无 / 无 / 不需要 / 仓库无 |

## 改动
`script/download`：去掉 glob 的引号（`rm -f ./avatars/*.png`）；`curl -fL`，失败时删残留并在最后列出失败 handle（stderr），仍 exit 0 让工作流继续生成拼图。

## 验证
沙箱访问不了 github.com 头像（403），用假 curl（本目录 fake-curl.sh，不随补丁提交）对比新旧脚本：改前残留 olduser.png 和 HTML 的 no-such-user.png，改后只剩 .gitkeep/github.png/octocat.png。另用本地 http.server 确认真 curl `-fL -o` 遇 404 不写文件。

## 如何提交
```
tools/submit_pr.sh contributions/292-benbalter-avatar-montage-4 benbalter/avatar-montage main download-cleanup contributions/292-benbalter-avatar-montage-4/pr_title.txt contributions/292-benbalter-avatar-montage-4/pr_body.md
```

## 独立复核（2026-10-22，独立 agent）
PASS：新克隆干净应用；假 curl 与真 curl+本地服务器均红→绿，`script/create` 能生成 montage；四条验收标准满足；macOS bash 3.2 兼容；shellcheck 干净。建议正文说明全部失败时工作流仍会在 montage 步失败 → 已补。
