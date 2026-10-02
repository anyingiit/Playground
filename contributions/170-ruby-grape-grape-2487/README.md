# ruby-grape/grape#2487 — Include Rack::TempfileReaper in Grape

| 项 | 值 |
|---|---|
| Issue | https://github.com/ruby-grape/grape/issues/2487 |
| Tier | 自由 |
| Labels | feature request, you can help |
| Status | ✅ ready — patch + PR text done (not submitted)；独立对抗复审通过（red→green 复跑、rubocop、全量 rspec 3075/0） |
| Base | `master` @ afdd3d2 (2026-10-01) |
| Duplicate-PR check | 2026-10-01 23:00 UTC: issue open, 0 comments, unassigned, Development 区无关联 PR/分支；`pulls?q=2487` 0 结果，`pulls?q=is:pr TempfileReaper` 0 结果（scout 也查过 `tempfile`）；独立复审 2026-10-01 23:09 UTC 复查：issue 仍 open、无评论/无关联 PR，`pulls?q=2487` 仍 0 结果 |
| 排除列表 | exclude_slugs.txt 中无 grape |

## 问题理解

Rack::Multipart 解析文件上传时创建的 tempfile，只有在中间件栈里有 `Rack::TempfileReaper` 时才会在响应结束后 `close!`（关闭并删除）。Rails 默认带这个中间件，所以在 Rails 中挂载 Grape 没问题；但纯 Rack 运行 Grape（rackup/puma 直接跑 API）时 tempfile 会一直留在磁盘上直到 GC/进程退出。维护者 ericproulx 开的 issue 提议直接把 Rack::TempfileReaper 加进 Grape。

## 合理性判断

- 维护者本人提出、打了 `you can help`（Grape 的 help-wanted 标签），无反对意见，需求明确。
- 仓库有 AGENTS.md 专门给 AI agent 的规则；最近的维护者提交本身带 `Co-authored-by: Claude ...` —— 明确欢迎 AI 辅助。CONTRIBUTING/.github/labels 中无 AI 禁令（labels 无描述）。
- Rack 2.2 / 3.x 都自带 `Rack::TempfileReaper`（autoload），无新增依赖。

## 改动

- `lib/grape/endpoint.rb` `build_stack`：在 `Rack::Head` 之前加 `stack.use Rack::TempfileReaper`（最外层，和 Rack::Head 一样放在 endpoint 栈里；在 Error 中间件外面，所以 `error!` / 被 rescue 的异常时也会清理）。
- `spec/grape/integration/rack_spec.rb`：新增 `multipart tempfiles` 两个用例 —— 成功上传和 `error!(422)` 两种情况下，请求结束后 `File.exist?(tempfile.path)` 为 false。
- `CHANGELOG.md`：4.1.0 Features 下加一行（PR 号占位 `#XXXX`）。
- 无 UPGRADING（不是契约破坏）。

## 验证

环境：Ruby 3.3.6，`bundle config set --local path vendor/bundle && bundle install`。

| 命令 | 结果 |
|---|---|
| 只保留新 spec、回退 lib：`bundle exec rspec spec/grape/integration/rack_spec.rb` | **6 examples, 2 failures**（tempfile 仍存在）→ red |
| 同上，`BUNDLE_GEMFILE=gemfiles/rack_2_2.gemfile` | **6 examples, 2 failures** → red |
| 打补丁后 `bundle exec rspec spec/grape/integration/rack_spec.rb` | 6 examples, 0 failures → green |
| 打补丁后 `RUBYOPT='--enable=frozen-string-literal' bundle exec rake`（AGENTS.md 要求：rubocop + rspec） | RuboCop 358 files no offenses；RSpec 3075 examples, 0 failures |
| CI 矩阵子集：`BUNDLE_GEMFILE=gemfiles/rack_2_2.gemfile bundle exec rspec spec --exclude-pattern='spec/integration/{grape_entity,grape_swagger,hashie,dry_validation,multi_*}/*_spec.rb'` | 3079 examples, 0 failures |
| 同上 `gemfiles/rails_8_1.gemfile` | 3077 examples, 0 failures |
| 双重 reaper（模拟 Rails 外层已有 reaper）：Rack::Builder 外层 `use Rack::TempfileReaper` 包 Grape API，MockRequest 上传（Rack 3.2.7 和 2.2.24） | `[201, "ok", 1, false]` —— 无报错，tempfile 已删除 |

未跑：其它 Ruby 版本（3.4/4.0）、rack_3_0/3_1、rails_7_2/8_0、integration gemfiles（与本改动无关）。

## 如何提交

```bash
git clone https://github.com/ruby-grape/grape && cd grape
git checkout -b tempfile-reaper origin/master
git am /path/to/0001-Add-Rack-TempfileReaper-to-the-endpoint-middleware-s.patch
bundle install && bundle exec rake
git push <your-fork> tempfile-reaper   # PR 目标: ruby-grape/grape master
```

PR title 见 `pr_title.txt`，PR body 见 `pr_body.md`。

### 需要提交者注意
- **CHANGELOG 占位**：开 PR 拿到编号后，把 CHANGELOG 里的 `#XXXX` 两处替换为真实 PR 号并 `git commit --amend` + `git push --force-with-lease`（AGENTS.md 要求一 PR 一 commit，用 amend；Danger 会检查 changelog 格式）。作者名用了 `@anyingiit`。
- 无 DCO、无 PR 模板、无 AI trailer 要求；AI 贡献被欢迎（AGENTS.md + 维护者自己的提交带 Claude co-author）。PR 描述已含 Claude Code 披露段。
- 提交信息风格：祈使句标题 + 正文 + `Fixes #2487`（AGENTS.md 要求引用 issue）；PR 描述 Related issue 用 `Closes #2487`（按模板，同样会自动关闭 issue）。
- 维护者很在意请求路径性能（大量 "Speed up ..." 提交）：本改动每个请求多一个 BodyProxy，PR 描述里已说明，如维护者希望放在别处（如 API instance 层或可配置）再调整。
