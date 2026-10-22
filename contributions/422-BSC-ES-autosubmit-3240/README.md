# 422 — BSC-ES/autosubmit#3240: Log.set_file 建目录逻辑

| 项 | 内容 |
|---|---|
| Issue | https://github.com/BSC-ES/autosubmit/issues/3240 |
| 层级 | 自由（BSC 地球科学部的工作流管理器，非常活跃，接受外部贡献并在 CHANGELOG 致谢） |
| Labels | bug, enhancement, good first issue；milestone 4.2.2；维护者 dbeltrankyl 开 |
| Base 分支 | `master`（补丁基于 5919cd9） |
| 状态 | ✅ 可提交 |
| 重复检查 | 2026-10-22：issue 无评论、无指派、无关联 PR；43 个开着的 PR 里无相关（#3357 是日志恢复进程，不同） |
| AI 政策 | CONTRIBUTING 无 AI 条款 |
| CLA/DCO | 无 |

## 问题理解
FIXME 认为“建了目录但 FileHandler 要求文件已存在所以会失败”——这一点其实不成立：`FileHandler(path,'w')` 会自己创建文件，单层缺目录时现有代码能工作。真正的缺陷是 `os.mkdir` 不递归：父目录也缺时，以及纯文件名（目录部分为 `''`）时，每次重试都失败，最后 sleep 15 秒后抛 AutosubmitCritical。

## 改动
`os.makedirs(directory or os.curdir, exist_ok=True)`；FIXME 换成解释性注释；新增测试 + CHANGELOG（4.2.0 未发布，VERSION=4.2.0、无 4.2 tag）。

## 验证
- 红：不带修复，新增 9 个用例中 5 个失败（嵌套缺目录 ×4 类型 + 纯文件名），单层缺目录 4 个通过（证明 FIXME 的判断不对，PR 正文已说明）。
- 绿：`pytest test/unit/log` 82 passed。
- 全量 `USER=root pytest test/unit -n 4`：2563 passed，4 failed；这 4 个在 base 上同样失败（无 psycopg、root 运行、PATH 无 autosubmit），与改动无关。
- `ruff check` 改动文件通过（CI 只对改动文件跑 ruff）。

## 需要提交者注意
- PR 正文已按仓库模板 Check List 填写。
- 测试需要环境变量 USER（cloud 环境缺省没有）。

## 如何提交
```
git clone https://github.com/BSC-ES/autosubmit && cd autosubmit && git checkout -b fix-log-set-file-dirs origin/master
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
- 全新浅克隆 BSC-ES/autosubmit（origin/master = 5919cd9），`git am` 补丁干净应用。
- 代码审查：`os.makedirs(directory or os.curdir, exist_ok=True)` 正确；`exist_ok=True` 下 directory 已存在不受影响，已存在为普通文件时照旧失败并走重试（与旧行为一致）。纯文件名时 file_path 变成 `./20100309_x.log`（out/err）或 `./x.log`（status/status_failed），而 `FileHandler` 内部做 `os.path.abspath`，实测 `FileHandler('./x.log')` 的 baseFilename 就是 `<cwd>/x.log`，与 `x.log` 等价；旧代码在这种情况下必然失败，所以没有回归。仓库内调用方（log/__init__.py、platforms/platform.py）都传完整路径，不受影响。重试时 file_path 被重赋值导致日期前缀叠加属既有问题，本补丁未改变。
- 核实 FIXME 的判断不成立：`FileHandler(path,'w')` 自己创建文件；基线代码下 `missing_dir` 4 个用例通过。
- 红→绿（USER=root，uv venv py3.12）：仅把 log.py 回退到 HEAD~1，`-k "creates_missing or bare_file"` 得 5 failed / 4 passed（missing_parent_dirs ×4 + bare_file_name 失败）；恢复后 `pytest test/unit/log` 82 passed。`ruff check` 改动的两个文件：All checks passed。
- 全量 `pytest test/unit -n 4`：2563 passed、4 failed（test_session postgresql、test_check_ownership ×2、test_version broken）；同样 4 个在 base（HEAD~1）上也失败，与补丁无关。数字与 PR 正文一致。
- 竞争检查：pulls?q=3240 0 结果；pulls?q=set_file 只有 #2618（已合并，即 issue 里提到的旧 quickfix）和 #2365（已关闭）。issue 仍 open、无评论、无指派、Development 无关联分支/PR。
- PR 文案：英文，前两行是 attribution 块，含 `Closes #3240`、Motivation/disclosure 段，Check List 与 `.github/PULL_REQUEST_TEMPLATE.md` 八项逐条对应；“5 s + 10 s” 与 `sleep(timeout * retries)` 相符。
- CHANGELOG：放在顶部 `### 4.2.0` 的 **Bug fixes** 末尾，VERSION=4.2.0 且远端无 4.2.x tag，位置合理。可选：外部贡献者条目常带 `(thanks @user)`，可自行加或留给维护者，不影响提交。
- 已删除 /home/user/work/review422。

结论：PASS
