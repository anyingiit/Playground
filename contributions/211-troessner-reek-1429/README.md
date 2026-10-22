# 211 — troessner/reek#1429: 管道输入 + --stdin-filename 时忽略 exclude_paths

| 项 | 内容 |
|---|---|
| Issue | https://github.com/troessner/reek/issues/1429 |
| 层级 | 自由（Ruby，约 4k stars，维护者 mvz 近期持续提交） |
| Labels | defect |
| Base 分支 | `master`（补丁基于 e8511a3） |
| 状态 | ✅ 可提交 |
| 重复检查 | 2026-10-22：issue 无指派、无关联 PR；`/pulls?q=stdin` 无 open PR。报告人 2018 年说过愿意提 PR，之后 8 年无动静，视为失效 |
| AI 政策 | CONTRIBUTING / .github 均无 AI 条款 |
| CLA/DCO | 无 |

## 问题理解
用 `--stdin-filename` 管道传代码时，`Application#source_from_pipe` 直接构造源码，不走 `SourceLocator` 的排除逻辑，所以 `exclude_paths`（含 `--force-exclusion`）完全无效。维护者 mvz 在 issue 下确认是 bug，并认可"抽取 SourceLocator 的排除逻辑复用"的思路，欢迎 PR。

## 改动
- `SourceLocator`：私有 `ignore_file?` 改为公开 `excluded_file?(path)`（逻辑不变，加 YARD 注释）。
- `Application#source_from_pipe`：有 stdin filename 且被排除时返回 `[]`。语义与命令行传文件一致：直接列出的文件排除；目录下的文件只在 `--force-exclusion` 时排除。
- 最初把检查放在单独私有方法里，触发 reek 自检 `TooManyMethods`（Application 16 个方法），改为内联。
- 测试：stdin.feature 两个场景；source_locator_spec 新增 `#excluded_file?` 三个用例。
- 注意：`exclude_paths` 用 `Dir[]` 展开，只匹配磁盘上存在的路径，所以 feature 里先建空文件（与编辑器集成的真实情形一致）。

## 验证
- 红：master 上新 feature 两个场景失败（exit 2 有 smell）；绿：带修复 8 scenarios 全过。
- `bundle exec rake ci`（Ruby 3.3.6）：spec 1120/0 失败；features 127 scenarios 全过；rubocop 无问题；quality 134/0 失败。exit 0。

## 需要提交者注意
- CHANGELOG 由维护者发版时写（条目带 PR 号），未改；PR 正文已说明。
- 仓库没有 PR 模板。

## 如何提交
```
git clone https://github.com/troessner/reek && cd reek && git checkout -b stdin-filename-exclusion origin/master
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
另一 agent：新克隆 `git am` 成功；`rake ci` 全绿（spec 1120/0、features 127、rubocop 0、quality 134/0）；回退 lib 后两个新场景失败（红）；核对了 `./`、绝对路径、`..`、`-f json`、无 `--stdin-filename` 等边界；issue/PR 无竞争。结论：OK。
