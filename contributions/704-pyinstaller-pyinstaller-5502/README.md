# pyinstaller/pyinstaller #5502 — Use script name instead of project name for xref and dot files

| 项 | 值 |
|---|---|
| Issue | https://github.com/pyinstaller/pyinstaller/issues/5502 |
| Tier | 高星 |
| Labels | Feature request, Pull-request wanted |
| Status | ✅ ready — patch + PR 文本已就绪 |
| 重复 PR 检查 | 2026-10-01：issue 仍为 open，没有 assignee，也没有评论。issue 页面 Development 栏没有关联 PR。`pulls?q=5502` 只搜到无关的 #4411；按 "xref" 搜索只有早已合并的无关 PR（#2847 等）。没有 open 或 merged 的重复 PR。 |
| Base | `develop` @ cea3915d（2026-09-29） |

## 问题理解
`build/<spec>/xref-<spec>.html` 和 `graph-<spec>.dot` 按 spec 名命名（`build_main.build()` 里设置的 `CONF['xref-file']` / `CONF['dot-file']`）。一个 spec 里有多个 `Analysis`（例如用 MERGE 打多个程序）时，每个 Analysis 都写同一对文件，最后只剩最后一个的结果。issue 提议改为按脚本名命名：`xref-<script>.html`。

## 合理性判断
- 维护者打了 "Pull-request wanted"，方案就是 issue 里提的那个，不需要先讨论设计。
- develop 上仍是旧行为（已核对源码），没有被修复过。
- 兼容性：默认情况下 spec 名就是脚本名（`pyinstaller foo.py` → `foo.spec`），所以文件名不变。只有用了 `--name` 或多 Analysis 的 spec 才会变。这两个文件只是调试输出，不属于 API。

## 改动
- `PyInstaller/building/build_main.py`：`_write_graph_debug()` 用 `self.inputs[0]` 的文件名（去掉扩展名）拼出 `xref-<script>.html` / `graph-<script>.dot`，放在 `CONF['workpath']` 下。删除不再使用的 `CONF['xref-file']` / `CONF['dot-file']`。
- `tests/functional/test_regression.py`：新增 `test_issue_5502`，在同一个 workpath 里跑两个 Analysis，开 DEBUG 日志，断言两套 xref/dot 文件都存在且内容不同。两个旧测试的假 CONF 里去掉了已删除的 key。
- `doc/when-things-go-wrong.rst`：更新文件名说明。
- `news/5502.feature.rst`：towncrier 片段。
- 提交信息遵循仓库规范：首行带子系统前缀（`building:`），以句号结尾。
- 没有改 `warn-<spec>.txt`：issue 只提到 xref/dot，而且 warnfile 还通过 WARNFILE 传给了 bootloader。PR 正文已说明。

## 验证（Linux，Python 3.11，venv 内装 altgraph/packaging/pyinstaller-hooks-contrib/setuptools/pytest，PYTHONPATH 指向源码树）
- Red：还原 build_main.py 后跑 `python -m pytest tests/functional/test_regression.py -k 5502`。直接跑时因缺少 `xref-file` 报 KeyError。在假 CONF 里补上旧 key 再跑，断言失败：`xref-script_a.html` 不存在（被写成了 `xref-issue_5502.html` 并被覆盖）。
- Green：同一命令 1 passed。
- `python -m pytest -n 2 tests/functional/test_multipackage.py tests/functional/test_regression.py`：13 passed。这些测试会构建 MERGE 多包程序，需要用 waf 本地编译 Linux bootloader。编译只是为了跑测试，生成物已还原，不在 patch 里。
- `python -m pytest -n 2 tests/unit`：324 passed，22 skipped，11 xfailed，1 failed（`test_pyimodulegraph.py::test_metadata_searching`，PackageNotFoundError，原因是没有 pip install 本包）。这个测试在 develop 上同样失败，与本改动无关。
- 手动复现 issue：两个 Analysis + MERGE 的 spec，`--log-level DEBUG`，build 目录下生成了 xref-a.html、xref-b.html、graph-a.dot、graph-b.dot。
- `yapf --recursive --parallel --diff .`（yapf 0.43.0，无 diff），`flake8 .`（干净）。
- **没有运行**：完整的 functional 测试集（很大，CI 上是多平台矩阵）。

## 需要提交者注意
- 仓库没有 AI 政策（CONTRIBUTING 指向开发文档；.github、doc/development、labels 页面都查过），不需要 DCO，也没有 PR 模板。
- news 片段用的是 issue 号 5502。仓库 README 写的是 `<pr#>.<type>.rst`，提交后可按 PR 号重命名，或保留 issue 号（文档也允许复制片段以关联多个编号）。
- 文件名对 `--name` 用户会变（例如 `xref-MyApp.html` 变成 `xref-main.html`），归为 feature。如果维护者认为属于 breaking，可以把片段改成 `.breaking.rst`。
- 两个 Analysis 用了同名脚本（不同目录）时仍会互相覆盖，属于边缘情况，暂未处理。

## 如何提交
```bash
git clone https://github.com/pyinstaller/pyinstaller && cd pyinstaller
git checkout -b building/xref-per-script origin/develop
git am /home/user/Playground/contributions/704-pyinstaller-pyinstaller-5502/0001-building-Name-xref-and-dot-files-after-the-analyzed-.patch
python -m pytest tests/functional/test_regression.py && yapf -rd . && flake8 .
```
或者直接运行：
```bash
tools/submit_pr.sh contributions/704-pyinstaller-pyinstaller-5502 pyinstaller/pyinstaller develop building/xref-per-script contributions/704-pyinstaller-pyinstaller-5502/pr_title.txt contributions/704-pyinstaller-pyinstaller-5502/pr_body.md
```

## PR
- Title：见 `pr_title.txt`
- Body：见 `pr_body.md`
