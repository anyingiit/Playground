# hanami/hanami-minitest#11 — README links to a missing EXAMPLES.md

| 项 | 值 |
|---|---|
| Issue | https://github.com/hanami/hanami-minitest/issues/11 |
| Tier | 自由（hanami） |
| Labels | bug, help wanted |
| Status | ✅ ready（复核 PASS，未提交） |
| 重复 PR 检查 | 2026-10-22 22:40 UTC：仓库无 open PR（9 个全已合并）；issue 无评论、无 assignee、无关联 PR |
| AI 政策 | 无 |
| Base | `main` @ 163c4af |
| DCO / CLA / changeset | 无；文档改动不写 CHANGELOG |
| 需先认领 | 否（CONTRIBUTING 明确接受文档错误修正） |

## 问题理解 / 改动
README 写"详见 EXAMPLES.md"，但仓库里没有这个文件。README 的 Usage 一节本身已有各类测试示例，故删除这句悬空链接。README.md 由 hanakai-rb/repo-sync 从 README.repo.md 生成，两处同改。PR 正文给维护者留了"改成新建 EXAMPLES.md"的选项。

## 验证
- `grep -rn EXAMPLES .` 修改后无引用；纯文档，无测试可跑。

## 如何提交
```
tools/submit_pr.sh contributions/275-hanami-hanami-minitest-11 hanami/hanami-minitest main remove-examples-link contributions/275-hanami-hanami-minitest-11/pr_title.txt contributions/275-hanami-hanami-minitest-11/pr_body.md
```

## 独立复核（2026-10-22 22:55 UTC，独立 agent）
- #11 open、无 assignee/评论/关联 PR；仓库 0 个 open PR。新克隆 `git am` 干净，修改后无 EXAMPLES 引用。
- 确认 hanakai-rb/repo-sync 的 README.md.tpl 读取 README.repo.md 生成 README.md，两处同改正确；该行来自 9389bf5（"Get started (#3)"），EXAMPLES.md 从未存在；hanami-rspec 等兄弟仓库也没有 EXAMPLES.md。
- 建议正文示例列表补上 action → 已改。结论：PASS
