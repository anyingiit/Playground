# danger/danger #1327 — Bitbucket server URLs not getting parsed correctly

| 项 | 值 |
|---|---|
| Issue | https://github.com/danger/danger/issues/1327 |
| Tier | 自由 |
| Labels | BitBucket, Bug, You Can Do This |
| Status | ✅ ready（独立复审通过，2026-10-01） |
| 重复 PR 检查 | 2026-10-01：`pulls?q=1327` 没有结果。issue 无人分配，也没有人在评论里认领或关联 PR（issue 开于 2021-10-06）。 |
| Base | `master` @ c94d38b3ce68 |

## 问题理解
在 Bitrise 上使用自建 Bitbucket Server，clone URL 形如 `https://host/bitbucket/scm/PROJ/repo.git` 时，`Danger::Bitrise#repo_slug_from` 返回的是整个 path：`bitbucket/scm/PROJ/repo`。`RequestSources::BitbucketServer#initialize` 中的 `project, slug = repo_slug.split("/")` 只取前两段，得到 project=`bitbucket`、slug=`scm`。API 请求因此失败，最后报 `NoMethodError`。

## 合理性判断
- 有 Bug 标签和 "You Can Do This" 标签，issue 报告者已经定位到根因。
- 修在 request source 这一层，而不是改 Bitrise：Bitrise 也服务 GitHub/GitLab，`bitrise_spec.rb` 要求保留多段 slug（GitLab subgroup，例如 `artsy/mobile/ios/artsy.github.io`）。Bitbucket Server 的仓库标识固定是 `PROJECT/REPO`（或 `~user/repo`），所以取最后两段是安全的。原来的两段 slug 行为不变。
- Appcircle 同样从 URL path 推出 slug，这次改动也顺带修好了它。

## 改动
- `lib/danger/request_sources/bitbucket_server.rb`：改为 `split("/").last(2)`，并加了说明原因的注释。
- `spec/lib/danger/request_sources/bitbucket_server_spec.rb`：在 `#new` 下新增用例。用 `Danger::Bitrise` 和 `https://stash.example.com/bitbucket/scm/PROJ/repo.git` 构造 CI source，先断言 slug 为 `bitbucket/scm/PROJ/repo`，再用 WebMock stub `projects/PROJ/repos/repo` 的 PR 接口，调用 `fetch_details` 后断言 `pr_json[:id] == 2080`。
- `CHANGELOG.md`：在 `## master` 下加了一条，链接的是 issue #1327。

## 验证（Ruby 3.3.6，Bundler 4.0.17）
```bash
cd /home/user/work/danger
export BUNDLE_PATH=/home/user/work/danger/vendor/bundle
bundle install -j2
# Red：
git stash push lib/danger/request_sources/bitbucket_server.rb
bundle exec rspec spec/lib/danger/request_sources/bitbucket_server_spec.rb -e "context path"
#  -> 1 failure: WebMock::NetConnectNotAllowedError ... GET .../projects/bitbucket/repos/scm/pull-requests/2080
git stash pop
# Green：
bundle exec rspec spec/lib/danger/request_sources/bitbucket_server_spec.rb spec/lib/danger/ci_sources/bitrise_spec.rb spec/lib/danger/ci_sources/appcircle_spec.rb
#  -> 56 examples, 0 failures
LANG=C.UTF-8 LC_ALL=C.UTF-8 bundle exec rspec spec/lib/danger/request_sources spec/lib/danger/ci_sources
#  -> 690 examples, 0 failures
bundle exec rubocop lib spec
#  -> 213 files inspected, no offenses detected
```
注意：不设置 UTF-8 locale 时，`github_spec.rb` 有 15 个用例因读取 fixture 时出现 `Encoding::InvalidByteSequenceError` 而失败。base 上的失败集合完全相同，属于环境问题，与本改动无关。
没有跑全量 `rake spec`（这个命令包含 rspec-queue 和 `danger plugins lint`），只跑了 request_sources 和 ci_sources 两个目录。vendor/bundle 已经删除。

## 独立复审（2026-10-01）
- 重新读了 issue，确认修复对应报告中的根因（`split("/")` 取前两段）。
- 自己复现了 red→green：还原 lib 改动后新用例失败（请求 `projects/bitbucket/repos/scm`）；恢复后 `LANG=C.UTF-8 bundle exec rspec spec/lib/danger/request_sources spec/lib/danger/ci_sources` → 690 examples, 0 failures；`bundle exec rubocop lib spec` → 213 files, no offenses。
- 在 upstream master 的全新浅克隆上 `git am` 能干净应用；作者为 anyingiit，patch 里没有 AI 模型名。
- 用 `pulls?q=is:pr bitbucket scm` 再查了一次，没有重复 PR。

## 需要提交者注意
- 仓库没有 AI 政策、CONTRIBUTING 或 DCO，也不需要 AI trailer。PR 正文里使用了标准 disclosure 段落。
- PR 模板要求：改动 lib/ 必须带 CHANGELOG 条目（已加），PR 正文不能为空（已满足）。
- CHANGELOG 条目现在链接的是 issue `#1327`，而已有条目链接的都是 PR。开出 PR 后，建议把链接改成 `[#<PR号>](https://github.com/danger/danger/pull/<PR号>)`，再 amend 并 force-push。

## 如何提交
```bash
git clone https://github.com/danger/danger && cd danger
git checkout -b fix/bitbucket-server-repo-slug-context-path origin/master
git am /home/user/Playground/contributions/117-danger-danger-1327/0001-Fix-Bitbucket-Server-repo-slug-with-context-path-or-.patch
bundle install && bundle exec rspec spec/lib/danger/request_sources/bitbucket_server_spec.rb && bundle exec rubocop lib spec
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/117-danger-danger-1327 danger/danger master fix/bitbucket-server-repo-slug-context-path contributions/117-danger-danger-1327/pr_title.txt contributions/117-danger-danger-1327/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
