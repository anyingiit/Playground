# valkey-io/valkey-glide-ruby#309 — create_client_from_uri GVL / 删除 create_client 死代码

| 项 | 值 |
|---|---|
| Issue | https://github.com/valkey-io/valkey-glide-ruby/issues/309 |
| Tier | 新锐 |
| Labels | good first issue, help wanted |
| Status | ✅ ready — patch + PR 文本已完成 |
| 重复 PR 检查 | Issue open、无 assignee、无评论、无关联 PR；PR 列表搜索 309 / blocking / GVL 无结果（2026-10-01） |
| Base | `main` @ f6225af |
| Patch | `0001-chore-ffi-drop-unused-create_client-binding-and-test.patch` |

## 问题理解
Issue 指出 `create_client_from_uri` 的 FFI 绑定缺少 `blocking: true`，导致 `Valkey.new` 在连网/重试时一直持有 GVL，其他 Ruby 线程全部卡住。提议两点：(1) 加 `blocking: true`；(2) 删除未使用的 `create_client` 死代码。

## 合理性判断
- **第 (1) 点已在 main 修复**：PR #316（2026-09-17，pubsub 功能 PR）顺带给 `create_client` 和 `create_client_from_uri` 都加了 `blocking: true`，CHANGELOG 也有记录；但 issue 仍是 open，第 (2) 点没做，也没有任何测试保护这个行为。
- 本贡献做剩下的部分：删除 `create_client` 绑定（`lib/`、`test/` 都没有引用它），再加一个不需要服务器的回归测试，防止 GVL 释放以后被改回去。
- AI 政策：CONTRIBUTING.md 有 "AI-Assisted Development" 段，并提供 AGENTS.md/CLAUDE.md，说明允许 AI 辅助，没有禁止。

## 改动
- `lib/valkey/bindings.rb`：删除 `attach_function :create_client`，并给 `create_client_from_uri` 加一条说明注释。
- `test/unit/connection_gvl_test.rb`（新增）：本地开一个 TCPServer，只完成握手、从不回包；`Valkey.new(connect_timeout: 0.5)` 期间让一个 ticker 线程计数，断言连接确实等了 ≥0.2s、ticker 至少跑了 10 次。
- `CHANGELOG.md`：在 #316 那条下面加一行。

## 验证
环境：Ruby 3.3.6、ffi 1.17.4；native lib 用 RubyGems 上 `valkey-glide-rb-1.0.0` 里的 x86_64-linux-gnu `libglide_ffi.so`，放在 `lib/valkey/native/...`（没有提交；没有从源码 cargo 编译）。
- 红：临时去掉 `create_client_from_uri` 的 `blocking: true` 后运行 `bundle exec ruby -Itest -Ilib test/unit/connection_gvl_test.rb`，结果 FAIL，报 "only 0 ticker iterations ran during a 0.5s connect"。
- 绿：恢复后 PASS（0.55s），连续再跑 5 次都通过。
- `bundle exec rake test:unit` → 460 tests, 1169 assertions, 0 failures。
- `bundle exec rubocop` → 129 files, no offenses。
- 没跑：`test:standalone` / `test:cluster`（需要 Valkey 服务器，且改动不涉及命令路径）。
- 备注：调试时曾用 `reconnect_attempts: 0` 遇到一次挂起（仓库已知 issue #117 相关），测试里没有用这个参数。

## 需要提交者注意
- **DCO + 签名提交**：CONTRIBUTING 要求 `git commit -S -s`。patch 里已经带了 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`，但**没有 GPG/SSH 签名**，提交前请用 `git commit --amend -S --no-edit` 补签。
- PR 正文用的是仓库自己的 `.github/pull_request_template.md` 格式（Summary/Issue link/Changes/Limitations/Testing/Checklist），已经在 Summary 里加了 disclosure 段。
- 需要在 PR 里讲清楚：主修复已由 #316 完成，本 PR 只做收尾。维护者也可能觉得直接关 issue 就行，被关掉也没关系。

## 如何提交
```bash
git clone https://github.com/anyingiit/valkey-glide-ruby.git && cd valkey-glide-ruby   # 先 fork
git remote add upstream https://github.com/valkey-io/valkey-glide-ruby.git && git fetch upstream
git checkout -b fix/309-create-client-gvl upstream/main
git am /path/to/0001-chore-ffi-drop-unused-create_client-binding-and-test.patch
git commit --amend -S --no-edit          # 补加密签名
git push origin fix/309-create-client-gvl
gh pr create --repo valkey-io/valkey-glide-ruby --head anyingiit:fix/309-create-client-gvl \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

## PR title
见 `pr_title.txt`。

## PR body
见 `pr_body.md`。
