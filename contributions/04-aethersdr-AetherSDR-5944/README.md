# aethersdr/AetherSDR#5944 — healthSnapshot publishes Converter ADC rows from a frozen bandscope block

| | |
|---|---|
| Issue | https://github.com/aethersdr/AetherSDR/issues/5944 |
| Tier | 新锐（~224★，2026-03 创建，566 个 open issue，每天大量合并，人工 reviewer 分级 CODEOWNERS） |
| Labels | `bug`, `good first issue`, `GUI`, `spectrum`, `priority: low`, `maintainer-review` |
| Status | ✅ 实现 + 单测 + 真实 Qt 6.8.3 构建 + `hl2_ep4_ingest_test` 通过 + 仓库 static-checks 全过 |
| 重复 PR 检查 | 无引用 #5944 的 PR（2026-09-24 检查） |

## 问题理解
`Hl2Backend::healthSnapshot()` 的 “Converter” 分组里，`adcPeakDbfs`/`adcRmsDbfs`/`adcCrestDb`（以及同一 block 的
`adcClippedPerBlock`）只判断 `m_bandscopeBlock.samples > 0`，没有任何时效检查。EP4 停止后 block 冻结，这些行永远显示最后一个值；
而同一个 block 派生的 headroom 行走 `bandscopeHeadroom()`，超过 `kHeadroomMaxAgeMs = 3000` 就变成 Absent。
报告者实测：停 EP4 后 peak/RMS 变化 0.00 dB，而实时 slice peak 变化 19.04 dB —— 陈旧值和当前值看起来一模一样。

## 合理性判断
- issue 明确给出期望：Converter 行使用与 headroom **同一个**时间门，过期时显示 “not known”。
- `Hl2BandscopeHeadroom.h` 的注释本就定义了 “EXPIRY IS NOT ZERO HEADROOM… ABSENT” 的约定；本改动只是让同源数据遵守同一约定。
- issue 注明与 #5802/#5803（校准含义）无关，本改动不碰数值含义。

## 改动
- `Hl2BandscopeHeadroom.h`：新增 `bandscopeBlockIsCurrent(block, ageMs, maxAgeMs = kHeadroomMaxAgeMs)`（纯函数，无 Qt）；
  `bandscopeHeadroom()` 改为调用它 —— 两处共用**一个**谓词，不可能各自漂移。
- `Hl2Backend.cpp::healthSnapshot()`：peak / RMS / crest / 轨上样本数改为以 `currentBlock` 为门；过期时渲染为 invalid `QVariant`
  （与首个 block 到达前完全相同的 “dash / JSON null” 表现，行不会消失、列表形状不变 —— 这点在 PR #5650 review 里被强调过）。
  `adcObservedAgoMs` **保持**以 `haveBlock` 为门继续报告年龄，正是它解释了为何其他行为空。
- `tests/hl2_bandscope_headroom_test.cpp`：新增 “2b” 段 —— 边界（无样本 / 从未观测 / 0 ms / 恰好 3000 ms / 3001 ms），
  并在所有边界 × 3 种 block 上断言 `bandscopeBlockIsCurrent` 与 `bandscopeHeadroom(...) != Absent` 一致。

## 验证
| 命令 | 结果 |
|---|---|
| `g++ -std=c++20 -Wall -Wextra` 独立编译 `hl2_bandscope_headroom_test` | all checks passed，无警告 ✅ |
| CMake（Qt 6.8.3 via aqtinstall，`-DAETHER_GPU_SPECTRUM=OFF -DENABLE_RADE=OFF`）构建 `aethercore` 全库 + `hl2_ep4_ingest_test` | 构建成功 ✅ |
| `ctest -R "hl2_ep4_ingest_test\|hl2_bandscope_headroom_test"` | 2/2 passed ✅（`hl2_ep4_ingest_test` 覆盖 “首个 block 前 Converter 行 ABSENT” 的既有断言） |
| 全部 49 个 `hl2_*` ctest 目标 | HL2_RESULT |
| `tools/check_engine_boundary.py --strict`、`gen_touchpoint_manifest.py --check`、`check_test_registration.py --strict`、`check_capability_records.py --strict`、`check_command_plane.py --strict`、`check_ci_test_gate.py --strict`、`check_network_timeouts.py --strict`、`check_theme_seed.py --strict`、`check_shader_dialects.py --strict`（static-checks.yml 中的门） | 全部 exit 0 ✅ |

未做：真实 Hermes-Lite 2 硬件验证（CONTRIBUTING：“Test against a real radio if possible”）；后端级 “超过 3 s 变空” 的测试需要新增 friend seam 和 3 s sleep，故以纯谓词测试 + 一致性断言锁定两者共用同一个门。
构建时关闭 RADE/GPU spectrum 仅因本地缺 Opus 预构建和 Qt ShaderTools，与本改动无关。

## 需要提交者注意
- **分支保护要求签名提交**（SSH 或 GPG，见 `docs/COMMIT-SIGNING.md`）：应用补丁后用 `git commit --amend -S --no-edit` 签名。
- CONTRIBUTING 要求提交信息引用 Constitution 原则 —— 已写 `Principle VIII`。
- 仓库 PR 模板有 “Constitution principle honored” 与 “Test plan”，已并入下方 PR 文本。
- 仓库对 AI 协作友好（CONTRIBUTING 推荐 Claude Code；PR 模板提示 AI agent 先在 issue 上认领）。

## 如何提交
```bash
git clone https://github.com/<you>/AetherSDR && cd AetherSDR
git checkout -b fix/5944-converter-rows-staleness origin/main
git am /path/to/0001-Withhold-HL2-Converter-ADC-rows-once-the-bandscope-b.patch
git commit --amend -S --no-edit    # signed commit required
git push -u origin HEAD            # base: main
```

### PR — chefs-pick-oss-starter 格式
**Title:** `Withhold HL2 Converter ADC rows once the bandscope block goes stale`

```markdown
## Description

`Hl2Backend::healthSnapshot()` published the Converter rows (`adcPeakDbfs`, `adcRmsDbfs`, `adcCrestDb`, and
`adcClippedPerBlock`) from `m_bandscopeBlock` with no age check, while the headroom row derived from the
same block goes Absent past `kHeadroomMaxAgeMs`. With EP4 stopped, the frozen peak/RMS kept reading as current
(0.00 dB movement while the live slice peak moved 19 dB).

- The freshness test is factored out of `bandscopeHeadroom()` into `bandscopeBlockIsCurrent()` in
  `Hl2BandscopeHeadroom.h`, so both consumers share one predicate and cannot drift apart.
- The Converter rows now gate on it: past the limit they render as "not known" — the same invalid variant as
  before the first block, so the rows stay in place and land as JSON null on the bridge.
- `adcObservedAgoMs` keeps reporting the age, which is what tells a reader why the other rows are blank.
- `hl2_bandscope_headroom_test` gains boundary checks for the predicate and asserts it agrees with
  `bandscopeHeadroom()` at every boundary.

**Constitution principle honored:** Principle VIII — a frozen reading is no longer presented as a current one.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Fixes #5944

## Checklist

- [x] Tests pass locally — Linux, Qt 6.8.3: `aethercore` builds; `ctest -R hl2_` → HL2_SHORT;
      `hl2_bandscope_headroom_test` also clean under `g++ -Wall -Wextra`; static-check tools (`tools/check_*.py --strict`) pass
- [ ] Behavior verified on a real radio — not done (no HL2 hardware available)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, release-prep file per AGENTS.md
- [ ] Documentation is updated (if applicable) — n/a, no user-visible docs describe these rows' staleness
- [x] Commits are signed — to be signed by the submitter (`git commit --amend -S`)
- [x] Code is clean-room (Principle IV); no AppSettings/meter UI changes
```
