# TheAlgorithms/C-Plus-Plus#3234 — Doxygen does not render JAVADOC_BANNER style comments

| 项 | 值 |
|---|---|
| Issue | https://github.com/TheAlgorithms/C-Plus-Plus/issues/3234 |
| Tier | 自由 |
| Labels | bug, good first issue |
| Status | ✅ ready — patch + PR text done (not submitted)；独立复审通过 2026-10-01 |
| Base | `master` @ b64d5ec (2026-09-30, "ci: fix up .clang-tidy and related files (#3236)") |
| Duplicate-PR check | 2026-10-01：`pulls?q=3234` 0 结果；关键词 `javadoc OR banner OR JAVADOC_BANNER` 只有 2024 年无关的已关闭 #2794；`is:pr doxygen` 只有 #3229（只改 `CONTRIBUTING.md` 里反引号转义，属于另一个 Doxygen bug，与本补丁无文件重叠）。Issue 无评论、无 assignee、无关联分支/PR |

## 问题理解

Issue 由维护者 realstealthninja 于 2026-09-29 开，指出部分文件用 Javadoc banner 风格注释（`/*****...`）写文档，Doxygen 不渲染：GitHub Pages 的文件列表里这些文件是**粗体**（无文件页面、点不进去）。Issue 直接引用了 `doc/Doxyfile` 第 228 行，即 `JAVADOC_BANNER = NO`。

仓库中用 banner 的文件：`search/binary_search.cpp`、`search/interpolation_search.cpp`、`sorting/selection_sort_iterative.cpp`、`dynamic_programming/partition_problem.cpp`、`geometry/graham_scan_algorithm.cpp`、`geometry/graham_scan_functions.hpp`（这 6 个用 banner 写 `@file`），另有 `data_structures/cll/cll.h`（banner 当分节标题）、`data_structures/morrisinorder.cpp`（`@author` banner）、`numerical_methods/durand_kerner_roots.cpp`（`/***` 的 main 注释）。

## 合理性判断

- 维护者自己开的 bug + good first issue，并指向 Doxyfile 那一行 → 预期修复就是打开 `JAVADOC_BANNER`。
- 也可以改写 9 个文件的注释，但那样跨多个目录（CONTRIBUTING 说跨目录 PR 常被拒），且以后新文件还会再犯；改配置一行最小、最直接。
- AI 政策：CONTRIBUTING / REVIEWER_CODE / CodingGuidelines / PR 模板 / label 描述均无 AI 相关规定（grep `AI|LLM|Copilot|ChatGPT` 无结果）。

## 改动

- `doc/Doxyfile`：`JAVADOC_BANNER = NO` → `YES`（1 行）。CMake 的 `doc` target（`doxygen_add_docs(... CONFIG_FILE doc/Doxyfile)`，gh-pages workflow 用 `cmake --build build -t doc`）直接使用这个文件，不需要改 CMakeLists。

## 验证

环境：`apt-get install doxygen`（1.9.8；Doxyfile 头写的是 1.12.0，CI 在 macOS 上 brew 最新版，`JAVADOC_BANNER` 自 1.8.17 起存在）。仓库没有文档测试，所以回归检查用本目录的 `check_banner_docs.sh`（**不在补丁中**）：在仓库根目录用 `doc/Doxyfile` 跑 doxygen（追加覆盖 `GENERATE_LATEX=NO HAVE_DOT=NO NUM_PROC_THREADS=2` 以省时间），检查上述 6 个文件在 `files.html` 中是否为粗体（无页面）。每次约 7 分钟。

| 命令 | 结果 |
|---|---|
| `./check_banner_docs.sh <master worktree> /home/user/work/cpp-doxy/red` | 6 个 FAIL（全部粗体、无页面），exit 1 → red |
| `./check_banner_docs.sh <patched clone> /home/user/work/cpp-doxy/green` | 6 个 ok（全部有文件页面），exit 0 → green |
| 渲染内容抽查（patched）：`df/dd5/binary__search_8cpp.html` | 含 "Binary search algorithm" brief、details、Author Lajat Manekar、函数文档 |
| warning 对比（base vs fix，doxygen stderr 2018 → 2024 行） | 新增均为这些文件里**原有**的文档小错误现在被解析出来（如 `@returns void` 写在 void 测试函数上、`@returns @param int` 、`@param array` 名不匹配）；同时消失若干 "not documented"。`WARN_AS_ERROR = NO`，不影响构建 |

未运行：完整 `cmake --build -t doc`（与直接用同一 Doxyfile 跑 doxygen 等价，省掉 CMake 配置/clang 解析环境差异）；代码编译/clang-tidy（未改任何源代码）。

## 如何提交

```bash
git clone https://github.com/TheAlgorithms/C-Plus-Plus && cd C-Plus-Plus
git checkout -b doxygen-javadoc-banner origin/master
git am /path/to/0001-docs-enable-JAVADOC_BANNER-so-banner-style-comments-.patch
git push <your-fork> doxygen-javadoc-banner   # PR 目标分支: master
```
PR 标题见 `pr_title.txt`，描述见 `pr_body.md`（已按仓库 PR 模板 "Description of Change / Checklist / Notes" 结构，并带披露段落）。

### 独立复审（2026-10-01 20:40 UTC）
- 重新读 issue：仍 open、无 assignee、无评论；`pulls?q=is:pr JAVADOC_BANNER` 0 结果；upstream master 仍为 b64d5ec，补丁可直接 `git am`。
- 快速 red→green 复现（只把 6 个 banner 文件作为 `INPUT`，其余同 `doc/Doxyfile`，约 10 秒）：
  `(git show b64d5ec:doc/Doxyfile; echo OUTPUT_DIRECTORY=$OUT; echo GENERATE_LATEX=NO; echo HAVE_DOT=NO; echo "INPUT=<6 files>") | doxygen -`
  → base 配置下 6 个文件在 `files.html` 全部为 `<b>…</b>`（无页面）；用补丁后的 `doc/Doxyfile` 6 个全部有页面。
- 全仓 banner 文件清单（9 个）与上文一致；commit 作者/信息、无 AI 模型名均核对无误。pr_body 仅修正一处措辞。

### 需要提交者注意
- 无 DCO、无 changelog；提交信息用语义前缀（`docs:`），符合 CONTRIBUTING 的 Commit Guidelines。
- 副作用已在 PR 描述说明：`binarySearch()` 函数体内的 banner 注释会被追加到该函数文档；`cll.h` 的分节 banner 会变成下一个成员的文档；会多出少量原有文档错误的 warning。若维护者希望顺便修这些文档小错，可另开 PR。
- #3229 同样与 Doxygen 有关但只改 `CONTRIBUTING.md`，无冲突。
- `check_banner_docs.sh` 只是本地验证脚本，不要提交到上游。
