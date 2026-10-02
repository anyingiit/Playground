# jgrossi/elephpant.me#347 — Show account creation date on profile

| 项 | 值 |
|---|---|
| Issue | https://github.com/jgrossi/elephpant.me/issues/347 |
| Tier | 自由 |
| Labels | frontend, good first issue |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | 2026-10-01：issue 无关联 PR、无 assignee、无评论；open PR 只有 #351（社交链接改图标）和 #86，均无关 |
| Base | `master` @ 51b4582 |

## 问题理解
#328（由 #339 关闭）在个人 herd 页加了 “Herd last updated x ago”。#347 希望再显示账号注册时间（至少月+年），格式建议 `Joined {Month} {Year} • Herd Updated x`，并顺带把 #328 的措辞改得一致。

## 合理性判断
同一 issue 作者（JonPurvis，活跃贡献者）提出，带 `good first issue`；`users.created_at` 已存在，纯视图改动，范围小，合理。
AI 政策：仓库有 `AGENTS.md`（Laravel Boost 指南）和 `.cursor/`，明显欢迎 AI 辅助；未发现禁止 AI 贡献的规定。

## 改动
- `resources/views/components/user-profile.blade.php`：新增 `showJoined` prop（默认 false）；把 “Joined F Y” 和 “Herd updated …” 用 ` • ` 拼在原日历图标那一行，任一缺失则省略。
- `resources/views/herd/show.blade.php`：传 `show-joined`（只在 herd 页显示，trade 列表 / 会话页不变）。
- `tests/Feature/ExampleTest.php`：旧断言改为 `Herd updated`；新增两条测试（有/无 elePHPant）。

## 验证
环境：仓库要求 PHP ^8.5，本机只有 8.3，使用 static-php-cli 的 PHP 8.5.8 (common build, 含 pdo_sqlite)；composer 依赖因 api.github.com 被拦，改为浅抓 git 源码打包后本地安装（composer.lock 已恢复原样，未改动）。`cp .env.testing .env` 同 CI。
- Red（还原视图改动，仅保留测试）：`pest tests/Feature/ExampleTest.php` → 3 failed, 5 passed
- Green：`pest tests/Feature/ExampleTest.php` → 8 passed (18 assertions)
- 全量：`./vendor/bin/pest -p` → 215 passed (504 assertions)
- `./vendor/bin/pint --test` → passed
- `./vendor/bin/phpstan analyse` → No errors
- `./vendor/bin/rector process --dry-run` → clean
- 未运行：CI 的 OpenAPI/redocly lint 与 elephpants.json 校验（与本改动无关）。

## 需要提交者注意
- 措辞：我用了句中小写 “Herd updated”，issue 原文是 “Herd Updated”；PR 中已说明可改。
- open PR #351（社交链接改为图标一行）也改 `user-profile.blade.php`，可能有轻微冲突，提交前 rebase 一下。
- 不需要 DCO / CLA；无 CHANGELOG；无 PR 模板。commit 作者 anyingiit <49945850+anyingiit@users.noreply.github.com>，无 AI trailer。
- 仓库 `AGENTS.md` 无披露要求；PR 正文已包含 Claude Code 披露段。

## 如何提交
```bash
gh repo fork jgrossi/elephpant.me --clone && cd elephpant.me
git checkout -b show-joined-date origin/master
git am /path/to/0001-Show-account-creation-date-on-profile.patch
git push -u origin show-joined-date
gh pr create --repo jgrossi/elephpant.me --head anyingiit:show-joined-date \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
Show account creation date on profile

## PR body
见 `pr_body.md`。
