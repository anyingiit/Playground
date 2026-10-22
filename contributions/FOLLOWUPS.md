# 已开 PR 的跟进（2026-10-22 22:00 UTC 起盘点）

本地提交员按行执行。"推补丁"= 在本地 fork 分支上 `git am <patch>` 后 `git push`（不 force）；"回复"= 把 reply.md 原文贴为 PR 评论（`gh pr comment <url> -F reply.md`）。做完在行尾标 ✅。

| PR | 文件夹 | 操作 | 说明 |
|---|---|---|---|
| [XAGI-Lab/melra#393](https://github.com/XAGI-Lab/melra/pull/393) | contributions/243-XAGI-Lab-melra-388 | 推补丁 `followup-0001-keep-help-out-of-read-scan.patch` 到 `anyingiit/melra:fix-help-env-vars`，再回复 reply.md | Bhavana Sanal CHANGES_REQUESTED 三点全改；红→绿（release.test.mjs 7/8→8/8），她的复现现在正确报错 |
| [git-ai-project/git-ai#2436](https://github.com/git-ai-project/git-ai/pull/2436) | contributions/204-git-ai-project-git-ai-1036 | 推补丁 `followup-0001-remove-dropped-array-table.patch` 到 `anyingiit/git-ai:fix/codex-toml-preserve-comments`，再回复 reply.md | svarlamov 问能否不加依赖：解释 toml_edit 只新增一个 crate，并提出可改；同时修 Devin 指出的卸载丢注释（红→绿，新测试） |
