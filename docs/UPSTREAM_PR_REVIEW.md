# 上游 PR 成果复盘（2026-10-23）

数据：anyingiit 自 2026-09-24 起开出的上游 PR（排除自己仓库），GitHub 状态于 2026-10-23 11:00 UTC 抓取；`contributions/submissions.json` 与 `gh search prs` 两边一致。层级取自 `contributions/INDEX.md`，编号 171 之后按星数（>5k 为高星）和建库时间（两年内为新锐）推断。关闭原因和开着 PR 的细分是读评论后人工归类。图表版见 Dashboard：https://claude.ai/artifact/8jjnkBQ5EFjHDLXU3Eijcy

## 总体

| 状态 | 数量 | 占比 |
|---|---|---|
| 已合并 | 40 | 21% |
| 开着 | 130 | 67% |
| 关闭未合并 | 24 | 12% |
| 合计 | 194 | |

已决合并率（合并 ÷（合并+关闭））：**62%**。合并中位用时 1.2 天，平均 3.9 天。

### 开着的 PR 细分

| 细分 | 数量 |
|---|---|
| 等审查 | 104 |
| CI 失败 | 11 |
| 维护者有要求待处理 | 10 |
| 已回复待复审 | 2 |
| 已批准待合并 | 2 |
| 等 CLA | 1 |

开着 PR 平均已等 3.2 天（中位 0.6 天）；第一轮仍开着的 6 个平均已等 28.3 天，第二轮 8 个平均 21.2 天，10-22 晚 116 个平均 0.6 天。

## 关闭原因

| 原因 | 数量 | 占比 | 例子 |
|---|---|---|---|
| 不欢迎 AI 或自动化贡献 | 12 | 50% | hanami-cli#464 "not interested in contributions from autonomous agents"（Hanakai 一次关 8 个）；remglk-rs#19 "I don't accept AI generated code"；pyinstaller#9555、supercollider#7812 认为 AI 做 good first issue 违背其初衷；mocha#6444 被 AgentScan 机器人判为自动化账号自动关闭 |
| 维护者另行修复或被取代 | 4 | 17% | celler#96 "Superseded by #97. The approach here is very convoluted."；barcodebuddy-docker#39 被维护者提交取代；i18n-tasks#759 在 #763 合入；provider-cassandra#30 让位于新契约 #36（维护者肯定了分析） |
| 我们主动关闭 | 4 | 17% | IDEasy#2737 无法签 CLA；litebox#1481 上游已修；spotatui#576、pyrite#398 无法跟进 |
| 问题不成立或不想要该改动 | 2 | 8% | mirador#4553 "canvasIndex is not a configurable setting"；zerobrew#481 "prefer issues like these to be taken with greater care" |
| 无说明关闭 | 2 | 8% | decomp.me#2167、methodologistUI-backend#378 无评论关闭 |

需先讨论设计：暂无关闭，但 zitadel/oidc#994 被维护者搁置待 issue 讨论。

### 全部被关闭的 PR

| PR | 原因 | 关闭者 | 原话 / 说明 |
|---|---|---|---|
| [curiousdannii/remglk-rs#19](https://github.com/curiousdannii/remglk-rs/pull/19) | 不欢迎 AI 或自动化贡献 | curiousdannii | Sorry, but I don't accept AI generated code. |
| [dry-rb/dry-schema#521](https://github.com/dry-rb/dry-schema/pull/521) | 不欢迎 AI 或自动化贡献 | timriley | 引用 hanami-cli#464 的 AI 政策一并关闭 |
| [dry-rb/dry-schema#522](https://github.com/dry-rb/dry-schema/pull/522) | 不欢迎 AI 或自动化贡献 | timriley | 引用 hanami-cli#464 的 AI 政策一并关闭 |
| [dry-rb/dry-schema#523](https://github.com/dry-rb/dry-schema/pull/523) | 不欢迎 AI 或自动化贡献 | timriley | 引用 hanami-cli#464 的 AI 政策一并关闭 |
| [dry-rb/dry-schema#524](https://github.com/dry-rb/dry-schema/pull/524) | 不欢迎 AI 或自动化贡献 | timriley | 引用 hanami-cli#464 的 AI 政策一并关闭 |
| [hanami/hanami-cli#464](https://github.com/hanami/hanami-cli/pull/464) | 不欢迎 AI 或自动化贡献 | timriley | not interested in contributions from autonomous agents |
| [hanami/hanami-cli#465](https://github.com/hanami/hanami-cli/pull/465) | 不欢迎 AI 或自动化贡献 | timriley | 引用 hanami-cli#464 的 AI 政策一并关闭 |
| [hanami/hanami-view#291](https://github.com/hanami/hanami-view/pull/291) | 不欢迎 AI 或自动化贡献 | timriley | 引用 hanami-cli#464 的 AI 政策一并关闭 |
| [hanami/hanami#1651](https://github.com/hanami/hanami/pull/1651) | 不欢迎 AI 或自动化贡献 | timriley | 引用 hanami-cli#464 的 AI 政策一并关闭 |
| [mochajs/mocha#6444](https://github.com/mochajs/mocha/pull/6444) | 不欢迎 AI 或自动化贡献 | github-actions | AgentScan 机器人判定为自动化账号，打 spam 标签后自动关闭 |
| [pyinstaller/pyinstaller#9555](https://github.com/pyinstaller/pyinstaller/pull/9555) | 不欢迎 AI 或自动化贡献 | rokm | completely misses the point of the "good first issue" concept |
| [supercollider/supercollider#7812](https://github.com/supercollider/supercollider/pull/7812) | 不欢迎 AI 或自动化贡献 | Spacechild1 | The purpose of good-first-issues is to help new contributors get on board. |
| [LargeModGames/spotatui#576](https://github.com/LargeModGames/spotatui/pull/576) | 我们主动关闭 | anyingiit | CodeRabbit 要求修改，按 owner 决定不返工 |
| [devonfw/IDEasy#2737](https://github.com/devonfw/IDEasy/pull/2737) | 我们主动关闭 | anyingiit | 需要签 CLA，无法签署 |
| [microsoft/litebox#1481](https://github.com/microsoft/litebox/pull/1481) | 我们主动关闭 | anyingiit | 上游 #1594 已修了同一问题 |
| [pyrite-wiki/pyrite#398](https://github.com/pyrite-wiki/pyrite/pull/398) | 我们主动关闭 | anyingiit | 无法跟进，释放 issue 给他人 |
| [decompme/decomp.me#2167](https://github.com/decompme/decomp.me/pull/2167) | 无说明关闭 | mkst | 无评论直接关闭 |
| [vitruv-tools/methodologistUI-backend#378](https://github.com/vitruv-tools/methodologistUI-backend/pull/378) | 无说明关闭 | arlange | 无评论直接关闭（同日另一外部 PR 也被关） |
| [Forceu/barcodebuddy-docker#39](https://github.com/Forceu/barcodebuddy-docker/pull/39) | 维护者另行修复或被取代 | Forceu | this PR has been superseded by eb1bb02 |
| [celler-cache/celler#96](https://github.com/celler-cache/celler/pull/96) | 维护者另行修复或被取代 | blitz | Superseded by #97. The approach here is very convoluted. |
| [glebm/i18n-tasks#759](https://github.com/glebm/i18n-tasks/pull/759) | 维护者另行修复或被取代 | davidwessman | Merged in #763（维护者在 #763 合入） |
| [openeverest/provider-cassandra#30](https://github.com/openeverest/provider-cassandra/pull/30) | 维护者另行修复或被取代 | spron-in | Closing in favor of #36.（并肯定了分析） |
| [ProjectMirador/mirador#4553](https://github.com/ProjectMirador/mirador/pull/4553) | 问题不成立或不想要该改动 | marlo-longley | canvasIndex is not a configurable setting in Mirador |
| [zerobrewhq/zerobrew#481](https://github.com/zerobrewhq/zerobrew/pull/481) | 问题不成立或不想要该改动 | cachebag | I prefer issues like these to be taken with greater care. |

## 按批次、层级、语言

| 批次 | PR 数 | 合并 | 关闭 | 开着 | 已决合并率 |
|---|---|---|---|---|---|
| 第一轮 09-25 | 32 | 21 | 5 | 6 | 81% |
| 第二轮 10-02 | 19 | 9 | 2 | 8 | 82% |
| 10-22 晚 | 143 | 10 | 17 | 116 | 37% |

| 层级 | PR 数 | 合并 | 关闭 | 开着 | 已决合并率 |
|---|---|---|---|---|---|
| 高星 | 42 | 4 | 5 | 33 | 44% |
| 新锐 | 49 | 16 | 3 | 30 | 84% |
| 自由 | 103 | 20 | 16 | 67 | 56% |

| 语言 | PR 数 | 合并 | 关闭 | 开着 | 已决合并率 |
|---|---|---|---|---|---|
| Rust | 44 | 12 | 5 | 27 | 71% |
| Go | 28 | 8 | 2 | 18 | 80% |
| Python | 26 | 8 | 2 | 16 | 80% |
| Ruby | 26 | 2 | 9 | 15 | 18% |
| PHP | 18 | 2 | 0 | 16 | 100% |
| TypeScript | 15 | 3 | 1 | 11 | 75% |
| Java | 12 | 2 | 2 | 8 | 50% |
| Kotlin | 6 | 1 | 0 | 5 | 100% |

10-22 晚这批大多不到一天，已决合并率偏低主要因为 Hanakai 的批量关闭和其他几起当天拒绝，结果还会变。高星层级 5 个关闭里有 4 个与 AI 政策有关；Ruby 的关闭集中在 Hanakai。

## 开着且需要我们动作的 PR

| PR | 状态 | 要点 | 已等（天） |
|---|---|---|---|
| [Adam-Vandervorst/PathMap#167](https://github.com/Adam-Vandervorst/PathMap/pull/167) | 维护者有要求待处理 | 维护者愿意合并，要求在 PR 里确认 MIT 授权 | 0.7 |
| [BSC-ES/autosubmit#3370](https://github.com/BSC-ES/autosubmit/pull/3370) | CI 失败 | CI 有失败项，尚无人工评论 | 0.6 |
| [Euro-Office/eurooffice-nextcloud#250](https://github.com/Euro-Office/eurooffice-nextcloud/pull/250) | CI 失败 | CI 有失败项，尚无人工评论 | 0.6 |
| [Euro-Office/eurooffice-nextcloud#251](https://github.com/Euro-Office/eurooffice-nextcloud/pull/251) | CI 失败 | CI 有失败项，尚无人工评论 | 0.6 |
| [NLog/NLog#6313](https://github.com/NLog/NLog/pull/6313) | CI 失败 | CI 有失败项，尚无人工评论 | 0.7 |
| [XAGI-Lab/melra#393](https://github.com/XAGI-Lab/melra/pull/393) | 已回复待复审 | 两轮修改要求都已处理，等复审 | 0.6 |
| [bpmn-io/bpmn-to-image#70](https://github.com/bpmn-io/bpmn-to-image/pull/70) | CI 失败 | CI 有失败项，尚无人工评论 | 0.5 |
| [bpmn-io/dmn-migrate#63](https://github.com/bpmn-io/dmn-migrate/pull/63) | CI 失败 | CI 有失败项，尚无人工评论 | 0.6 |
| [bpmn-io/properties-panel#565](https://github.com/bpmn-io/properties-panel/pull/565) | CI 失败 | CI 有失败项，尚无人工评论 | 0.5 |
| [conventional-changelog/commitlint#5070](https://github.com/conventional-changelog/commitlint/pull/5070) | 维护者有要求待处理 | 维护者先要我们对规则行为变化表态 | 0.7 |
| [git-ai-project/git-ai#2436](https://github.com/git-ai-project/git-ai/pull/2436) | 等 CLA | CLA 未签；维护者还问能否不加依赖（已回复） | 0.6 |
| [go-git/go-git#2423](https://github.com/go-git/go-git/pull/2423) | 已回复待复审 | 已按要求 rebase，等复审 | 28.3 |
| [infection/infection#3699](https://github.com/infection/infection/pull/3699) | 维护者有要求待处理 | 要求加一个可观测的未覆盖变异（用 diff 评论标记不合并） | 0.7 |
| [openrewrite/rewrite-cucumber-jvm#73](https://github.com/openrewrite/rewrite-cucumber-jvm/pull/73) | CI 失败 | CI 有失败项，尚无人工评论 | 0.6 |
| [phpmyadmin/motranslator#67](https://github.com/phpmyadmin/motranslator/pull/67) | 已批准待合并 | 已批准；CI 有失败项 | 0.6 |
| [rjsf-team/react-jsonschema-form#5622](https://github.com/rjsf-team/react-jsonschema-form/pull/5622) | 维护者有要求待处理 | 要求 rebase 到 v7 分支 | 0.7 |
| [rust-embedded/heapless#692](https://github.com/rust-embedded/heapless/pull/692) | 维护者有要求待处理 | 改动被认可，但 AI 描述被批评；需 rebase | 21.2 |
| [sdlc-pro/spring-lens#527](https://github.com/sdlc-pro/spring-lens/pull/527) | 维护者有要求待处理 | 要求先在 issue 留言认领 | 0.5 |
| [sdlc-pro/spring-lens#528](https://github.com/sdlc-pro/spring-lens/pull/528) | 维护者有要求待处理 | 要求先在 issue 留言认领 | 0.5 |
| [stackrox/kube-linter#1273](https://github.com/stackrox/kube-linter/pull/1273) | CI 失败 | CI 有失败项，尚无人工评论 | 21.2 |
| [stackrox/kube-linter#1280](https://github.com/stackrox/kube-linter/pull/1280) | CI 失败 | CI 有失败项，尚无人工评论 | 0.7 |
| [typstyle-rs/typstyle#521](https://github.com/typstyle-rs/typstyle/pull/521) | 维护者有要求待处理 | 维护者不确定哪种行为更好，需要说明取舍 | 0.7 |
| [valkey-io/valkey-glide-ruby#385](https://github.com/valkey-io/valkey-glide-ruby/pull/385) | CI 失败 | CI 有失败项，尚无人工评论 | 0.6 |
| [vcr/vcr#1079](https://github.com/vcr/vcr/pull/1079) | 已批准待合并 | Very clear fix, thank you! | 0.6 |
| [zerobrewhq/zerobrew#480](https://github.com/zerobrewhq/zerobrew/pull/480) | 维护者有要求待处理 | CHANGES_REQUESTED：清理逻辑只删空目录才接受 | 0.6 |
| [zitadel/oidc#994](https://github.com/zitadel/oidc/pull/994) | 维护者有要求待处理 | 暂缓：维护者不确定是否该修，先在 issue 讨论 | 21.1 |

## 规律与改进建议

1. **先查项目的 AI 政策再选题。** 一半的关闭来自明确不接受 AI 贡献的项目。提交前读 CONTRIBUTING、CODE_OF_CONDUCT 和组织主页的 AI policy，有限制的直接跳过。
2. **避开 good first issue 标签。** pyinstaller、supercollider 的维护者都指出这类 issue 是给新人练手的。优先选 help wanted、bug 或维护者已确认待修的 issue。
3. **同一组织一次只提一两个。** 10-22 晚 benbalter 收到 7 个、hanami 5 个、dry-rb/OpenCHAMI/tuProlog/helix-editor 各 4 个；Hanakai 的 8 个被一条评论全部关掉，mocha 的机器人因 24 小时内 fork 13 次把账号判为自动化。分散到不同日子、不同组织。
4. **精简 PR 描述。** heapless 维护者认可改动，但批评描述冗长重复。只写问题、改法、怎么验证；动机里不要写“用剩余额度帮项目”。
5. **提交前查重和查认领。** 被取代的 4 个都是维护者自己动手或已有更合适方案；spring-lens 要求先在 issue 认领。提交前看 issue 最新评论、关联 PR 和最近提交。
6. **新锐项目回报最好。** 新锐层级已决合并率最高（84%），高星最低（44%）。可以提高新锐比例，高星只挑明确欢迎外部贡献的。
7. **及时回应维护者。** 上表 10 个“维护者有要求待处理”的 PR 处理掉就可能转为合并；需要 CLA 的仓库提交前就排除。
