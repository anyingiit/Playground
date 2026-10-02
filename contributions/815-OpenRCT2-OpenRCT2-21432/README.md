# OpenRCT2/OpenRCT2 #21432 — Replace old constant notation (Entrance.h + NewsItem.h slice)

| 项 | 值 |
|---|---|
| Issue | https://github.com/OpenRCT2/OpenRCT2/issues/21432 |
| Tier | 高星 |
| Labels | good-first-issue, refactor |
| Status | ✅ ready — 独立复审通过（2026-10-01）：upstream develop 仍是 e9fedc1，原名仍在；patch 在干净 checkout 上 `git am` 成功；无重复 open PR |
| 重复 PR 检查 | 2026-10-01：`is:pr is:open 21432` 没有结果；issue 评论里也没人认领 Entrance.h / NewsItem.h。这是 tracking issue，按文件分片做，之前的分片 PR 如 #26974（FontStyle）已合并。 |
| Base | `develop` @ e9fedc1 |

## 问题理解
#21432 是一个长期 tracking issue，要把常量从 SHOUTING_SNAKE_CASE / TitleCase 统一成 `kCamelCase`。贡献者按文件或按组分 PR，每个 PR 只做一小块。

## 合理性判断
- 维护者开的 issue，带 good-first-issue 和 refactor 标签，类似的分片 PR 一直在合并（"Refactor constant notation in Audio.h"、"Replace constant notation in Window.h"、#26974）。
- 这一片很小（10 个文件，34 行），没有被任何 open PR 覆盖。
- 这些常量都是真正的编译期常量（`constexpr` 数值），不属于 issue 里说的"像 inline 方法一样的 constexpr"例外。
- 没有动 `WC_*__WIDX_*`（TileInspectorGlobals.h / WidgetIndexGlobals.h），它们是 widget index 的命名约定，改了风险更大。

## 改动
- `src/openrct2/world/Entrance.h`：`ParkEntranceHeight`、`RideEntranceHeight`、`RideExitHeight`、`MaxRideEntranceOrExitHeight` → 加 `k` 前缀。
- `src/openrct2/management/NewsItem.h`（`News` 命名空间）：`ItemTypeCount`、`ItemHistoryStart`、`MaxItemsArchive`、`MaxItems` → 加 `k` 前缀。
- 使用处：`ParkEntrancePlaceAction.cpp`、`RideEntranceExitPlaceAction.cpp`、`InteractiveConsole.cpp`、`NewsItem.cpp`、`S6Importer.cpp`、`scripting/.../ScPark.cpp`、`ScParkMessage.cpp`、`openrct2-ui/windows/News.cpp`。
- 没有 changelog 条目（之前的同类重构 PR 都没有加）。
- 插件 API 不受影响：这些名字只在 C++ 内部使用（grep 了 `data/` 和 scripting，JS 侧没有暴露）。

## 验证
纯重命名，**没有 red→green 测试**，也不应该有。证据是：能编译、现有测试通过、旧名字已经没有残留。

```bash
# 旧名字已无残留（无输出）
grep -rnwE 'ParkEntranceHeight|RideEntranceHeight|RideExitHeight|MaxRideEntranceOrExitHeight|ItemTypeCount|ItemHistoryStart|MaxItemsArchive|MaxItems' src test
# 只检查改动行的格式（clang-format 18.1.3；无输出 = 干净）
git diff -U0 e9fedc1 | clang-format-diff -p1
# headless 构建 + 测试（需临时给 NetworkServerAdvertiser.cpp 加 #include <future>，见下）
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DWITH_TESTS=ON -DDISABLE_GUI=ON -DDISABLE_DISCORD_RPC=ON -DDISABLE_HTTP=ON -DDISABLE_FLAC=ON -DDISABLE_VORBIS=ON -DDISABLE_OPENGL=ON -DOPENRCT2_USE_CCACHE=OFF -DDOWNLOAD_TITLE_SEQUENCES=OFF -DDOWNLOAD_OBJECTS=OFF -DDOWNLOAD_OPENSFX=OFF -DDOWNLOAD_OPENMUSIC=OFF
ninja -C build -j2
(cd build && ctest -j2 --output-on-failure)
```
编译通过（libopenrct2 + OpenRCT2Tests，GCC 13.3，Debug，scripting 开启）。`ctest`：257 个里 244 个通过，13 个失败，**全部因为本地没有游戏数据**，与本改动无关：
  - `MultiLaunchTest.all`、`PlayTests.*`（3）、`RideRatings.*`（3）、`EntityImportTests.*`（2）、`S6ImportExport*`（2）：初始化 Context 时 `FATAL: Failed to open fallback language`（找不到 `/language/en-GB.txt`，因为 `build/data` 指向安装目录，而这里没有安装）。
  - `FetchAndApplyScenarioPatch.expected_json_format`：同样需要 data 目录（scenario_patches）。
  - `GoogleTestVerification.UninstantiatedParameterizedTestSuite<ReplayTests>`：没有下载 replays，参数化测试没有实例。
  - 补充：把 `build/data` 软链到仓库的 `data/` 后，language 问题消失，但这些测试和寻路测试又因为 `Object not found`（`DOWNLOAD_OBJECTS=OFF`）失败。所以这一类测试在本环境里跑不了，需要 CI（会下载 objects/replays）来覆盖。
  - 没有任何测试直接引用被改名的常量（`grep` test/ 无结果）。改名只换了符号名，编译产物应当完全一样。
- **构建时遇到的、与本改动无关的上游问题**：`src/openrct2/network/NetworkServerAdvertiser.cpp` 用了 `std::shared_future`，但没有 `#include <future>`。在 GCC 13 + `-DDISABLE_HTTP=ON` 下编译失败（CI 的编译器或依赖大概会间接带进这个头文件）。为了验证，本地**临时**加了 `#include <future>`，构建完已经还原，**没有放进 patch**。以后可以考虑单独提一个小 PR。

- `src/openrct2-ui/windows/News.cpp` 不在 headless 构建里，所以单独用 libopenrct2 的完整编译命令（`ninja -t commands` 取得）加 `-fsyntax-only` 编译了一次：通过（rc=0）。
- scripting 是开启的（`ENABLE_SCRIPTING=ON`），所以 ScPark.cpp / ScParkMessage.cpp 在构建里编译过。
- 注意：对整个文件跑本地 clang-format 18 会改动很多无关代码（CI 用的版本不同），所以只用 `clang-format-diff` 检查了改动行。

## 需要提交者注意
- AI 政策：仓库没有禁止 AI 的规定，只在 PR 模板里要求如实回答 "Did you use AI…"；pr_body.md 已回答 Yes 并简要说明。提交前请自己读一遍 diff，维护者问起时能解释改动。
- 不需要先认领/被 assign：这是 tracking issue，大家直接按文件开 PR。
- 提交前再确认一次 upstream 没有别人已改这两个文件（`curl -s https://raw.githubusercontent.com/OpenRCT2/OpenRCT2/develop/src/openrct2/world/Entrance.h | grep EntranceHeight`）；如果 develop 有新提交导致冲突，rebase 后重新 grep 旧名字。
- 另有一个同名但不相关的常量 `RideMeasurement::kMaxItems`（Ride.h，类作用域）已存在，与 `News::kMaxItems` 作用域不同，不冲突。
- CONTRIBUTING 没有 DCO 或 trailer 要求，提交里没有 Signed-off-by。
- "code style" 标签由维护者加，不用自己加。
- 正文写的是 "Part of #21432"，不会自动关闭这个 tracking issue。

## 如何提交
```bash
git clone https://github.com/OpenRCT2/OpenRCT2 && cd OpenRCT2
git checkout -b refactor-entrance-news-constants origin/develop
git am /home/user/Playground/contributions/815-OpenRCT2-OpenRCT2-21432/0001-Refactor-constant-notation-in-Entrance.h-and-NewsIte.patch
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/815-OpenRCT2-OpenRCT2-21432 OpenRCT2/OpenRCT2 develop refactor-entrance-news-constants contributions/815-OpenRCT2-OpenRCT2-21432/pr_title.txt contributions/815-OpenRCT2-OpenRCT2-21432/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
