# pasteurlabs/tesseract-core #768 — Client-facing API to query supported device (GPU) transports

| 项 | 值 |
|---|---|
| Issue | https://github.com/pasteurlabs/tesseract-core/issues/768 |
| Tier | 新锐 |
| Labels | good first issue |
| Status | 🚧 in progress — implemented, patch exported, full fast suite running |
| 重复 PR 检查 | 2026-09-24: issue 无 assignee、0 comments、无 linked branch/PR；PR 搜索 `transport repo:pasteurlabs/tesseract-core` 仅见已合并的 #737/#781 和无关的 open #726 (cuda_vmm) / #723 (NIXL) / #748 (Ref)，无人实现本 issue |

## 为什么是 新锐

- **Stars / 年龄**：~134 stars，仓库创建于 2025-02（约 1.5 年），典型的上升期项目。
- **贡献者**：最近 50 个 commit 中有 10 位不同作者（Dion Häfner、Harsh Singh、Jonathan Brodrick、julienkloers、Shivansh Shukla、Afonso Januário 等），外部贡献者 PR 在 1–2 天内被合并（例如今天合并的 #789）。
- **活跃度**：本周（09-18 至 09-24）每天都有 commit，维护者 Dion Häfner 亲自开 issue 并打 good-first-issue 标签。
- **价值**：Pasteur Labs 出品的可微分科学计算组件框架（把模型/仿真打包成带 Jacobian/VJP 等端点的容器），有 tesseract-jax、tesseract-torch 等下游包装库；本 issue 正是为了让这些下游库摆脱对私有属性的依赖。
- 非 issue farm、非单作者仓库；Apache-2.0，有 CLA。

## 需要提交者注意

- 仓库有 `AGENTS.md` / `CLAUDE.md`（面向 AI agent 的规则），即明确接受 AI 辅助贡献；未发现禁止 AI 或拒绝大规模贡献者的条款。
- **需要签署 CLA**（https://github.com/pasteurlabs/pasteur-oss-cla），CLA bot 会在 PR 上提示。
- PR 标题须符合 Conventional Commits（squash merge，标题即 commit 标题）：`feat(sdk): expose Tesseract.supported_device_transports`。
- **不要改 `CHANGELOG.md`**（发布时由 PR 标题自动生成）。
- PR 模板字段：`#### Relevant issue or PR` / `#### Description of changes` / `#### Testing done`，下面的 PR body 已按此模板组织并附上 disclosure 段落。
- 原先挑的 #788 已被 #789 于今天修复，所以改选 #768（同一项目）。

## 问题理解

下游包装库（tesseract-torch#42、tesseract-jax#239）需要知道：
1. 这个 client 能否使用 device transport（目前靠 `hasattr(client, "_gpu_transport")` 区分 `HTTPClient` 与 `LocalClient`）；
2. 哪些 transport 名字可用（目前硬编码 / 从 runtime 的 `Literal` 推导）。

issue 要求提供一个公开的 per-client 访问器，例如 `Tesseract.supported_device_transports`：
- `from_image(..., gpu_transport="cuda_ipc")` → `("cuda_ipc",)`
- `from_tesseract_api(...)` → `()`

## 合理性判断

由维护者本人（dionhaefner）提出并标记 good first issue；新增一个只读属性，无破坏性，符合 AGENTS.md "follow existing patterns"（参照 `available_endpoints` 属性 + `requires_client` 装饰器）。

## 改动

`tesseract_core/sdk/tesseract.py`：
- `HTTPClient.supported_device_transports`：返回其配置的 `gpu_transport`（`"none"` 时为空 tuple）。
- `LocalClient.supported_device_transports`：恒为 `()`（进程内共享内存，无需传输）。
- `Tesseract.supported_device_transports`：`@property @requires_client`，委托给 client；未 serve 的 `from_image` 对象会像其它方法一样抛出 "use it as a context manager or call .serve()" 的 RuntimeError。

`tests/sdk_tests/test_tesseract.py`：
- `test_supported_device_transports_served`（参数化 4 例：默认、显式 `none`、kwarg `cuda_ipc`、`runtime_config` 中的 `cuda_ipc`；使用已有的 `mock_serving` fixture，并验证未 serve 时报错）。
- `test_supported_device_transports_unserved`：`from_url` → `()`；`from_tesseract_api(..., gpu_transport="cuda_ipc")` → `()`。

范围说明：服务端在 OpenAPI 中广播 transport（issue 中 "ideally, negotiate against what the served Tesseract genuinely supports"）未做，理由写在 PR 描述里（#732 的 review 曾要求先只做服务端 / 不急于固定 client API；本 PR 反过来只做 issue 核心诉求的 client 端属性，保持小而清晰）。

## 验证

环境：`uv venv .venv -p 3.11 && uv pip install -e ".[dev]"`（无 Docker、无 GPU）。

- Red（仅应用测试、未改源码）：
  `pytest -q --skip-endtoend tests/sdk_tests/test_tesseract.py -k supported_device_transports`
  → `5 failed` (`AttributeError: 'Tesseract' object has no attribute 'supported_device_transports'`)
- Green（应用补丁后）：同命令 → `5 passed`
- `tests/sdk_tests/test_tesseract.py` 全文件：基线 `65 passed`；补丁后见下
- 全部快速测试 `pytest --skip-endtoend tests`：见下
- Lint：`uvx ruff@0.15.22 check tesseract_core tests` → All checks passed；`ruff format --check` → 94 files already formatted（与 pre-commit 中 ruff 版本一致；prettier 钩子只涉及 json/yaml/md/toml，本改动未触及）

## 如何提交

```bash
git clone https://github.com/<you>/tesseract-core && cd tesseract-core
git checkout -b feat/supported-device-transports origin/main   # base: main @ a8d7801
git am /path/to/0001-feat-sdk-expose-Tesseract.supported_device_transport.patch
git push -u origin feat/supported-device-transports
```
然后开 PR，标题与 body 如下；签 CLA。

## PR title

```
feat(sdk): expose `Tesseract.supported_device_transports`
```

## PR body

```markdown
#### Relevant issue or PR

Closes #768

#### Description of changes

Adds a public, per-client way to ask which device (GPU) transports a Tesseract uses, so wrapper libraries (tesseract-torch, tesseract-jax) no longer need to duck-type the private `_gpu_transport` attribute or hardcode transport names.

- `Tesseract.supported_device_transports` (property, follows the `available_endpoints` pattern incl. `requires_client`) delegates to the client.
- `HTTPClient.supported_device_transports` returns its configured `gpu_transport`, or `()` for `"none"`. For a Tesseract served via `from_image`/`from_source` this is the transport mirrored from the served container (kwarg > `runtime_config` > `"none"`), so it reflects what that Tesseract was actually started with.
- `LocalClient.supported_device_transports` is always `()`: in-process Tesseracts share memory with the caller, so there is nothing to transport (even if a `gpu_transport` is set in its config).

```python
tess = Tesseract.from_image("mytesseract", gpus=["all"], gpu_transport="cuda_ipc")
with tess:
    tess.supported_device_transports   # ("cuda_ipc",)

Tesseract.from_tesseract_api("...").supported_device_transports  # ()
```

Scope note: this is client-side only. For `from_url` the client can't know the server's transport and reports `()`; advertising the server's transports (e.g. alongside `x-supported-output-formats` in the OpenAPI schema) and negotiating against it could be a follow-up if you'd like — happy to adjust the shape of this API (e.g. a tuple vs. a frozenset, or a different name) if you had something else in mind.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

#### Testing done

- New tests in `tests/sdk_tests/test_tesseract.py`: `test_supported_device_transports_served` (default / `none` / `cuda_ipc` kwarg / `cuda_ipc` via `runtime_config`, plus the unserved error) and `test_supported_device_transports_unserved` (`from_url`, `from_tesseract_api` with `gpu_transport="cuda_ipc"`). They fail on `main` with `AttributeError` (5 failed) and pass with this change (5 passed).
- `pytest --skip-endtoend tests`: FULL_SUITE_RESULT
- `ruff check` / `ruff format --check` (v0.15.22, as pinned in pre-commit): clean.
- `CHANGELOG.md` not touched (auto-generated). No docs page covers GPU transports yet; the property is documented via its docstring.
- End-to-end (Docker) and GPU tests not run locally (no Docker/GPU here); the change doesn't touch the serving or transport paths.
```
