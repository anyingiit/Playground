# Upstream submissions

Tracker for PRs opened from `anyingiit` (2026-09-25). Refresh with `python3 tools/pr_status.py`.
Submit helper: `tools/submit_pr.sh` (author = `anyingiit <49945850+anyingiit@users.noreply.github.com>`).

| # | Issue | PR | 备注 |
|---|---|---|---|
| 001 | [medusajs/medusa#16969](https://github.com/medusajs/medusa/issues/16969) | — | 放弃：已有 2 个竞争 PR（#16970、#16973） |
| 002 | [wasmCloud/wasmCloud#5607](https://github.com/wasmCloud/wasmCloud/issues/5607) | — | 放弃：已由 #5609 修复并关闭 |
| 003 | [mloda-ai/mloda#1642](https://github.com/mloda-ai/mloda/issues/1642) | [mloda-ai/mloda#1649](https://github.com/mloda-ai/mloda/pull/1649) | ✅ 已合并 |
| 004 | [aethersdr/AetherSDR#5944](https://github.com/aethersdr/AetherSDR/issues/5944) | — | 放弃：项目自有 AI 流程按标签审批（aetherclaude-eligible），维护者待定设计 |
| 005 | [MakazhanAlpamys/Soup#1224](https://github.com/MakazhanAlpamys/Soup/issues/1224) | [MakazhanAlpamys/Soup#1260](https://github.com/MakazhanAlpamys/Soup/pull/1260) | ✅ 已合并 |
| 006 | [uutils/coreutils#9060](https://github.com/uutils/coreutils/issues/9060) | [uutils/coreutils#14853](https://github.com/uutils/coreutils/pull/14853) | ✅ 已合并（2026-09-25） |
| 007 | [MakazhanAlpamys/Soup#1221](https://github.com/MakazhanAlpamys/Soup/issues/1221) | [MakazhanAlpamys/Soup#1261](https://github.com/MakazhanAlpamys/Soup/pull/1261) | ✅ 已合并 |
| 008 | [mloda-ai/mloda-registry#742](https://github.com/mloda-ai/mloda-registry/issues/742) | [mloda-ai/mloda-registry#752](https://github.com/mloda-ai/mloda-registry/pull/752) | ✅ 已合并 |
| 009 | [getsotto/sotto#393](https://github.com/getsotto/sotto/issues/393) | [getsotto/sotto#400](https://github.com/getsotto/sotto/pull/400) | ✅ 已合并（2026-09-25） |
| 010 | [go-git/go-git#1518](https://github.com/go-git/go-git/issues/1518) | [go-git/go-git#2423](https://github.com/go-git/go-git/pull/2423) | 维护者 pjbgf（09-30）：失败测试与本 PR 无关，请 rebase 解决冲突 → 已在 main@a9ce94f 上 rebase（冲突仅 #2354 新增的 TestPushPruneForceRefSpec，移入 remote_push_test.go），测试集与 main 一致；待 owner force-push `followup-0001-rebased-onto-main-a9ce94f.patch` 并回复 |
| 011 | [thebanri/limoni#59](https://github.com/thebanri/limoni/issues/59) | — | 放弃：竞争 PR #64 于 2026-09-25 开出 |
| 012 | [openeverest/provider-cassandra#23](https://github.com/openeverest/provider-cassandra/issues/23) | [openeverest/provider-cassandra#30](https://github.com/openeverest/provider-cassandra/pull/30) | 暂无 review/评论；DCO ✅，CI 待维护者批准运行（10-01 检查） |
| 013 | [fadyehabamer/qr-zero#4](https://github.com/fadyehabamer/qr-zero/issues/4) | [fadyehabamer/qr-zero#13](https://github.com/fadyehabamer/qr-zero/pull/13) | 维护者 CHANGES_REQUESTED（--module-size 需 isSafeInteger）→ 已推送修复 1f62578 + 用例（114/114）并回复（09-29）；之后无新动态，等待复审（10-01） |
| 014 | [Mozart2234/herdr-agent-pulse#1](https://github.com/Mozart2234/herdr-agent-pulse/issues/1) | [Mozart2234/herdr-agent-pulse#12](https://github.com/Mozart2234/herdr-agent-pulse/pull/12) | 暂无 review/评论；CI 未运行（首次贡献者 workflow 待批准）（10-01 检查） |
| 015 | [ezedike-evan/corridor-in-a-box#239](https://github.com/ezedike-evan/corridor-in-a-box/issues/239) | [ezedike-evan/corridor-in-a-box#313](https://github.com/ezedike-evan/corridor-in-a-box/pull/313) | ✅ 已合并 |
| 016 | [cubrid-lab/pycubrid#371](https://github.com/cubrid-lab/pycubrid/issues/371) | — | 放弃（2026-09-29）：上游 API 清单（#438 决策）要求 fetchmany(0/-1) 保留返回 []，补丁与之冲突，且异步游标失效语义已变；在最新 main 上 9 个测试失败，返工代价大 |
| 017 | [smol-machines/smolvm#1385](https://github.com/smol-machines/smolvm/issues/1385) | — | 放弃：竞争 PR #1392 |
| 018 | [inokawa/remark-pdf#61](https://github.com/inokawa/remark-pdf/issues/61) | [inokawa/remark-pdf#73](https://github.com/inokawa/remark-pdf/pull/73) | 暂无 review/评论；CI 未运行（待批准）（10-01 检查） |
| 019 | [eclipse-paho/paho.mqtt.golang#798](https://github.com/eclipse-paho/paho.mqtt.golang/issues/798) | [eclipse-paho/paho.mqtt.golang#801](https://github.com/eclipse-paho/paho.mqtt.golang/pull/801) | ✅ 已合并（2026-09-29，MattBrittan） |
| 020 | [BfArM-MVH/grz-tools#622](https://github.com/BfArM-MVH/grz-tools/issues/622) | — | 阻塞：仓库只允许协作者创建 PR（FORBIDDEN）；分支 anyingiit/grz-tools:fix/alembic-url-password 已推送 |
| 022 | [etiennebacher/jarl#491](https://github.com/etiennebacher/jarl/issues/491) | — | 跳过：要求 PR 描述人写 |
| 023 | [denoland/std#3964](https://github.com/denoland/std/issues/3964) | [denoland/std#7332](https://github.com/denoland/std/pull/7332) | CLA 已签；暂无 review；CI 运行中/待定，codecov 报 patch 有 3 行未覆盖（未被要求处理）（10-01 检查） |
| 024 | [flint-fyi/flint#2164](https://github.com/flint-fyi/flint/issues/2164) | — | 跳过：要求 PR 描述人写 |
| 025 | [Smaug6739/Alexandrie#781](https://github.com/Smaug6739/Alexandrie/issues/781) | [Smaug6739/Alexandrie#786](https://github.com/Smaug6739/Alexandrie/pull/786) | 暂无 review/评论；CI 未运行（待批准）（10-01 检查） |
| 026 | [DioxusLabs/taffy#835](https://github.com/DioxusLabs/taffy/issues/835) | — | 跳过：维护者要求文档用自己的话写（Bevy AI 政策），同 jarl/flint/biome |
| 027 | [webgpu-tools/wesl-rs#256](https://github.com/webgpu-tools/wesl-rs/issues/256) | [webgpu-tools/wesl-rs#304](https://github.com/webgpu-tools/wesl-rs/pull/304) | ✅ 已合并 |
| 028 | [LargeModGames/spotatui#554](https://github.com/LargeModGames/spotatui/issues/554) | [LargeModGames/spotatui#576](https://github.com/LargeModGames/spotatui/pull/576) | 已关闭（放弃）：CodeRabbit 请求修改，按 owner 决定不返工 |
| 029 | [biomejs/biome#8762](https://github.com/biomejs/biome/issues/8762) | — | 跳过：要求 PR 描述人写 |
| 030 | [librasn/rasn#55](https://github.com/librasn/rasn/issues/55) | [librasn/rasn#573](https://github.com/librasn/rasn/pull/573) | ✅ 已合并（2026-09-25） |
| 031 | [MudBlazor/MudBlazor#3461](https://github.com/MudBlazor/MudBlazor/issues/3461) | — | 跳过：要求 before/after 录像 |
| 032 | [celler-cache/celler#75](https://github.com/celler-cache/celler/issues/75) | [celler-cache/celler#96](https://github.com/celler-cache/celler/pull/96) | 已关闭（10-01，blitz）：被 #97 取代（"approach is very convoluted"，直接删除 ConfigWriteGuard）；无需操作 |
| 033 | [brig-sh/brig#176](https://github.com/brig-sh/brig/issues/176) | [brig-sh/brig#326](https://github.com/brig-sh/brig/pull/326) | draft；暂无 review；CI/DCO workflow "completed with no jobs"（首次贡献者待批准），CI 绿后再 `gh pr ready 326 -R brig-sh/brig`（10-01 检查） |
| 034 | [pmd/pmd#7100](https://github.com/pmd/pmd/issues/7100) | [pmd/pmd#7110](https://github.com/pmd/pmd/pull/7110) | ✅ 已合并 |
| 035 | [csaf-rs/csaf#736](https://github.com/csaf-rs/csaf/issues/736) | [csaf-rs/csaf#1122](https://github.com/csaf-rs/csaf/pull/1122) | ✅ 已合并 |
| 036 | [complytime/complyctl#881](https://github.com/complytime/complyctl/issues/881) | [complytime/complyctl#883](https://github.com/complytime/complyctl/pull/883) | ✅ 已合并（2026-09-29，marcusburghardt；yvonnedevlinrh 也已 approve） |
| 037 | [ruby/rdoc#1743](https://github.com/ruby/rdoc/issues/1743) | [ruby/rdoc#1833](https://github.com/ruby/rdoc/pull/1833) | ✅ 已合并（2026-09-25） |
| 038 | [rnag/dataclass-wizard#219](https://github.com/rnag/dataclass-wizard/issues/219) | [rnag/dataclass-wizard#258](https://github.com/rnag/dataclass-wizard/pull/258) | 暂无 review/评论；CI 未运行（待批准）（10-01 检查） |
| 039 | [vimeo/psalm#6866](https://github.com/vimeo/psalm/issues/6866) | [vimeo/psalm#11990](https://github.com/vimeo/psalm/pull/11990) | ✅ 已合并（2026-09-25） |
| 040 | [ulyssa/iamb#617](https://github.com/ulyssa/iamb/issues/617) | [ulyssa/iamb#745](https://github.com/ulyssa/iamb/pull/745) | ✅ 已合并（2026-09-25） |
| 041 | [pyrite-wiki/pyrite#363](https://github.com/pyrite-wiki/pyrite/issues/363) | [pyrite-wiki/pyrite#398](https://github.com/pyrite-wiki/pyrite/pull/398) | 已关闭（放弃）：需按维护者 groom 评论返工，按 owner 决定不做 |
| 042 | [ProjectMirador/mirador#4071](https://github.com/ProjectMirador/mirador/issues/4071) | [ProjectMirador/mirador#4553](https://github.com/ProjectMirador/mirador/pull/4553) | 已关闭（09-30，marlo-longley）：认为 canvasIndex 不是正式配置项、可用 canvasId 替代、近乎死代码；dnoneill（已 approve）关闭后表示不同意。按 owner 规则不返工；可选择留言致谢 |
| 043 | [cubrid-lab/sqlalchemy-cubrid#440](https://github.com/cubrid-lab/sqlalchemy-cubrid/issues/440) | [cubrid-lab/sqlalchemy-cubrid#456](https://github.com/cubrid-lab/sqlalchemy-cubrid/pull/456) | ✅ 已合并 |
| 044 | [pasteurlabs/tesseract-core#768](https://github.com/pasteurlabs/tesseract-core/issues/768) | [pasteurlabs/tesseract-core#793](https://github.com/pasteurlabs/tesseract-core/pull/793) | ✅ 已合并（2026-09-25） |
| 045 | [fsspec/projspec#69](https://github.com/fsspec/projspec/issues/69) | [fsspec/projspec#111](https://github.com/fsspec/projspec/pull/111) | ✅ 已合并 |

## 接续说明（2026-09-25 快照）

状态（2026-10-01 UTC）：19 个已合并，9 个开着，celler#96、mirador#4553 已被维护者关闭（见表）

**待办 / 下次会话从这里继续**
1. 跑 `python3 tools/pr_status.py`（需 `gh auth login`；脚本会自动去掉受限的 Codespaces `GITHUB_TOKEN`），看 review、CI、合并情况。
2. ~~taffy #835（26）~~：已跳过（需人写文档）。
3. **brig#326（33）**：draft；CI 获批并通过后 `gh pr ready 326 -R brig-sh/brig`（CONTRIBUTING 要求）。
4. ~~pycubrid #371（16）~~：已放弃（上游约定变更）。
5. rasn#573 的 CI 失败来自上游 main（32 位 `view_bits`），非本改动；上游修复后可 rebase 以得到绿色 CI。

**处理规则（owner 决定）**
- 需要返工的 PR（review 要求改动 / CI 因本改动失败）→ 直接关闭并简短致歉，不返工。
- 需要 owner 本人做的事（签协议、在 issue 留言、人写描述）→ 列出并引导 owner 操作；不代发评论。
- commit 作者、Signed-off-by 等公开邮箱一律用 `anyingiit <49945850+anyingiit@users.noreply.github.com>`。
- DCO 可代签；上游要求 AI trailer 时按上游（`Assisted-by: Claude Code (claude-opus-5-5)`）。
