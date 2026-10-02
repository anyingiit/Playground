# protocolbuffers/protobuf #30162 — protobuf_generate() ignores --proto_path passed through PROTOC_OPTIONS

| 项 | 值 |
|---|---|
| Issue | https://github.com/protocolbuffers/protobuf/issues/30162 |
| Tier | 高星 |
| Labels | cmake, documentation, help wanted |
| Status | ✅ ready — 仅文档改动（审核去掉了会误报的 AUTHOR_WARNING）；提交者需先签 Google CLA |
| 重复 PR 检查 | 2026-10-01：issue 开放、无人分配、无评论、无关联 PR。`pulls?q=30162` 返回 0 条。搜 `protobuf_generate` 只有 #30159 是 open（给 COMMENT 加引号，与本 issue 无关）。搜 `proto_path cmake` 没有相关的 open PR（#15929 prepend path 已于 2024 年关闭）。anyingiit 在该仓库没有 PR。 |
| Base | `main` @ 1d2f6fa4（2026-10-01） |

## 问题理解
`protobuf_generate()` 只用 `IMPORT_DIRS` / `APPEND_PATH`（都没给时用 `CMAKE_CURRENT_SOURCE_DIR`）计算每个 proto 的相对目录 `_rel_dir`，再据此推出 `add_custom_command` 的 OUTPUT。通过 `PROTOC_OPTIONS` 传入的 `--proto_path` / `-I` 会原样转给 protoc，而且排在命令行最前面，但 CMake 计算路径时完全不看它。结果分两种：
- proto 不在任何已知 include 目录下：configure 阶段报 "could not find any correct proto include directory"；
- proto 在 `CMAKE_CURRENT_SOURCE_DIR` 下：CMake 期望生成 `<bin>/proto/foo/a_pb2.py`，protoc 实际写到 `<bin>/foo/a_pb2.py`。OUTPUT 永远不存在，所以每次构建都会重新生成（已用真实 protoc 复现）。

## 合理性判断
- 维护者打了 `documentation` + `help wanted` 标签。issue 给出的第二个方案（文档说明 import root 必须走 IMPORT_DIRS）就是最小且明确想要的改动。
- 解析 PROTOC_OPTIONS 属于行为变更。CONTRIBUTING 要求这类改动先得到维护者支持，所以没做，只在 PR 里提出可以后续跟进。
- 实现者原本加了一个 `AUTHOR_WARNING`（PROTOC_OPTIONS 中出现 `-I`/`--proto_path` 就警告）。**审核时已去掉**：用真实 protoc 验证，`IMPORT_DIRS proto` + `PROTOC_OPTIONS -Idep`（只放被 import 的目录）完全正常、二次构建 no work to do，但警告照样触发，属于误报；开了 `-Werror=dev` 的项目还会直接 configure 失败。issue 标签是 `documentation`，因此最终只改文档。
- CONTRIBUTING 写着"文档改动提交到 protocolbuffers.github.io"，但 `docs/cmake_protobuf_generate.md` 在本仓库里，PR #25641 也直接改过它；加上这次还有代码改动，所以在本仓库提 PR 是合理的。

## 改动
- 只改 `docs/cmake_protobuf_generate.md`：
  - `PROTOC_OPTIONS` 条目：不要在这里传 `PROTOS` 所在的 import 目录（`--proto_path`/`-I`），说明两种后果（configure 报错 / 每次构建都重新生成），改用 `IMPORT_DIRS` / `APPEND_PATH`。措辞限定为"PROTOS 的 import 目录"，因为只放被 import 文件的目录通过 PROTOC_OPTIONS 传是能正常工作的。
  - `IMPORT_DIRS` 条目：补充每个目录都会以 `-I` 传给 protoc，所以只含被 import 文件的目录也可以放这里。
- 单个 commit，作者 anyingiit，句子式标题，末尾 `Fixes #30162`。

## 验证（CMake 3.28.3）
纯文档改动，没有可做 red→green 的单元测试；用真实 protoc 验证文档描述属实。独立小工程 `p/`：`proto/foo/a.proto` import `dep/bar/b.proto`；`include(<protobuf>/cmake/protobuf-generate.cmake)` 后
`protobuf_generate(PROTOS .../proto/foo/a.proto LANGUAGE python OUT_VAR gen PROTOC_EXE ${PROTOC} ${_a})` + `add_custom_target(g ALL DEPENDS ${gen})`，PROTOC 为 `python -m grpc_tools.protoc` 的包装（`uv pip install grpcio-tools`，libprotoc 35.1）。对每个 CASE：`cmake -S p -B b-$c -G Ninja ...; ninja -C b-$c; ninja -C b-$c`：
- `bad`：`PROTOC_OPTIONS --proto_path=<p>/proto -I<p>/dep` → 第二次 ninja 仍重跑 protoc（复现 issue）。
- `importdirs`：`IMPORT_DIRS <p>/proto <p>/dep`（文档推荐）→ `ninja: no work to do.`
- `importonly`：`IMPORT_DIRS <p>/proto` + `PROTOC_OPTIONS -I<p>/dep` → `ninja: no work to do.`（据此把文档措辞限定为 PROTOS 的 import 目录，也是去掉警告的原因）。
- `git apply --check` 到干净的 `main`@1d2f6fa4：通过。新增行均 ≤80 列；仓库对 Markdown 无 lint 配置。
- 未运行：完整构建 protobuf 及单元测试（文档改动，不影响构建）。

## 需要提交者注意
- **必须先签 Google 个人 CLA**：https://cla.developers.google.com/ ，否则 PR 会被 CLA bot 拦住。
- 仓库没有 AI 相关规定，不需要 DCO，没有 changelog fragment，也没有 PR 模板。PR 会经 copybara 导入，保持单个 commit 即可。
- PR 正文写的是 `Fixes #30162`。只做了文档；解析 PROTOC_OPTIONS 留作可选的后续工作，PR 里已说明。

## 如何提交
```bash
git clone https://github.com/protocolbuffers/protobuf && cd protobuf
git checkout -b cmake-protoc-options-proto-path origin/main
git am /home/user/Playground/contributions/101-protocolbuffers-protobuf-30162/0001-Document-that-protobuf_generate-import-dirs-belong-i.patch
git push <你的 fork> cmake-protoc-options-proto-path
gh pr create --repo protocolbuffers/protobuf --head anyingiit:cmake-protoc-options-proto-path \
  --title "$(cat contributions/101-protocolbuffers-protobuf-30162/pr_title.txt)" \
  --body-file contributions/101-protocolbuffers-protobuf-30162/pr_body.md
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/101-protocolbuffers-protobuf-30162 protocolbuffers/protobuf main cmake-protoc-options-proto-path contributions/101-protocolbuffers-protobuf-30162/pr_title.txt contributions/101-protocolbuffers-protobuf-30162/pr_body.md
```
审核后工作克隆已删除；patch 基于 `main` @ 1d2f6fa4。

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
