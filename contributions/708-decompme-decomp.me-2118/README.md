# decompme/decomp.me #2118 — download.py fails to consider errors failures

| 项 | 值 |
|---|---|
| Issue | https://github.com/decompme/decomp.me/issues/2118 |
| Tier | 自由 |
| Labels | bug, good first issue |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：`pulls?q=2118` 没有结果；按 "download" 搜索也没有相关的 open PR（唯一的 open PR 是 #2042 cromper，与此无关）。issue 无人分配，没有评论。 |
| Base | `main` @ 4ab701a（2026-09-27） |

## 问题理解
维护者 ethteck 于 2026-09-30 开的 issue。CI 运行 `backend/compilers/download.py` 时有一个下载抛出 `RemoteDisconnected`，最后却打印 `Updated 213 / 213 compiler(s)`，并以 0 退出。
根因：`DownloadThread.run` 捕获异常后只打日志，没有往 results 队列放任何东西，所以失败项从分子和分母里一起消失了（实际总数应为 214）。`main()` 也从来不返回非零值。

## 合理性判断
- 维护者本人开的 bug，带 good first issue 标签，期望行为写得很明确：失败不计入成功数，有失败时以非零退出。
- 仓库没有 AI 政策（README、.github、labels 页都查过；没有 CONTRIBUTING / AGENTS.md），不要求 DCO，没有 PR 模板，也没有 CHANGELOG。
- default branch 上还没有修复。

## 改动（`backend/compilers/download.py`）
- results 改为 `(item, result)` 二元组；遇到异常时记为 `(item, False)`。
- 镜像在 registry 中存在、但获取 index 或 manifest 返回非 200 时，原来 `return None`（被当作"无需更新"），现在打 error 日志并 `return False`。
- 汇总只统计 `result is True`。有失败时打印 `N compiler(s) failed to download: platform/compiler, ...`，`main()` 返回 1；入口改为 `sys.exit(main())`。
- 新增测试 `backend/coreapp/tests/test_compiler_download.py`（SimpleTestCase，用 importlib 加载脚本，mock `get_compiler_raw` 和 `platform.system`，不联网）。
- **没有改** "not found in registry" 的情况（仍返回 None，不算失败），PR 正文里已说明原因并表示可以按维护者意见再改。

## 验证（uv，Python 3.13 venv，`uv sync --locked`）
- Red（只还原 download.py）：`uv run python manage.py test coreapp.tests.test_compiler_download` → 2 个测试都失败（`None != 1`，`None != 0`）。
- Green：同一命令 → `Ran 2 tests ... OK`。
- `uv run ruff check .` → All checks passed；`uv run ruff format --check .` → 138 files already formatted；`uv run mypy` → Success。
- 全量 `uv run python manage.py test`：143 个测试，20 个失败（`test_platform` 的 roundtrip 和 `test_compiler_endpoint`），原因是本机没有下载编译器和 binutils（CI 在 docker 里先下载）。base 上同样是这 20 个失败（141 个测试），新增的 2 个测试通过。
- 没有运行：CI 里的 docker 构建、docker compose 测试，以及前端 biome/yarn 测试（与本改动无关）。

## 需要提交者注意
- 无 AI 政策限制，无 DCO，无 PR 模板，无 CHANGELOG。
- 提交信息沿用仓库风格（句子式标题，合并时由 GitHub 追加 `(#PR)`）。
- 行为变化：CI 中 `compilers/download.py` 只要有下载失败就会让 job 失败。这正是 issue 想要的，但 CI 可能因此更容易暴露网络抖动。

## 独立复核（2026-10-01）
- 在 upstream `main` @ 4ab701a 的全新浅克隆上 `git am` 干净应用；作者为 anyingiit，提交信息无 AI 模型名。
- Red/Green 已独立复现：只还原 `download.py` → 2 个失败（`None != 1`、`None != 0`）；恢复 → OK。ruff / ruff format / mypy 均干净；全量测试 143 个、20 个失败（均为 `test_compiler_endpoint` / `test_platform` roundtrip，缺编译器/binutils 所致）。
- 检查过：`docker_entrypoint.sh` 没有 `set -e`，退出码变化不会阻止容器启动；CI 中 `&&` 链会在下载失败时停下，符合 issue 的要求。`libraries/download.py` 用 `pool.starmap`，异常会直接抛出，不在本 issue 范围内。
- issue 仍 open、无人分配、无评论；`pulls?q=2118` 无结果。未发现需要修改的问题。

## 如何提交
```bash
git clone https://github.com/decompme/decomp.me && cd decomp.me
git checkout -b fix/compiler-download-failures origin/main
git am /home/user/Playground/contributions/708-decompme-decomp.me-2118/0001-Report-failed-compiler-downloads-and-exit-non-zero.patch
cd backend && uv sync --locked && uv run python manage.py test coreapp.tests.test_compiler_download && uv run ruff check . && uv run mypy
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/708-decompme-decomp.me-2118 decompme/decomp.me main fix/compiler-download-failures contributions/708-decompme-decomp.me-2118/pr_title.txt contributions/708-decompme-decomp.me-2118/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
