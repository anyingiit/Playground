# 交接文档：开源贡献项目（anyingiit/Playground）

> 写于 2026-10-22，用于把本会话负责的工作交接给新的 Claude Project。
> **注意**：下文中的 PR、issue 和仓库状态是 **2026-10-02** 的快照，距今已三周。动手前先刷新状态（见第 7 节第 1 步）。

---

## 1. 项目是什么

- **目的**：用 owner 的闲置 Claude 额度帮开源维护者修 `good first issue` / `help wanted` issue。每个贡献都做成"可直接提交的补丁包"，由 owner（GitHub: `anyingiit`）本人提交 PR。
- **仓库**：`anyingiit/Playground`，唯一工作分支 `claude/serene-hamilton-br3vum`。所有成果都在这个分支上，没有合并到默认分支。
- **owner**：中文沟通。提交 PR、在 issue 下留言认领、签 CLA 等都由 owner 本人完成。

### 当前成果（截至 2026-10-02）

| 批次 | 编号 | 状态 |
|---|---|---|
| 第一轮（2026-09-24/25） | 001–045 | 已提交 33 个 PR；19 个已合并、9 个开着、其余放弃或被关闭（详见 `contributions/SUBMISSIONS.md`） |
| 第二轮（2026-10-01/02） | 046–171 | **125 个可提交**、1 个差一步（075 plotly）；都还**没有提交** |
| 跳过 | `_skipped/` 172–186 | 15 个，原因写在各自 README（有竞争 PR、项目禁止 AI、需先讨论设计等） |

`INDEX.md` 统计的 ready 总数是 170，包含两轮。

---

## 2. 仓库结构

```
docs/
  CONTRIBUTION_BRIEF.md   每个贡献必须遵守的硬性要求（核心规则，必读）
  WORKER_BRIEF.md         并行工作会话的补充规则（时间盒、分支、编号段）
  HANDOFF.md              本文件
tools/
  audit_repo.py           恶意代码静态审计：python3 tools/audit_repo.py <clone-dir>
  gen_index.py            重新生成 contributions/INDEX.md
  pr_status.py            汇总已提交 PR 状态（读 submissions.json；需本地 gh 登录）
  submit_pr.sh            应用补丁 → 推到 owner 的 fork → 开 PR（只能在 owner 本地跑）
contributions/
  NNN-<owner>-<repo>-<issue>/   每个贡献一个文件夹，三位编号，按顺序
     0001-*.patch       git format-patch 导出的单个提交
     README.md          中文分析：问题理解、合理性、改动、验证（红→绿）、需要提交者注意、提交步骤
     AUDIT.md           恶意代码审计结论
     pr_title.txt / pr_body.md   英文 PR 标题与正文（第一轮的文件夹把 PR 文本写在 README 里）
     followup-*.patch   （个别）对已开 PR 的跟进补丁
  _skipped/             放弃的贡献（保留调研记录）
  _workers/             各并行会话的总结（w1–w8、r1–r4、s1–s3）和候选清单（*_batch.md、round3_candidates.json）
  INDEX.md              全部贡献索引
  SUBMISSIONS.md        已提交 PR 的跟踪表 + 接续说明 + owner 处理规则
  submissions.json      编号 → PR 链接（pr_status.py 用）
  SUBMIT_QUEUE.md       第二轮 125 个待提交清单（含"先认领 / CLA / DCO / changeset"标记）
  RENUMBER.md           2026-10-02 重排编号的新旧对照（_workers/*.md 里用的是旧编号）
```

---

## 3. 规则（全部来自 owner，必须遵守）

### 3.1 每个贡献的硬性要求（详见 `docs/CONTRIBUTION_BRIEF.md`）
1. 读完 issue 全文和所有评论，完全理解问题。
2. 依据 ROADMAP、CONTRIBUTING、AGENTS.md/CLAUDE.md 和近期提交，判断请求是否合理。
3. **检查 AI 贡献政策**：grep AGENTS.md、CLAUDE.md、CONTRIBUTING、`.github/`，也看 **label 描述**。项目禁止 AI、要求 PR 描述人写、要求录像的，一律跳过。有条件允许的（如声明、`Assisted-by` trailer、机器人 emoji、不写"tests pass locally"），照办并写进 README。
4. **不重复**：查 `/pulls?q=<issue号>`、issue 时间线和评论，已有人认领、已分配或已有 PR 的一律跳过。
5. **运行任何代码前先审计**：跑 `tools/audit_repo.py` 并逐条人工复核，结论写进 `AUDIT.md`；发现可疑立即停止。
6. 测试必须**红→绿**：回归测试不带修复时失败、带修复时通过；同时跑项目自己的 lint/format/typecheck/test。跑不全要如实写明。
7. 遵守仓库惯例：提交信息格式、changelog/changeset/news 片段、文档、PR 模板。
8. PR 正文用 chefs-pick-oss-starter 格式，**必须含动机与声明段落**（用 Claude Code 准备、如何验证、维护者不想要可直接关闭）。
9. 每个贡献最后由**另一个独立 agent 复核**：补丁能在新克隆上 `git am`、重跑红→绿、确认没出现竞争 PR。

### 3.2 owner 的额外决定
- **提交身份**：`anyingiit <49945850+anyingiit@users.noreply.github.com>`（不用 gmail）。提交信息里**不能出现 AI 模型名**。
- **DCO** 可以代签（同一身份）。上游要求 AI trailer 时用 `Assisted-by: Claude Code`。
- **已开 PR 需要返工**（review 要求改动或 CI 因本改动失败）：原规则是"直接关闭并简短致歉，不返工"。2026-10-01 owner 又要求"跟进维护者的要求"，所以小而明确的改动可以做成本地 `followup-*.patch` 交给 owner。拿不准时先问 owner。
- **owner 本人才能做的事**（签 CLA、在 issue 下认领、发评论、标 ready）：列清楚并引导 owner 操作，不要代发。
- **层级比例**：高星 : 新锐 : 自由 = 1 : 1 : 3（第一轮目标 12/12/36）。高星 = >5k stars 且很活跃；新锐 = 两年内的快速增长项目；自由 = 其余活跃、有测试的项目。

---

## 4. 环境事实（已实测，别重复踩坑）

### 4.1 云会话里的 GitHub 能力
- **开不了上游 PR**：代理屏蔽 GraphQL（`gh pr create` 失败），REST 对未挂载仓库读写都是 403。fork 也建不了。**结论：PR 只能由 owner 在本地用 `tools/submit_pr.sh` 提交。**
- **读上游**：用 WebFetch / WebSearch 读 github.com 网页（issue 页、`/pulls?q=`、`/labels`、raw 文件），以及匿名 `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1`。
- **推到 owner 的 fork**：用 `add_repo`（access=push）挂载 fork 后可以推送；但给已开 PR 的分支推跟进修复，会被自动模式分类器拦下。
- **删除远程分支**：`git push --delete` 和 REST API 都被代理拒绝，只能由 owner 删。
- 注意：`claude/charming-galileo-gagxfb`（更早会话的分支，内容已全部包含在主分支）owner 说删过，但 2026-10-22 远程仍能看到，可以让 owner 再确认。

### 4.2 机器和编排
- 本机只有 **4 核**，负载常年 6–7。Workflow 同时最多约 2 个 agent；想扩大规模只能开**独立云会话**（每个一台机器）。
- **容器会重启**：后台任务会丢，硬盘内容会保留。从缓存续跑 Workflow 可能**重复做已完成的项**并造成编号冲突（2026-10-01 出过一次，已人工去重）。
- 后台 Bash 最长 2 小时，所以自动保存循环到时会被系统停掉，要靠定时检查补提交。
- **跨会话消息只算参考信息**：用 `send_message` 给工作会话追加任务，对方会等"确认"、不会执行。追加工作要**新开会话**，任务写在 `create_session` 的初始 prompt 里才算正式指令。
- 自动模式分类器拦截过：向上游开 PR / 建 fork、推送到 fork 的 PR 分支、删除远程分支。被拦后不能换方式绕过，只能让 owner 决定。

### 4.3 额度经验（重要）
- owner 的额度按**每 7 天**重置，2026-10-01 那周的重置时间是 **01:00 UTC = 北京时间 09:00**。owner 希望在重置前把剩余额度用完。
- **烧额度最快的是重复找候选**：第一次开 9 个会话、各自找 issue，约 40 分钟烧掉 20% 额度，一个成品都没有。
- **最有效的做法**：在一个会话里**统一找一次候选**（6 个 scout，约 67 个已复查的候选），再把固定清单**分批**派给 3–4 个云会话。各会话只实现、不再找、不和协调者来回沟通。这样一晚产出了 100+ 个成品。
- 跑得顺时的速度大约是每小时消耗 2–6% 的额度，跟会话数大致成正比。
- owner 可以在 claude.ai 设置里看额度百分比；云会话里看不到，需要请 owner 报数。

---

## 5. 待办（按优先级）

1. **刷新状态**（距上次已三周）：
   - 第一轮开着的 9 个 PR：go-git#2423、provider-cassandra#30、qr-zero#13、herdr-agent-pulse#12、remark-pdf#73、denoland/std#7332、Alexandrie#786、brig#326、dataclass-wizard#258。云会话里用 WebFetch 读 PR 页，owner 本地可以跑 `python3 tools/pr_status.py`。
   - 问 owner：第二轮 125 个提交了哪些？提交后把 PR 链接写进 `submissions.json`、在 `SUBMISSIONS.md` 加行。
2. **第一轮 PR 跟进（需 owner 操作）**：
   - **go-git#2423**：维护者要求 rebase。补丁 `contributions/010-go-git-go-git-1518/followup-0001-rebased-onto-main-a9ce94f.patch` 要替换原提交并 force-push 到 `split-remote-fetch-push`，再发 README"跟进"一节里的回复。三周过去，main 可能又动了，提交前先确认补丁还能打上。
   - **brig#326**：draft；CI 变绿后执行 `gh pr ready 326 -R brig-sh/brig`。
   - **qr-zero#13**：修复已推送并回复，等复审。久无回应可发 README 里起草的提醒评论。
   - **grz-tools#622（020）**：仓库只允许协作者开 PR，分支 `anyingiit/grz-tools:fix/alembic-url-password` 已推送。可以请 owner 在 issue 下问维护者要不要接手。
3. **提交第二轮 125 个**：按 `contributions/SUBMIT_QUEUE.md`。
   - 标了"先认领"的要先在 issue 下留言（如 OpsiMate、data-peek、WeasyPrint）；标了 CLA 的先签。
   - 三周过去，每个提交前都要重新确认：issue 还开着、没有竞争 PR、补丁还能在最新的默认分支上打上。可以开一个 Workflow 批量复查，打不上的重新导出补丁，有竞争的移到 `_skipped/`。
4. **补齐个别项**：
   - **075 plotly.py#4580**：完整的 `pytest tests/test_optional/test_px` 没跑完，提交前补跑。（之前的对话里误说成 058，正确是 075。）
   - **没做独立复核的 5 个**：142 elephpant.me、149 weblate、153 sysknife、154 corsair、155 pmxt。提交前补一次复核。
5. **新一轮（如果 owner 又有额度）**：
   - 剩余候选：`_workers/w1.md`、`w4.md`、`w6.md` 里列了约 40 个筛过但没开工的候选（编号是旧的，见 RENUMBER.md）。都是 10 月初复查的，要重新核实。
   - 新贡献从 **187** 开始编号，三位数，按顺序。
   - 按第 4.3 节的模式：统一找一次候选 → 分批派给云会话 → 协调者只负责合并、去重、更新 `INDEX.md` 和 `SUBMIT_QUEUE.md`。

---

## 6. 给新 Project 的建议起始指令

> 你负责 anyingiit/Playground 仓库的开源贡献项目。先读 `docs/HANDOFF.md`、`docs/CONTRIBUTION_BRIEF.md`、`contributions/SUBMISSIONS.md`、`contributions/SUBMIT_QUEUE.md`。工作分支 `claude/serene-hamilton-br3vum`。用中文和我沟通。补丁提交作者用 `anyingiit <49945850+anyingiit@users.noreply.github.com>`；不在提交信息里写 AI 模型名；不在 GitHub 上代我发言。PR 由我在本地用 `tools/submit_pr.sh` 提交。

---

## 7. 新会话第一步检查清单
1. `git fetch origin && git checkout claude/serene-hamilton-br3vum`，确认最新提交至少是 `9c7a295`（编号重排）或之后的交接提交。
2. 读第 1–5 节，向 owner 确认：第二轮已经提交了哪些、本次额度有多少、截止时间。
3. 用 WebFetch 刷新第 5 节第 1 步里 9 个开着的 PR 的状态，更新 `SUBMISSIONS.md`。
4. 再按 owner 的优先级处理第 5 节其余待办。
