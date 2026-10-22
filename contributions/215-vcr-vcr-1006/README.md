# 215 — vcr/vcr#1006: 修改 cassette 的 match_requests_on 会改掉全局默认值

| 项 | 内容 |
|---|---|
| Issue | https://github.com/vcr/vcr/issues/1006 |
| 层级 | 高星（约 6.1k stars） |
| Base 分支 | `master`（补丁基于 a747bb6） |
| 状态 | ✅ 可提交 |
| 重复检查 | 2026-10-22：无指派、无关联 PR；`pulls?q=default_cassette_options`、`match_requests_on` 无相关 PR |
| AI 政策 | 无 AI 条款；无 CLA/DCO；无 PR 模板 |
| 许可证 | Hippocratic 2.1 |

## 问题理解
`Cassette#initialize` 用 `default_cassette_options.merge(options)` 浅合并，cassette 与全局配置共享同一个数组；`cassette.match_requests_on << :body` 会污染后续所有 cassette。协作者 galori 问过是否只让全局配置全局生效、单 cassette 修改保持局部，作者确认是。另发现 `assign_tags` 会把 `:preserve_exact_body_bytes` 等标签追加进默认 `tags` 数组（VCR 自身就会触发）。

## 改动
- 新私有方法 `default_options`：对 Array/Hash 类型的默认值 `dup` 后再合并。其他值原样传递。
- 两个新 spec（match_requests_on、tags），无修复时均失败。
- CHANGELOG 未发布区加一行（沿用 "(#issue) by @user" 格式）。

## 验证
- 红：2 个新 spec 在 master 上失败（got `[:uri, :method, :body]` / `[:foo, :preserve_exact_body_bytes]`）。
- 绿：`bundle exec rspec` 1999 例 0 失败 1 pending（原有）；`bundle exec cucumber features/` 258 场景全过。
- 本地需 `libcurl4-openssl-dev`（patron/curb 依赖）。CI 的 `fail_if_warnings` 在本机因第三方 gem 警告失败，与本改动无关。

## 如何提交
```
git clone https://github.com/vcr/vcr && cd vcr && git checkout -b cassette-default-options-dup origin/master
git am /path/to/0001-*.patch
```

## 独立复核
- 独立 agent 复核：OK（仅需改 star 数，已改）。复现 rspec 1999/0/1 及无修复时 2 个新 spec 失败；确认无调用方依赖 options 与默认值同一对象，浅 dup 足够，Ruby ≥2.4 可用；无竞争 PR（`1006`、`cassette options`、`dup` 搜索）。
- 已知范围外：用户单个 cassette 传入的 `tags:` 数组仍会被 `assign_tags` 追加，未改。
