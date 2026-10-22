# Muvon/octomind#235 — `/image` and `/video` fail on `~/` paths

| 项 | 值 |
|---|---|
| Issue | https://github.com/Muvon/octomind/issues/235 （同批 #236/#237/#238 亦同） |
| Tier | 自由 |
| Labels | E-easy, bug, good first issue, help wanted |
| Status | ⏭️ skipped — issue 正文明确禁止 agent 认领/解决 |

## 跳过原因

Issue 正文 contributor-process 段原文："This issue is meant for a person learning the codebase, so disclose any AI help, and don't let an agent claim or solve it."
#236 也有同样语句。Muvon/octomind 这批 good first issue（#235–#238，donk8r 2026-10-22 创建）都按同一模板写，全部不做。

已在本地实现过（`CommandCompleter::expand_tilde` 改 `pub(crate)` 并在两个 attach 函数里使用），发现该语句后放弃，未保留补丁。

教训：这类新模板 issue 要先全文搜 "agent" / "person learning"。
