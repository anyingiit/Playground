# supercollider/supercollider #7556 — LinExp.ar with mixed-rate params goes off the rails

| 项 | 值 |
|---|---|
| Issue | https://github.com/supercollider/supercollider/issues/7556 |
| Tier | 高星 |
| Labels | bug, comp: server plugins, good-first-issue |
| Status | ✅ ready（已通过独立复审）— patch + PR 文本已就绪，sclang UnitTest 实际跑过 red→green |
| 重复 PR 检查 | 2026-10-01：`is:pr is:open 7556` 无结果；`is:pr LinExp` 只有无关的已关闭 PR（#6172、#5730 等）。issue 无 assignee、无评论。 |
| Base | `develop` @ 7e6f20928cc4（"sclang: add setCanCallOS() (#7748)"） |

## 问题理解
`{LinExp.ar(DC.ar(0.5), -1.0, 1.0, 1.0, DC.ar(2.0))}.plot` 输出乱掉；换成 `DC.kr(2.0)` 时结果正确（`0.5.linexp(-1,1,1,2) = 1.6817928`）。

根因在 `server/plugins/LFUGens.cpp`：`LinExp_SetCalc` 只要 srclo/srchi（或 dstlo/dsthi）里**任意一个**是 audio rate，就选 `_aa` / `_ak` / `_ka`。这些函数对整对输入都用 `ZXP` 逐采样前进。scalar / control rate 输入只有 1 个采样，于是读越界到别的 wire buffer / 垃圾内存。issue 的例子：dstlo 是 scalar、dsthi 是 audio，走 `_ka`，`ZXP(dstlo)` 越界。

## 合理性判断
- 维护者打了 bug + good-first-issue，issue 里已经指向这段代码，修法没有设计争议。
- 采用最小改动：保持 calc 函数的选择逻辑和各变体的预计算不变，只让 audio-rate 的输入前进（step=1），其它输入 step=0 当常量读。原有的 `/` 和 `sc_reciprocal` 语义不变，所以原本正确的组合（整对都 ar，或全 ir/kr）输出逐位不变。
- Ctor 不动（它用 ZIN0 算初始采样，本来就对）。

## 改动
- `server/plugins/LFUGens.cpp`：新增 `static inline int LinExp_inputStep(LinExp*, int)`（`INRATE(i) == calc_FullRate ? 1 : 0`）；`LinExp_next_aa/_ak/_ka` 改为用 `IN(i)` 指针 + step 前进，不再用 `ZXP` 读参数输入。
- `testsuite/classlibrary/TestCoreUGens.sc`：新增 `test_linexp_mixedRateInputs`，对 srclo/srchi/dstlo/dsthi 的 scalar / `DC.kr` / `DC.ar` 全部 81 种组合，渲染 `LinExp.ar(DC.ar(0.5), ...)` 并和 `0.5.linexp(-1,1,1,2)` 比较（within 1e-5）。wiki 要求 bug 修复带回归测试。
- 没改 CHANGELOG.md（release 时统一整理），在 PR body 的 Merge notes 里给了建议的 release note。

## 验证
环境：Ubuntu 24.04、GCC 13、clang-format 18。

1. **sclang UnitTest（真实 scsynth + sclang）**：
   ```bash
   apt-get install -y libsndfile1-dev libfftw3-dev libjack-jackd2-dev libasound2-dev libreadline-dev jackd2 cmake ninja-build
   # 子模块 nova-simd / nova-tt / yaml-cpp / utf8proc 按 git ls-tree 的 pinned commit clone
   cd build && cmake -G Ninja -DCMAKE_BUILD_TYPE=Release -DSC_QT=OFF -DSC_IDE=OFF -DSUPERNOVA=OFF -DSC_HIDAPI=OFF -DSC_ABLETON_LINK=OFF -DNO_AVAHI=ON -DNO_X11=ON -DSC_EL=OFF -DSC_VIM=OFF -DINSTALL_HELP=OFF -DENABLE_TESTSUITE=OFF .. && ninja -j2
   jackd --no-realtime -d dummy -r 48000 -p 64 &
   SC_PLUGIN_PATH=$PWD/server/plugins ./lang/sclang -l verify/conf.yaml verify/run.scd
   ```
   （`verify/run.scd` 跑 `TestCoreUGens.runTest("TestCoreUGens:test_linexp_mixedRateInputs")`）
   - Red（LFUGens.cpp 还原成 develop，只重编 LFUGens）：`PASSES: 26 / FAILURES: 56`，例如 `[scalar, scalar, scalar, audio]` 输出 `nan, 216232.64, ...`，期望 1.6817928。
   - Green（带修复）：`PASSES: 82 / FAILURES: 0`（81 个组合 + 1 个 timeout 断言）。
2. **完整 `TestCoreUGens.run`（带修复）**：652 pass / 1 fail。失败的是 `test_demand`（"Duty should free itself after a limited sequence"），在未修改的 develop 上同样失败（JACK dummy + non-realtime 环境问题），与本改动无关。
3. **独立 C++ harness**（`verify/harness.cpp`，不在 patch 里）：`#include` LFUGens.cpp，伪造 Wire/Unit，非 audio 输入是 1 个采样 + NaN 毒化内存，校验 81 种组合：
   ```bash
   g++ -std=c++17 -O2 [-DNOVA_SIMD] -I include/plugin_interface -I include/common -I external_libraries/nova-simd -I external_libraries/boost -I server/plugins verify/harness.cpp -o h && ./h
   ```
   Red：`56/81 rate combinations wrong`；Green：`0/81`（带和不带 NOVA_SIMD 都是）。
4. `ninja -j2`（全部 target）编译通过；`clang-format --lines` 对改动区域无变化（仓库 pre-commit 用 clang-format 14，CI 不强制格式）。

## 独立复审（2026-10-01）
- 重读 issue：修复正对 issue 例子（dstlo scalar + dsthi audio → `_ka`）以及同类 `_aa`/`_ak` 情况。
- 复审者亲自复现 red→green：用 `verify/harness.cpp`，把 `LFUGens.cpp` 还原为 develop 版本 → `56/81 rate combinations wrong`；恢复修复 → `0/81`。
- `git ls-remote` 确认 upstream develop 仍为 7e6f20928cc4；在该 base 的干净 worktree 上 `git am` 干净应用。
- `clang-format-18 --lines`（改动行）无差异；patch 中无 AI 模型名；author 为 anyingiit。
- sclang 全量构建未在复审中重跑（成本高），以实现者记录为准。

## 需要提交者注意
- PR body 勾选了 "All tests are passing"，但本地 `test_demand` 失败（base 上同样失败、与本改动无关，PR body 已说明）；如 CI 有不同结果请据实修改。
- 仓库没有 AI 政策（CONTRIBUTING.md、.github、wiki 都查过），不需要 DCO / Signed-off-by，也不需要 AI trailer，patch 里都没有加。
- commit 标题遵循 wiki 的 "component: sub-component: description" 格式。
- PR body 已合并仓库模板（Purpose and Motivation / Types of changes / To-do list / Merge notes）。
- `test_demand` 在本环境的失败与本改动无关（base 上同样失败），如 CI 正常则无需关注。

## 如何提交
```bash
git clone https://github.com/supercollider/supercollider && cd supercollider
git checkout -b fix-linexp-mixed-rate-inputs origin/develop
git am /home/user/Playground/contributions/121-supercollider-supercollider-7556/0001-plugins-LinExp-fix-audio-rate-params-mixed-with-scal.patch
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/121-supercollider-supercollider-7556 supercollider/supercollider develop fix-linexp-mixed-rate-inputs contributions/121-supercollider-supercollider-7556/pr_title.txt contributions/121-supercollider-supercollider-7556/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
