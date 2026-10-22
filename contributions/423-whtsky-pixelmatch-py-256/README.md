# 423 — whtsky/pixelmatch-py#256: 移植上游 v8 的 ignore_mask

| 项 | 内容 |
|---|---|
| Issue | https://github.com/whtsky/pixelmatch-py/issues/256 |
| 层级 | 自由（mapbox/pixelmatch 的 Python 移植，PyPI 包 `pixelmatch`） |
| Labels | enhancement, **pr welcome**（维护者 whtsky 10-08 打的） |
| Base 分支 | `master`（补丁基于 669c3c7） |
| 状态 | ✅ 可提交 |
| 重复检查 | 2026-10-22：issue 无评论、无指派、无关联 PR；开着的 3 个 PR 是 2 个 renovate + 2023 年的性能 PR #164，均无关 |
| AI 政策 | 仓库无 CONTRIBUTING / AI 条款 |
| CLA/DCO | 无 |

## 问题理解
上游 pixelmatch v8（mapbox/pixelmatch#171，已合并）新增 `ignoreMask`：每像素一个值，非零则跳过比较、在 diff 输出中按“未变化”绘制；快速路径也忽略掩码内差异。issue 列了 4 条验收标准（同尺寸、PIL 接受 Image 或 list、core 接受 list、非零跳过、快速路径跳过）。

## 改动
- `core.py`：`ignore_mask` 参数、长度校验、快速路径（掩码外全相同即走快速路径）、主循环中掩码像素 delta=0。
- `contrib/PIL.py`：接受 PIL.Image（转 "L"）或序列；尺寸校验；透传给 core。
- README API 文档。没改 Changelog（该节条目都带 PR 链接，留给维护者/PR 号确定后再加，PR 正文已说明）。
- 注意 Python 版仍是旧的 YIQ 算法（上游 v8 已换 OKLab），所以不能直接复用上游 9/10 号 fixture 的期望数，改为用现有 1a/1b 构造与上游同样的“上半部掩码”测试，并用“掩码外 diff 像素数”作期望，结果不依赖颜色算法。

## 验证
- 红：不带源码改动，4 个新测试全部失败（TypeError: unexpected keyword）。
- 绿：按 CI 命令 `pytest --mypy --cov=pixelmatch --cov-report term-missing --benchmark-disable` → 51 passed，mypy 无问题；`black --check .` 通过。core.py 未覆盖的 3 行是既有的尺寸校验分支。
- fixtures 是 LFS，代理拒绝 LFS，改从 media.githubusercontent.com 下载并逐个核对 sha256 与 LFS 指针一致。

## 需要提交者注意
- 提交信息 Conventional Commits（`feat:`），与仓库历史一致。
- 本地 clone 时需 `git lfs pull` 才能跑测试（本机正常有 LFS 权限即可）。

## 如何提交
```
git clone https://github.com/whtsky/pixelmatch-py && cd pixelmatch-py && git checkout -b feat-ignore-mask origin/master
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
- **补丁应用**：全新 `GIT_LFS_SKIP_SMUDGE=1` clone，origin/master = 669c3c7，`git am` 干净应用。33 个 fixture 从 pm-fixtures 拷入前逐个核对 sha256，与 LFS 指针 oid 全部一致。
- **语义对照上游**（pm-js index.js / test.js / README）：长度校验（`width*height`，报错文案 "Ignore mask size does not match…"）、快速路径条件（相当于 `a32[i] !== b32[i] && !ignoreMask[i]`）、主循环中掩码像素 delta=0 → 按灰度背景绘制、不计数、不触发 fail_fast、diff_mask 下不画；抗锯齿检测仍读邻居像素：均与上游一致。测试里的半掩码（`i <= size/2`）与上游 diffTest 一致。issue 的 4 条验收标准都满足（issue 无新评论、无指派、无关联 PR）。
- **边界与混合输入**（自写脚本）：list/bytes/tuple/bytearray 混搭的 img1、img2、mask，计数和输出都与纯 list 一致。类型不同时 `img1 == img2` 和切片比较恒为 False，快速路径不会走，但主循环结果完全相同，这和改动前的行为一样。全掩码返回 0；PIL 的 "1"/"L"/"RGBA"/"P" 掩码图都正确；`ignore_mask=None` 正常。
- **性能**（ignore_mask=None，1/3/4 号 fixture，min-of-7，base 与 patched 各跑两轮）：差异在 ±5% 噪声内，而且方向不一致，可以忽略。主循环每像素只多一次 `is not None` 判断。
- **红→绿**：只把 pixelmatch/ 回退到 HEAD~1 → 4 个新测试全部失败（TypeError）。恢复后跑 CI 命令 → 51 passed，mypy 无问题，core.py 只剩既有的 50/52/57 三行未覆盖（PIL.py 100%）；`black --check .` 通过。3 条 PytestBenchmarkWarning 是改动前就有的。
- **变异测试**：故意改坏 core.py 来验证测试。“掩码像素画红但不计数”“掩码像素不绘制”“主循环忽略掩码”“去掉长度校验”“快速路径不绘制”都被测试抓到。“快速路径不看掩码”和“快速路径下标错位”没被抓到，原因是快速路径和主循环在可观测结果上完全等价（计数与输出相同），它只是性能优化，上游测试同样无法区分。这不影响正确性，不算问题。如果维护者要求，可以 mock `color_delta` 断言它没被调用。
- **竞争 PR**：open 的 PR 只有 #265、#250（renovate）和 #164（2023 年的性能优化，会改 core.py 主循环）。没有和 ignore_mask 相关的。如果 #164 先合并，可能需要 rebase。
- **pr_body.md**：英文；首两行是 attribution 块；有 Motivation / disclosure 段；描述的行为和数字（51 passed、未覆盖行、4 个新测试红）都经本次复核确认属实。未发现需要修改的文档问题。

结论：PASS
