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
| 010 | [go-git/go-git#1518](https://github.com/go-git/go-git/issues/1518) | [go-git/go-git#2423](https://github.com/go-git/go-git/pull/2423) | 10-22：已 rebase 到最新 main，冲突仅 TestPushPruneForceRefSpec（移入 remote_push_test.go），函数集与测试集与 main 一致、RemoteSuite 通过；已 force-push（95c6b804）并回复 pjbgf，等复审 |
| 011 | [thebanri/limoni#59](https://github.com/thebanri/limoni/issues/59) | — | 放弃：竞争 PR #64 于 2026-09-25 开出 |
| 012 | [openeverest/provider-cassandra#23](https://github.com/openeverest/provider-cassandra/issues/23) | [openeverest/provider-cassandra#30](https://github.com/openeverest/provider-cassandra/pull/30) | 已关闭（10-07，spron-in）：改用 core 的 schedulingPolicy.affinity 统一契约，被 #36 取代；维护者肯定了分析。无需操作 |
| 013 | [fadyehabamer/qr-zero#4](https://github.com/fadyehabamer/qr-zero/issues/4) | [fadyehabamer/qr-zero#13](https://github.com/fadyehabamer/qr-zero/pull/13) | 维护者 CHANGES_REQUESTED → 已修复 1f62578（09-29）；10-22 已发提醒评论，等复审 |
| 014 | [Mozart2234/herdr-agent-pulse#1](https://github.com/Mozart2234/herdr-agent-pulse/issues/1) | [Mozart2234/herdr-agent-pulse#12](https://github.com/Mozart2234/herdr-agent-pulse/pull/12) | 暂无 review/评论（10-22 复查无变化） |
| 015 | [ezedike-evan/corridor-in-a-box#239](https://github.com/ezedike-evan/corridor-in-a-box/issues/239) | [ezedike-evan/corridor-in-a-box#313](https://github.com/ezedike-evan/corridor-in-a-box/pull/313) | ✅ 已合并 |
| 016 | [cubrid-lab/pycubrid#371](https://github.com/cubrid-lab/pycubrid/issues/371) | — | 放弃（2026-09-29）：上游 API 清单（#438 决策）要求 fetchmany(0/-1) 保留返回 []，补丁与之冲突，且异步游标失效语义已变；在最新 main 上 9 个测试失败，返工代价大 |
| 017 | [smol-machines/smolvm#1385](https://github.com/smol-machines/smolvm/issues/1385) | — | 放弃：竞争 PR #1392 |
| 018 | [inokawa/remark-pdf#61](https://github.com/inokawa/remark-pdf/issues/61) | [inokawa/remark-pdf#73](https://github.com/inokawa/remark-pdf/pull/73) | 暂无 review/评论（10-22 复查无变化） |
| 019 | [eclipse-paho/paho.mqtt.golang#798](https://github.com/eclipse-paho/paho.mqtt.golang/issues/798) | [eclipse-paho/paho.mqtt.golang#801](https://github.com/eclipse-paho/paho.mqtt.golang/pull/801) | ✅ 已合并（2026-09-29，MattBrittan） |
| 020 | [BfArM-MVH/grz-tools#622](https://github.com/BfArM-MVH/grz-tools/issues/622) | — | 阻塞：仓库只允许协作者创建 PR（FORBIDDEN）；分支 anyingiit/grz-tools:fix/alembic-url-password 已推送 |
| 022 | [etiennebacher/jarl#491](https://github.com/etiennebacher/jarl/issues/491) | — | 跳过：要求 PR 描述人写 |
| 023 | [denoland/std#3964](https://github.com/denoland/std/issues/3964) | [denoland/std#7332](https://github.com/denoland/std/pull/7332) | CLA 已签；CI 全绿（17/17）；仍无 review（10-22 复查） |
| 024 | [flint-fyi/flint#2164](https://github.com/flint-fyi/flint/issues/2164) | — | 跳过：要求 PR 描述人写 |
| 025 | [Smaug6739/Alexandrie#781](https://github.com/Smaug6739/Alexandrie/issues/781) | [Smaug6739/Alexandrie#786](https://github.com/Smaug6739/Alexandrie/pull/786) | ✅ 已合并（2026-10-18，Smaug6739） |
| 026 | [DioxusLabs/taffy#835](https://github.com/DioxusLabs/taffy/issues/835) | — | 跳过：维护者要求文档用自己的话写（Bevy AI 政策），同 jarl/flint/biome |
| 027 | [webgpu-tools/wesl-rs#256](https://github.com/webgpu-tools/wesl-rs/issues/256) | [webgpu-tools/wesl-rs#304](https://github.com/webgpu-tools/wesl-rs/pull/304) | ✅ 已合并 |
| 028 | [LargeModGames/spotatui#554](https://github.com/LargeModGames/spotatui/issues/554) | [LargeModGames/spotatui#576](https://github.com/LargeModGames/spotatui/pull/576) | 已关闭（放弃）：CodeRabbit 请求修改，按 owner 决定不返工 |
| 029 | [biomejs/biome#8762](https://github.com/biomejs/biome/issues/8762) | — | 跳过：要求 PR 描述人写 |
| 030 | [librasn/rasn#55](https://github.com/librasn/rasn/issues/55) | [librasn/rasn#573](https://github.com/librasn/rasn/pull/573) | ✅ 已合并（2026-09-25） |
| 031 | [MudBlazor/MudBlazor#3461](https://github.com/MudBlazor/MudBlazor/issues/3461) | — | 跳过：要求 before/after 录像 |
| 032 | [celler-cache/celler#75](https://github.com/celler-cache/celler/issues/75) | [celler-cache/celler#96](https://github.com/celler-cache/celler/pull/96) | 已关闭（10-01，blitz）：被 #97 取代（"approach is very convoluted"，直接删除 ConfigWriteGuard）；无需操作 |
| 033 | [brig-sh/brig#176](https://github.com/brig-sh/brig/issues/176) | [brig-sh/brig#326](https://github.com/brig-sh/brig/pull/326) | draft；CI/DCO 仍是 action_required（首次贡献者待维护者批准），按 CONTRIBUTING 绿了才能标 ready（10-22） |
| 034 | [pmd/pmd#7100](https://github.com/pmd/pmd/issues/7100) | [pmd/pmd#7110](https://github.com/pmd/pmd/pull/7110) | ✅ 已合并 |
| 035 | [csaf-rs/csaf#736](https://github.com/csaf-rs/csaf/issues/736) | [csaf-rs/csaf#1122](https://github.com/csaf-rs/csaf/pull/1122) | ✅ 已合并 |
| 036 | [complytime/complyctl#881](https://github.com/complytime/complyctl/issues/881) | [complytime/complyctl#883](https://github.com/complytime/complyctl/pull/883) | ✅ 已合并（2026-09-29，marcusburghardt；yvonnedevlinrh 也已 approve） |
| 037 | [ruby/rdoc#1743](https://github.com/ruby/rdoc/issues/1743) | [ruby/rdoc#1833](https://github.com/ruby/rdoc/pull/1833) | ✅ 已合并（2026-09-25） |
| 038 | [rnag/dataclass-wizard#219](https://github.com/rnag/dataclass-wizard/issues/219) | [rnag/dataclass-wizard#258](https://github.com/rnag/dataclass-wizard/pull/258) | 暂无 review/评论（10-22 复查无变化） |
| 039 | [vimeo/psalm#6866](https://github.com/vimeo/psalm/issues/6866) | [vimeo/psalm#11990](https://github.com/vimeo/psalm/pull/11990) | ✅ 已合并（2026-09-25） |
| 040 | [ulyssa/iamb#617](https://github.com/ulyssa/iamb/issues/617) | [ulyssa/iamb#745](https://github.com/ulyssa/iamb/pull/745) | ✅ 已合并（2026-09-25） |
| 041 | [pyrite-wiki/pyrite#363](https://github.com/pyrite-wiki/pyrite/issues/363) | [pyrite-wiki/pyrite#398](https://github.com/pyrite-wiki/pyrite/pull/398) | 已关闭（放弃）：需按维护者 groom 评论返工，按 owner 决定不做 |
| 042 | [ProjectMirador/mirador#4071](https://github.com/ProjectMirador/mirador/issues/4071) | [ProjectMirador/mirador#4553](https://github.com/ProjectMirador/mirador/pull/4553) | 已关闭（09-30，marlo-longley）：认为 canvasIndex 不是正式配置项、可用 canvasId 替代、近乎死代码；dnoneill（已 approve）关闭后表示不同意。按 owner 规则不返工；可选择留言致谢 |
| 043 | [cubrid-lab/sqlalchemy-cubrid#440](https://github.com/cubrid-lab/sqlalchemy-cubrid/issues/440) | [cubrid-lab/sqlalchemy-cubrid#456](https://github.com/cubrid-lab/sqlalchemy-cubrid/pull/456) | ✅ 已合并 |
| 044 | [pasteurlabs/tesseract-core#768](https://github.com/pasteurlabs/tesseract-core/issues/768) | [pasteurlabs/tesseract-core#793](https://github.com/pasteurlabs/tesseract-core/pull/793) | ✅ 已合并（2026-09-25） |
| 045 | [fsspec/projspec#69](https://github.com/fsspec/projspec/issues/69) | [fsspec/projspec#111](https://github.com/fsspec/projspec/pull/111) | ✅ 已合并 |


## 第二轮（2026-10-02 提交，10-22 复查）

第二轮 125 个可提交中已提交 **19** 个：10 个已合并、1 个关闭但修复已进上游（i18n-tasks）、8 个开着。其余 106 个未提交。

| # | Issue | PR | 备注 |
|---|---|---|---|
| 046 | [symfony/ai#2430](https://github.com/symfony/ai/issues/2430) | [symfony/ai#2634](https://github.com/symfony/ai/pull/2634) | ✅ 已合并（2026-10-06，wachterjohannes） |
| 049 | [microsoft/litebox#1222](https://github.com/microsoft/litebox/issues/1222) | [microsoft/litebox#1481](https://github.com/microsoft/litebox/pull/1481) | 已关闭（10-22，owner 确认）：上游 #1594（10-15）已在 main 落地同一修复；CLA 已签。无需操作 |
| 052 | [eugenioenko/ttt#277](https://github.com/eugenioenko/ttt/issues/277) | [eugenioenko/ttt#698](https://github.com/eugenioenko/ttt/pull/698) | ✅ 已合并（2026-10-02） |
| 053 | [zerobrewhq/zerobrew#357](https://github.com/zerobrewhq/zerobrew/issues/357) | [zerobrewhq/zerobrew#479](https://github.com/zerobrewhq/zerobrew/pull/479) | 10-22 提交（rustc 1.96 下红→绿） |
| 054 | [kubecolor/kubecolor#171](https://github.com/kubecolor/kubecolor/issues/171) | [kubecolor/kubecolor#370](https://github.com/kubecolor/kubecolor/pull/370) | ✅ 已合并（2026-10-17，applejag） |
| 056 | [stackrox/kube-linter#1241](https://github.com/stackrox/kube-linter/issues/1241) | [stackrox/kube-linter#1273](https://github.com/stackrox/kube-linter/pull/1273) | 待 review；CodeRabbit 无意见；只有 codecov/project 失败（非必需） |
| 057 | [helm-unittest/helm-unittest#848](https://github.com/helm-unittest/helm-unittest/issues/848) | [helm-unittest/helm-unittest#941](https://github.com/helm-unittest/helm-unittest/pull/941) | ✅ 已合并（2026-10-09，quintush） |
| 058 | [arxanas/git-branchless#498](https://github.com/arxanas/git-branchless/issues/498) | [arxanas/git-branchless#1702](https://github.com/arxanas/git-branchless/pull/1702) | 10-22 提交 |
| 059 | [sds/overcommit#822](https://github.com/sds/overcommit/issues/822) | [sds/overcommit#900](https://github.com/sds/overcommit/pull/900) | ✅ 已合并（2026-10-15，sds） |
| 060 | [glebm/i18n-tasks#746](https://github.com/glebm/i18n-tasks/issues/746) | [glebm/i18n-tasks#759](https://github.com/glebm/i18n-tasks/pull/759) | 已关闭（10-10，davidwessman）：因合并冲突由维护者以同名 #763 重新提交并合并，修复已进上游。无需操作 |
| 061 | [cashapp/licensee#545](https://github.com/cashapp/licensee/issues/545) | [cashapp/licensee#636](https://github.com/cashapp/licensee/pull/636) | ✅ 已合并（2026-10-03，JakeWharton） |
| 062 | [open-policy-agent/conftest#1022](https://github.com/open-policy-agent/conftest/issues/1022) | [open-policy-agent/conftest#1437](https://github.com/open-policy-agent/conftest/pull/1437) | 待 review；CI 通过 |
| 064 | [GREsau/schemars#536](https://github.com/GREsau/schemars/issues/536) | [GREsau/schemars#543](https://github.com/GREsau/schemars/pull/543) | 10-22 提交，待 review |
| 065 | [gosnmp/gosnmp#591](https://github.com/gosnmp/gosnmp/issues/591) | [gosnmp/gosnmp#624](https://github.com/gosnmp/gosnmp/pull/624) | ✅ 已合并（2026-10-21，SuperQ） |
| 066 | [suzuki-shunsuke/pinact#1448](https://github.com/suzuki-shunsuke/pinact/issues/1448) | [suzuki-shunsuke/pinact#1745](https://github.com/suzuki-shunsuke/pinact/pull/1745) | 待 review；CI 通过 |
| 067 | [embedded-graphics/embedded-graphics#821](https://github.com/embedded-graphics/embedded-graphics/issues/821) | [embedded-graphics/embedded-graphics#830](https://github.com/embedded-graphics/embedded-graphics/pull/830) | 待 review；CI 未运行 |
| 068 | [rust-embedded/heapless#492](https://github.com/rust-embedded/heapless/issues/492) | [rust-embedded/heapless#692](https://github.com/rust-embedded/heapless/pull/692) | 10-22 已 rebase 到最新 main（无冲突，linear_map 测试 17/17、fmt 通过）、force-push（2961d8e3），PR 描述改为简短版本；现在 MERGEABLE，auto-merge 已失效需维护者重开 |
| 069 | [jam1garner/binrw#370](https://github.com/jam1garner/binrw/issues/370) | [jam1garner/binrw#372](https://github.com/jam1garner/binrw/pull/372) | 待 review；CI 未运行 |
| 070 | [typstyle-rs/typstyle#478](https://github.com/typstyle-rs/typstyle/issues/478) | [typstyle-rs/typstyle#521](https://github.com/typstyle-rs/typstyle/pull/521) | 10-22 提交 |
| 071 | [go-jet/jet#609](https://github.com/go-jet/jet/issues/609) | [go-jet/jet#621](https://github.com/go-jet/jet/pull/621) | ✅ 已合并（2026-10-05） |
| 072 | [vega/altair#3619](https://github.com/vega/altair/issues/3619) | [vega/altair#4162](https://github.com/vega/altair/pull/4162) | 待 review；CI 全绿（16/16） |
| 074 | [zitadel/oidc#967](https://github.com/zitadel/oidc/issues/967) | [zitadel/oidc#994](https://github.com/zitadel/oidc/pull/994) | 维护者 wim07101993 暂缓（10-02）：不确定是否该修，已在 issue 下开讨论；失败的 check 只是 kanban 机器人 |
| 076 | [gkampitakis/go-snaps#156](https://github.com/gkampitakis/go-snaps/issues/156) | [gkampitakis/go-snaps#162](https://github.com/gkampitakis/go-snaps/pull/162) | 10-22 提交 |
| 078 | [image-rs/image-png#720](https://github.com/image-rs/image-png/issues/720) | [image-rs/image-png#723](https://github.com/image-rs/image-png/pull/723) | 10-22 提交 |
| 081 | [samber/ro#74](https://github.com/samber/ro/issues/74) | [samber/ro#474](https://github.com/samber/ro/pull/474) | 10-22 提交 |
| 082 | [carthage-software/mago#2182](https://github.com/carthage-software/mago/issues/2182) | [carthage-software/mago#2417](https://github.com/carthage-software/mago/pull/2417) | ✅ 已合并（2026-10-03，azjezz） |
| 084 | [agavra/tuicr#597](https://github.com/agavra/tuicr/issues/597) | [agavra/tuicr#802](https://github.com/agavra/tuicr/pull/802) | 10-22 提交（在 #712/#797 之后重新移植） |
| 087 | [jnsahaj/lumen#156](https://github.com/jnsahaj/lumen/issues/156) | [jnsahaj/lumen#211](https://github.com/jnsahaj/lumen/pull/211) | 10-22 提交 |
| 130 | [rjsf-team/react-jsonschema-form#3882](https://github.com/rjsf-team/react-jsonschema-form/issues/3882) | [rjsf-team/react-jsonschema-form#5622](https://github.com/rjsf-team/react-jsonschema-form/pull/5622) | 2026-10-22 提交 |
| 140 | [marketcalls/openalgo#1849](https://github.com/marketcalls/openalgo/issues/1849) | [marketcalls/openalgo#2270](https://github.com/marketcalls/openalgo/pull/2270) | 2026-10-22 提交 |
| 142 | [jgrossi/elephpant.me#347](https://github.com/jgrossi/elephpant.me/issues/347) | [jgrossi/elephpant.me#386](https://github.com/jgrossi/elephpant.me/pull/386) | 2026-10-22 提交 |
| 146 | [github-linguist/linguist#7949](https://github.com/github-linguist/linguist/issues/7949) | [github-linguist/linguist#8288](https://github.com/github-linguist/linguist/pull/8288) | 2026-10-22 提交 |
| 150 | [infection/infection#2582](https://github.com/infection/infection/issues/2582) | [infection/infection#3699](https://github.com/infection/infection/pull/3699) | 2026-10-22 提交；变异测试门槛（MSI 100%）漏掉 `formatDiff` 的 ProtectedVisibility，已改为抽象方法并 force-push |
| 148 | [valkey-io/valkey-glide-ruby#309](https://github.com/valkey-io/valkey-glide-ruby/issues/309) | [valkey-io/valkey-glide-ruby#385](https://github.com/valkey-io/valkey-glide-ruby/pull/385) | 2026-10-22 提交；GPG 签名 + DCO；macOS arm64 上红→绿，test:unit 512/0 |
| 151 | [openrewrite/rewrite-cucumber-jvm#63](https://github.com/openrewrite/rewrite-cucumber-jvm/issues/63) | [openrewrite/rewrite-cucumber-jvm#73](https://github.com/openrewrite/rewrite-cucumber-jvm/pull/73) | 2026-10-22 提交；红 4/4 失败→绿 4/4 通过；check 157 例 6 失败与 main 相同（本地 rewrite 版本旧） |
| 153 | [lacs-project/sysknife#567](https://github.com/lacs-project/sysknife/issues/567) | [lacs-project/sysknife#639](https://github.com/lacs-project/sysknife/pull/639) | 2026-10-22 issue 下认领后提交；补丁含白名单 since；macOS 上 daemon lib 912 过 / 12 败，与 main 相同 |
| 137 | [OpenRefine/OpenRefine#5207](https://github.com/OpenRefine/OpenRefine/issues/5207) | [OpenRefine/OpenRefine#8036](https://github.com/OpenRefine/OpenRefine/pull/8036) | 2026-10-22 issue 下认领后提交；Cypress 红→绿；facet 目录 3 个失败与 master 相同；截图放在 fork 的 pr-assets-5207 分支 |
| 152 | [uutils/acl#21](https://github.com/uutils/acl/issues/21) | [uutils/acl#356](https://github.com/uutils/acl/pull/356) | 2026-10-22 提交 |
| 155 | [pmxt-dev/pmxt#2353](https://github.com/pmxt-dev/pmxt/issues/2353) | [pmxt-dev/pmxt#2586](https://github.com/pmxt-dev/pmxt/pull/2586) | 2026-10-22 提交 |
| 169 | [hanami/hanami#1284](https://github.com/hanami/hanami/issues/1284) | [hanami/hanami-cli#464](https://github.com/hanami/hanami-cli/pull/464) | 2026-10-22 提交；CHANGELOG 已填 PR 号 |
| 170 | [ruby-grape/grape#2487](https://github.com/ruby-grape/grape/issues/2487) | [ruby-grape/grape#3041](https://github.com/ruby-grape/grape/pull/3041) | 2026-10-22 提交；CHANGELOG 已填 PR 号 |
| 202 | [vega/altair#3502](https://github.com/vega/altair/issues/3502) | [vega/altair#4193](https://github.com/vega/altair/pull/4193) | 2026-10-22 提交（独立复核 PASS） |
| 208 | [image-rs/image-png#584](https://github.com/image-rs/image-png/issues/584) | [image-rs/image-png#722](https://github.com/image-rs/image-png/pull/722) | 2026-10-22 提交（独立复核 PASS） |
| 207 | [arxanas/git-branchless#1308](https://github.com/arxanas/git-branchless/issues/1308) | [arxanas/git-branchless#1703](https://github.com/arxanas/git-branchless/pull/1703) | 2026-10-22 提交（独立复核通过） |
| 206 | [stackrox/kube-linter#1194](https://github.com/stackrox/kube-linter/issues/1194) | [stackrox/kube-linter#1280](https://github.com/stackrox/kube-linter/pull/1280) | 2026-10-22 提交（独立复核通过） |
| 200 | [plotly/plotly.py#2059](https://github.com/plotly/plotly.py/issues/2059) | [plotly/plotly.py#5839](https://github.com/plotly/plotly.py/pull/5839) | 2026-10-22 提交（独立复核通过）；CHANGELOG 已填 PR 号 |

## 接续说明（2026-09-25 快照）

状态（2026-10-22 UTC 复查）：第一轮 20 个已合并、7 个开着（010、013、014、018、023、033、038），provider-cassandra#30 于 10-07 被维护者关闭；第二轮见上表

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

## 第二轮提交（2026-10-22，088–129 线程，前半段）

| # | PR |
|---|---|
| 089 | https://github.com/NLog/NLog/pull/6313 |
| 090 | https://github.com/grpc-ecosystem/grpc-gateway/pull/7562 |
| 091 | https://github.com/ipython/ipython/pull/15448 |
| 092 | https://github.com/pyinstaller/pyinstaller/pull/9555 |
| 094 | https://github.com/OpsiMate/OpsiMate/pull/1293 |
| 098 | https://github.com/Adam-Vandervorst/PathMap/pull/167 |
| 100 | https://github.com/phpmyadmin/phpmyadmin/pull/20553 |
| 102 | https://github.com/xtermjs/xterm.js/pull/6253 |
| 103 | https://github.com/compiler-explorer/compiler-explorer/pull/9344 |

备注：100 解决了 ChangeLog 冲突后提交（base QA_5_2）；090 已在 issue 下留言链接 PR；094 已在 issue 下认领。其余 088–129 由续接会话处理。

## 第二轮提交（2026-10-22，088–129 续接会话）

| # | PR |
|---|---|
| 096 | https://github.com/decompme/decomp.me/pull/2167 |
| 104 | https://github.com/highlightjs/highlight.js/pull/4564 |
| 108 | https://github.com/scikit-hep/pyhf/pull/2777 |
| 114 | https://github.com/scikit-hep/hist/pull/740 |
| 115 | https://github.com/conventional-changelog/commitlint/pull/5070 |
| 116 | https://github.com/pylint-dev/pylint/pull/11717 |
| 120 | https://github.com/jasonjmcghee/ron-lsp/pull/28 |
| 125 | https://github.com/mochajs/mocha/pull/6444 |
| 129 | https://github.com/maciejhirsz/logos/pull/585 |

备注：每个都在最新上游上重新跑过测试。096 上游把 `backend/compilers` 挪到了 `cromper/`，测试已改为 cromper 下的 pytest（红→绿复现）。104 的 #4497 是别人做的函数高亮，与本补丁无关。125 mocha 需 owner 签 OpenJS EasyCLA（链接已发线程）。119 ipfs-cluster 放弃：维护者 hsanjuan 明确反对无索引的服务端名字过滤。

## 第二轮提交（2026-10-22，088–129 收尾会话）

| # | PR |
|---|---|
| 088 | https://github.com/SurgeDM/Surge/pull/734 |
| 099 | https://github.com/Kotlin/dataframe/pull/2182 |
| 118 | https://github.com/getsentry/sentry-laravel/pull/1204 |
| 121 | https://github.com/supercollider/supercollider/pull/7812 |
| 123 | https://github.com/OpenRCT2/OpenRCT2/pull/27317 |
| 128 | https://github.com/spec-kitty/spec-kitty/pull/6620（draft） |
| 208 | https://github.com/image-rs/image-png/pull/722 |
| 241 | [ZcashFoundation/zebra#11892](https://github.com/ZcashFoundation/zebra/issues/11892) | [ZcashFoundation/zebra#11894](https://github.com/ZcashFoundation/zebra/pull/11894) | 2026-10-22 提交（独立复核 PASS）；已先在 issue 留言认领 |
| 242 | [getsotto/sotto#696](https://github.com/getsotto/sotto/issues/696) | [getsotto/sotto#698](https://github.com/getsotto/sotto/pull/698) | 2026-10-22 提交（独立复核 PASS） |
| 243 | [XAGI-Lab/melra#388](https://github.com/XAGI-Lab/melra/issues/388) | [XAGI-Lab/melra#393](https://github.com/XAGI-Lab/melra/pull/393) | 2026-10-22 提交（独立复核 PASS） |
| 210 | [hgrecco/pint#2502](https://github.com/hgrecco/pint/issues/2502) | [hgrecco/pint#2517](https://github.com/hgrecco/pint/pull/2517) | 2026-10-22 提交（独立复核 PASS） |
| 204 | [git-ai-project/git-ai#1036](https://github.com/git-ai-project/git-ai/issues/1036) | [git-ai-project/git-ai#2436](https://github.com/git-ai-project/git-ai/pull/2436) | 2026-10-22 提交（独立复核 PASS） |
| 244 | [Rohit-Dnath/RAMen#63](https://github.com/Rohit-Dnath/RAMen/issues/63) | — | 放弃：维护者于 10-22 19:34 UTC 以自有 commit 932787e 修复并关闭 issue |
| 271 | [dry-rb/dry-schema#504](https://github.com/dry-rb/dry-schema/issues/504) | [dry-rb/dry-schema#521](https://github.com/dry-rb/dry-schema/pull/521) | 2026-10-22 提交（独立复核 PASS）；CHANGELOG 已填 PR 号 |
| 245 | [vyncint/termlens#594](https://github.com/vyncint/termlens/issues/594) | [vyncint/termlens#604](https://github.com/vyncint/termlens/pull/604) | 2026-10-22 提交（独立复核 PASS） |
| 211 | [troessner/reek#1429](https://github.com/troessner/reek/issues/1429) | [troessner/reek#1848](https://github.com/troessner/reek/pull/1848) | 2026-10-22 提交（独立复核 PASS） |
| 300 | [zigtools/zls#2098](https://github.com/zigtools/zls/issues/2098) | [zigtools/zls#3304](https://github.com/zigtools/zls/pull/3304) | 2026-10-22 提交（独立复核 PASS） |
| 272 | [dry-rb/dry-schema#455](https://github.com/dry-rb/dry-schema/issues/455) | [dry-rb/dry-schema#522](https://github.com/dry-rb/dry-schema/pull/522) | 2026-10-22 提交（独立复核 PASS）；CHANGELOG 已填 PR 号 |
| 247 | [vyncint/termlens#586](https://github.com/vyncint/termlens/issues/586) | [vyncint/termlens#605](https://github.com/vyncint/termlens/pull/605) | 2026-10-22 提交（独立复核 PASS） |
| 273 | [dry-rb/dry-schema#468](https://github.com/dry-rb/dry-schema/issues/468) | [dry-rb/dry-schema#523](https://github.com/dry-rb/dry-schema/pull/523) | 2026-10-22 提交（独立复核 PASS）；CHANGELOG 已填 PR 号 |
| 274 | [dry-rb/dry-validation#741](https://github.com/dry-rb/dry-validation/issues/741) | [dry-rb/dry-schema#524](https://github.com/dry-rb/dry-schema/pull/524) | 2026-10-22 提交（独立复核 PASS）；PR 开在 dry-schema；CHANGELOG 已填 PR 号 |
| 275 | [hanami/hanami-minitest#11](https://github.com/hanami/hanami-minitest/issues/11) | [hanami/hanami-minitest#13](https://github.com/hanami/hanami-minitest/pull/13) | 2026-10-22 提交（独立复核 PASS） |
| 330 | [crazy-goat/tikv-php#680](https://github.com/crazy-goat/tikv-php/issues/680) | [crazy-goat/tikv-php#738](https://github.com/crazy-goat/tikv-php/pull/738) | 2026-10-22 提交（独立复核 PASS） |
| 331 | [crazy-goat/tikv-php#682](https://github.com/crazy-goat/tikv-php/issues/682) | [crazy-goat/tikv-php#739](https://github.com/crazy-goat/tikv-php/pull/739) | 2026-10-22 提交（独立复核 PASS） |
| 332 | [crazy-goat/tikv-php#662](https://github.com/crazy-goat/tikv-php/issues/662) | [crazy-goat/tikv-php#740](https://github.com/crazy-goat/tikv-php/pull/740) | 2026-10-22 提交（独立复核 PASS） |
| 213 | [PyCQA/pyflakes#548](https://github.com/PyCQA/pyflakes/issues/548) | — | 阻塞：开 PR 被拒（GraphQL: no permission to CreatePullRequest，仓库限协作者开 PR）；分支 anyingiit/pyflakes:del-shadowed-builtin 已推送 |
| 248 | [open-nexus-OS/open-nexus-OS#47](https://github.com/open-nexus-OS/open-nexus-OS/issues/47) | [open-nexus-OS/open-nexus-OS#53](https://github.com/open-nexus-OS/open-nexus-OS/pull/53) | 2026-10-22 提交（独立复核 PASS）；已先在 issue 认领；CLA 已在 PR 下签署并编辑描述触发重跑，但 cla-check 因上游 workflow 自身错误（读取 neuron-foundation 分支 signed_clas.json 返回 404）仍失败，需维护者修 workflow |
| 212 | [troessner/reek#1476](https://github.com/troessner/reek/issues/1476) | [troessner/reek#1849](https://github.com/troessner/reek/pull/1849) | 2026-10-22 提交（独立复核 PASS） |
| 201 | [plotly/plotly.py#4040](https://github.com/plotly/plotly.py/issues/4040) | [plotly/plotly.py#5840](https://github.com/plotly/plotly.py/pull/5840) | 2026-10-22 提交（独立复核 PASS-WITH-FIXES）；CHANGELOG 已填 PR 号；与 #5839 同改 CHANGELOG，后合并者需 rebase |
| 249 | [KnockOutEZ/wigolo#526](https://github.com/KnockOutEZ/wigolo/issues/526) | [KnockOutEZ/wigolo#663](https://github.com/KnockOutEZ/wigolo/pull/663) | 2026-10-22 提交（独立复核 PASS）；CLA 为提交即同意 |
| 276 | [hanami/hanami-cli#450](https://github.com/hanami/hanami-cli/issues/450) | [hanami/hanami-cli#465](https://github.com/hanami/hanami-cli/pull/465) | 2026-10-22 提交（独立复核 PASS）；CHANGELOG 已填 PR 号 |
| 301 | [seladb/PcapPlusPlus#2278](https://github.com/seladb/PcapPlusPlus/issues/2278) | [seladb/PcapPlusPlus#2334](https://github.com/seladb/PcapPlusPlus/pull/2334) | 2026-10-22 提交（独立复核 PASS）；GTP 部分 |
| 302 | [seladb/PcapPlusPlus#2278](https://github.com/seladb/PcapPlusPlus/issues/2278) | [seladb/PcapPlusPlus#2335](https://github.com/seladb/PcapPlusPlus/pull/2335) | 2026-10-22 提交（独立复核 PASS）；QUIC 部分 |
| 333 | [mpdf/mpdf#2232](https://github.com/mpdf/mpdf/issues/2232) | [mpdf/mpdf#2234](https://github.com/mpdf/mpdf/pull/2234) | 2026-10-22 提交（独立复核 PASS）；base development；commit 含 Assisted-by 声明 |
| 390 | [pydantic/monty#1101](https://github.com/pydantic/monty/issues/1101) | [pydantic/monty#1114](https://github.com/pydantic/monty/pull/1114) | 2026-10-22 提交（独立复核 PASS） |
| 420 | [opendatahub-io/ai-gateway-payload-processing#315](https://github.com/opendatahub-io/ai-gateway-payload-processing/issues/315) | [opendatahub-io/ai-gateway-payload-processing#489](https://github.com/opendatahub-io/ai-gateway-payload-processing/pull/489) | 2026-10-22 提交（独立复核 PASS）；DCO 已签 |
| 422 | [BSC-ES/autosubmit#3240](https://github.com/BSC-ES/autosubmit/issues/3240) | [BSC-ES/autosubmit#3370](https://github.com/BSC-ES/autosubmit/pull/3370) | 2026-10-22 提交（独立复核 PASS） |
| 360 | [helix-editor/helix#3115](https://github.com/helix-editor/helix/issues/3115) | [helix-editor/helix#16404](https://github.com/helix-editor/helix/pull/16404) | 2026-10-22 提交（独立复核 PASS）；20:50 已 push 跟进补丁（内联表）并更新 PR 正文 |
| 334 | [Euro-Office/eurooffice-nextcloud#173](https://github.com/Euro-Office/eurooffice-nextcloud/issues/173) | [Euro-Office/eurooffice-nextcloud#250](https://github.com/Euro-Office/eurooffice-nextcloud/pull/250) | 2026-10-22 提交（独立复核 PASS） |
| 335 | [Euro-Office/eurooffice-nextcloud#151](https://github.com/Euro-Office/eurooffice-nextcloud/issues/151) | [Euro-Office/eurooffice-nextcloud#251](https://github.com/Euro-Office/eurooffice-nextcloud/pull/251) | 2026-10-22 提交（独立复核 PASS） |
| 277 | [ruby/rdoc#1567](https://github.com/ruby/rdoc/issues/1567) | [ruby/rdoc#1860](https://github.com/ruby/rdoc/pull/1860) | 2026-10-22 提交（独立复核 PASS）；按 AGENTS.md 正文无 AI 声明段 |
| 421 | [tuProlog/2p-kt#946](https://github.com/tuProlog/2p-kt/issues/946) | [tuProlog/2p-kt#1044](https://github.com/tuProlog/2p-kt/pull/1044) | 2026-10-22 提交（独立复核 PASS） |
| 250 | [femboypuppy/Tessera-Notes#38](https://github.com/femboypuppy/Tessera-Notes/issues/38) | [femboypuppy/Tessera-Notes#116](https://github.com/femboypuppy/Tessera-Notes/pull/116) | 2026-10-22 提交（独立复核 PASS）；已先在 issue 认领 |
| 251 | [simonives/redwrench#57](https://github.com/simonives/redwrench/issues/57) | [simonives/redwrench#97](https://github.com/simonives/redwrench/pull/97) | 2026-10-22 提交（独立复核 PASS）；commit 加 Assisted-by trailer |
| 336 | [phpmyadmin/motranslator#59](https://github.com/phpmyadmin/motranslator/issues/59) | [phpmyadmin/motranslator#67](https://github.com/phpmyadmin/motranslator/pull/67) | 2026-10-22 提交（独立复核 PASS）；DCO 已签 |
| 214 | [mitmproxy/pdoc#775](https://github.com/mitmproxy/pdoc/issues/775) | [mitmproxy/pdoc#902](https://github.com/mitmproxy/pdoc/pull/902) | 2026-10-22 提交（独立复核 PASS） |
| 278 | [ruby/rdoc#1782](https://github.com/ruby/rdoc/issues/1782) | [ruby/rdoc#1861](https://github.com/ruby/rdoc/pull/1861) | 2026-10-22 提交（独立复核 PASS）；与 open #1831 同改一行，后合者需 rebase |
| 361 | [helix-editor/helix#11198](https://github.com/helix-editor/helix/issues/11198) | [helix-editor/helix#16405](https://github.com/helix-editor/helix/pull/16405) | 2026-10-22 提交（独立复核 PASS） |
| 391 | [Gaurav-Gosain/tuios#980](https://github.com/Gaurav-Gosain/tuios/issues/980) | [Gaurav-Gosain/tuios#1038](https://github.com/Gaurav-Gosain/tuios/pull/1038) | 2026-10-22 提交（独立复核 PASS） |
| 392 | [Gaurav-Gosain/tuios#585](https://github.com/Gaurav-Gosain/tuios/issues/585) | [Gaurav-Gosain/tuios#1039](https://github.com/Gaurav-Gosain/tuios/pull/1039) | 2026-10-22 提交（独立复核 PASS）；与 #1038 在 registry.go 相邻行冲突，后合者用 alt-0001-on-top-of-391.patch |
| 423 | [whtsky/pixelmatch-py#256](https://github.com/whtsky/pixelmatch-py/issues/256) | [whtsky/pixelmatch-py#268](https://github.com/whtsky/pixelmatch-py/pull/268) | 2026-10-22 提交（独立复核 PASS） |
| 279 | [hanami/hanami-view#264](https://github.com/hanami/hanami-view/issues/264) | [hanami/hanami-view#291](https://github.com/hanami/hanami-view/pull/291) | 2026-10-22 提交（独立复核 PASS）；CHANGELOG 已填 PR 号 |
| 424 | [wiktor-k/ssh-agent-lib#116](https://github.com/wiktor-k/ssh-agent-lib/issues/116) | [wiktor-k/ssh-agent-lib#117](https://github.com/wiktor-k/ssh-agent-lib/pull/117) | 2026-10-22 提交（独立复核 PASS）；DCO 已签；正文用 Refs 不关 issue |
| 303 | [melihbirim/csvql#259](https://github.com/melihbirim/csvql/issues/259) | [melihbirim/csvql#264](https://github.com/melihbirim/csvql/pull/264) | 2026-10-22 提交（独立复核 PASS）；Part of #259 |
| 215 | [vcr/vcr#1006](https://github.com/vcr/vcr/issues/1006) | [vcr/vcr#1079](https://github.com/vcr/vcr/pull/1079) | 2026-10-22 提交（独立复核 PASS） |
| 280 | [hanami/hanami#1626](https://github.com/hanami/hanami/issues/1626) | [hanami/hanami#1651](https://github.com/hanami/hanami/pull/1651) | 2026-10-22 提交（独立复核 PASS）；CHANGELOG 已填 PR 号 |
| 393 | [zerobrewhq/zerobrew#414](https://github.com/zerobrewhq/zerobrew/issues/414) | [zerobrewhq/zerobrew#480](https://github.com/zerobrewhq/zerobrew/pull/480) | 2026-10-22 提交（独立复核 PASS）；Frameworks 部分（sbin 已由维护者修） |
| 362 | [helix-editor/helix#5817](https://github.com/helix-editor/helix/issues/5817) | [helix-editor/helix#16406](https://github.com/helix-editor/helix/pull/16406) | 2026-10-22 提交（独立复核 PASS） |
| 363 | [helix-editor/helix#11207](https://github.com/helix-editor/helix/issues/11207) | [helix-editor/helix#16407](https://github.com/helix-editor/helix/pull/16407) | 2026-10-22 提交（独立复核 PASS） |
| 337 | [synolia/SyliusMaintenancePlugin#54](https://github.com/synolia/SyliusMaintenancePlugin/issues/54) | [synolia/SyliusMaintenancePlugin#55](https://github.com/synolia/SyliusMaintenancePlugin/pull/55) | 2026-10-22 提交（独立复核 PASS） |
| 425 | [BSC-ES/autosubmit#3104](https://github.com/BSC-ES/autosubmit/issues/3104) | [BSC-ES/autosubmit#3371](https://github.com/BSC-ES/autosubmit/pull/3371) | 2026-10-22 提交（独立复核 PASS） |
| 281 | [ruby/rdoc#1857](https://github.com/ruby/rdoc/issues/1857) | [ruby/rdoc#1862](https://github.com/ruby/rdoc/pull/1862) | 2026-10-22 提交（独立复核 PASS）；按 AGENTS.md 正文无 AI 声明段 |
| 282 | [TNG/ArchUnit#154](https://github.com/TNG/ArchUnit/issues/154) | [TNG/ArchUnit#1769](https://github.com/TNG/ArchUnit/pull/1769) | 2026-10-22 提交（独立复核 PASS）；DCO 已签；同时解决 #190；#154 旧 assignee 已在正文说明 |
| 338 | [thephpleague/openapi-psr7-validator#273](https://github.com/thephpleague/openapi-psr7-validator/issues/273) | [thephpleague/openapi-psr7-validator#275](https://github.com/thephpleague/openapi-psr7-validator/pull/275) | 2026-10-22 提交（独立复核 PASS） |
| 394 | [zerobrewhq/zerobrew#348](https://github.com/zerobrewhq/zerobrew/issues/348) | [zerobrewhq/zerobrew#481](https://github.com/zerobrewhq/zerobrew/pull/481) | 2026-10-22 提交（独立复核 PASS） |
| 426 | [OpenCHAMI/ochami#188](https://github.com/OpenCHAMI/ochami/issues/188) | [OpenCHAMI/ochami#214](https://github.com/OpenCHAMI/ochami/pull/214) | 2026-10-22 提交（独立复核 PASS）；DCO 已签 |
| 427 | [OpenCHAMI/ochami#186](https://github.com/OpenCHAMI/ochami/issues/186) | [OpenCHAMI/ochami#215](https://github.com/OpenCHAMI/ochami/pull/215) | 2026-10-22 提交（独立复核 PASS）；DCO 已签 |
| 283 | [devonfw/IDEasy#1214](https://github.com/devonfw/IDEasy/issues/1214) | [devonfw/IDEasy#2737](https://github.com/devonfw/IDEasy/pull/2737) | 2026-10-22 提交（独立复核 PASS）；已先在 issue 认领；**待 owner 签 CLA**（cla-assistant.io 网页，GitHub 登录：https://cla-assistant.io/devonfw/IDEasy?pullRequest=2737） |
| 428 | [OpenCHAMI/ochami#191](https://github.com/OpenCHAMI/ochami/issues/191) | [OpenCHAMI/ochami#216](https://github.com/OpenCHAMI/ochami/pull/216) | 2026-10-22 提交（独立复核 PASS）；DCO 已签 |
| 339 | [hrsh7th/nvim-cmp#2232](https://github.com/hrsh7th/nvim-cmp/issues/2232) | [hrsh7th/nvim-cmp#2234](https://github.com/hrsh7th/nvim-cmp/pull/2234) | 2026-10-22 提交（独立复核 PASS） |
| 340 | [stevearc/oil.nvim#754](https://github.com/stevearc/oil.nvim/issues/754) | [stevearc/oil.nvim#793](https://github.com/stevearc/oil.nvim/pull/793) | 2026-10-22 提交（独立复核 PASS） |
| 429 | [supabase/terraform-provider-supabase#372](https://github.com/supabase/terraform-provider-supabase/issues/372) | [supabase/terraform-provider-supabase#380](https://github.com/supabase/terraform-provider-supabase/pull/380) | 2026-10-22 提交（独立复核 PASS）；未对真实 API 验证（正文已说明） |
| 430 | [curiousdannii/remglk-rs#18](https://github.com/curiousdannii/remglk-rs/issues/18) | [curiousdannii/remglk-rs#19](https://github.com/curiousdannii/remglk-rs/pull/19) | 2026-10-22 提交（独立复核 PASS）；含 .ulx 测试文件 |
| 431 | [OpenCHAMI/ochami#206](https://github.com/OpenCHAMI/ochami/issues/206) | [OpenCHAMI/ochami#217](https://github.com/OpenCHAMI/ochami/pull/217) | 2026-10-22 提交（独立复核 PASS）；DCO 已签 |
| 432 | [bpmn-io/dmn-migrate#60](https://github.com/bpmn-io/dmn-migrate/issues/60) | [bpmn-io/dmn-migrate#63](https://github.com/bpmn-io/dmn-migrate/pull/63) | 2026-10-22 提交（独立复核 PASS）；git am --keep-cr 应用；**CLA 待签**（bot 评论后）；CI 等维护者批准（首次贡献者），bot 尚未出现 |
| 341 | [nvim-orgmode/orgmode#1171](https://github.com/nvim-orgmode/orgmode/issues/1171) | [nvim-orgmode/orgmode#1201](https://github.com/nvim-orgmode/orgmode/pull/1201) | 2026-10-22 提交（独立复核 PASS）；commit 带 AI-assisted trailer（AGENTS.md 要求） |
| 342 | [stevearc/conform.nvim#877](https://github.com/stevearc/conform.nvim/issues/877) | [stevearc/conform.nvim#905](https://github.com/stevearc/conform.nvim/pull/905) | 2026-10-22 提交（独立复核 PASS） |
| 433 | [tuProlog/2p-kt#1005](https://github.com/tuProlog/2p-kt/issues/1005) | [tuProlog/2p-kt#1045](https://github.com/tuProlog/2p-kt/pull/1045) | 2026-10-22 提交（独立复核 PASS） |
| 284 | [tuProlog/2p-kt#945](https://github.com/tuProlog/2p-kt/issues/945) | [tuProlog/2p-kt#1046](https://github.com/tuProlog/2p-kt/pull/1046) | 2026-10-22 提交（独立复核 PASS） |
| 434 | [bpmn-io/bpmn-to-image#65](https://github.com/bpmn-io/bpmn-to-image/issues/65) | [bpmn-io/bpmn-to-image#70](https://github.com/bpmn-io/bpmn-to-image/pull/70) | 2026-10-22 提交（独立复核 PASS）；纯文档，Related to #65；**CLA 待签**（bot 评论后）；需 owner 在网页签 bpmn-io CLA：https://cla-assistant.io/bpmn-io/bpmn-to-image?pullRequest=70（签一次可能覆盖 432/436） |
| 286 | [benbalter/jekyll-remote-theme#109](https://github.com/benbalter/jekyll-remote-theme/issues/109) | [benbalter/jekyll-remote-theme#174](https://github.com/benbalter/jekyll-remote-theme/pull/174) | 2026-10-22 提交（独立复核 PASS） |
| 287 | [benbalter/jekyll-optional-front-matter#67](https://github.com/benbalter/jekyll-optional-front-matter/issues/67) | [benbalter/jekyll-optional-front-matter#69](https://github.com/benbalter/jekyll-optional-front-matter/pull/69) | 2026-10-22 提交（独立复核 PASS） |
| 288 | [benbalter/jekyll-titles-from-headings#109](https://github.com/benbalter/jekyll-titles-from-headings/issues/109) | [benbalter/jekyll-titles-from-headings#111](https://github.com/benbalter/jekyll-titles-from-headings/pull/111) | 2026-10-22 提交（独立复核 PASS） |
| 436 | [bpmn-io/properties-panel#553](https://github.com/bpmn-io/properties-panel/issues/553) | [bpmn-io/properties-panel#565](https://github.com/bpmn-io/properties-panel/pull/565) | 2026-10-22 提交（独立复核 PASS）；**CLA 待签**（bot 评论后） |
| 289 | [benbalter/site-inspector#126](https://github.com/benbalter/site-inspector/issues/126) | [benbalter/site-inspector#133](https://github.com/benbalter/site-inspector/pull/133) | 2026-10-22 提交（独立复核 PASS） |
| 290 | [benbalter/site-inspector#128](https://github.com/benbalter/site-inspector/issues/128) | [benbalter/site-inspector#134](https://github.com/benbalter/site-inspector/pull/134) | 2026-10-22 提交（独立复核 PASS） |
| 291 | [benbalter/situation-clock#24](https://github.com/benbalter/situation-clock/issues/24) | [benbalter/situation-clock#34](https://github.com/benbalter/situation-clock/pull/34) | 2026-10-22 提交（独立复核 PASS）；base gh-pages |
| 292 | [benbalter/avatar-montage#4](https://github.com/benbalter/avatar-montage/issues/4) | [benbalter/avatar-montage#5](https://github.com/benbalter/avatar-montage/pull/5) | 2026-10-22 提交（独立复核 PASS） |
| 293 | [higher-kinded-j/higher-kinded-j#1221](https://github.com/higher-kinded-j/higher-kinded-j/issues/1221) | [higher-kinded-j/higher-kinded-j#1223](https://github.com/higher-kinded-j/higher-kinded-j/pull/1223) | 2026-10-22 提交（独立复核 PASS）；已先在 issue 认领 |
| 294 | [authorjapps/zerocode#800](https://github.com/authorjapps/zerocode/issues/800) | [authorjapps/zerocode#801](https://github.com/authorjapps/zerocode/pull/801) | 2026-10-22 提交（独立复核 PASS） |
| 295 | [oscarbol09/jvm-mcp#177](https://github.com/oscarbol09/jvm-mcp/issues/177) | [oscarbol09/jvm-mcp#182](https://github.com/oscarbol09/jvm-mcp/pull/182) | 2026-10-22 提交（独立复核 PASS） |
| 296 | [oscarbol09/jvm-mcp#175](https://github.com/oscarbol09/jvm-mcp/issues/175) | [oscarbol09/jvm-mcp#183](https://github.com/oscarbol09/jvm-mcp/pull/183) | 2026-10-22 提交（独立复核 PASS） |

备注：088 解冲突后适配上游 `formatSettingValueForEdit` 新签名，`go test ./...` 全过，回退源码则新测试编译失败（红）。099 解冲突并把上游新增的公开 `AnyCol` 用法一并展开，`:core/:dataframe-arrow` compileTestKotlin + apiCheck + ktlint 通过（未跑全量测试）。118 装了 PHP 8.5：红→绿、全量 phpunit 363 通过、phpstan 无错，已在 issue #1070 留言。121 两个改动文件上游无变化，沿用之前 sclang 红→绿结果。123 为纯改名，解冲突后无残留旧名，未本地编译（依赖太多，靠 CI）。128 已在 issue #4292 留言认领，最新 main 上红→绿。208 是协调员撤回提交员任务前已开出的。
旧会话 9 个 PR 本地重跑：grpc-gateway、ipython（test_system_interrupt 偶发超时，重跑通过，与改动无关）、pyinstaller、OpsiMate、PathMap、xterm.js、compiler-explorer 均通过；NLog（无 dotnet）、phpmyadmin（未跑）只能看 CI。

## PHP2Shell 专题（2026-10-22，CVE-2026-109618/109619，编号 187–199）

| # | PR |
|---|---|
| 187 | https://github.com/ErugoOSS/Erugo/pull/294 |
| 188 | https://github.com/Forceu/barcodebuddy-docker/pull/39 |
| 189 | https://github.com/wireless-broadband-alliance/wba-openroaming-portal/pull/11 |
| 190 | https://github.com/ploi/roadmap/pull/389 |
