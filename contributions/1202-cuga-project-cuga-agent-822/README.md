# cuga-project/cuga-agent#822: mcp-text 递归切块丢分隔符

| 项 | 值 |
|---|---|
| Issue | https://github.com/cuga-project/cuga-agent/issues/822 |
| **实际修改仓库** | **https://github.com/cuga-project/cuga-apps**（代码不在 cuga-agent，见下文） |
| Tier | 新锐 |
| Labels | good first issue |
| Status | ✅ ready：独立复核通过，patch 和 PR 文本可直接提交（尚未提交） |
| Base | cuga-apps `main` @ `51b087ee7a34` (2026-06-25, "add star")，2026-10-01 23:14 UTC `git ls-remote` 确认未变 |
| Duplicate-PR check | 2026-10-01 23:10 UTC 检查：issue 状态 open，0 评论，无 assignee，Development 区无关联 PR/分支。cuga-agent `pulls?q=822` 无结果；`chunk` 和 `separator OR mcp-text` 关键词搜索均无相关 PR。cuga-apps 的 PR 列表（22 open + 5 closed，大多是 10-01 当天新开的）里没有改 `_chunk_recursive` 的。#23（lakshmip03，"reject overlap >= size in chunk_text"）改的是同一文件里的 `chunk_text` 入口校验，不是同一 bug，详见“需要提交者注意”。 |

## 问题理解

`text` MCP server 的 `chunk_text(strategy="recursive")` 调用 `_chunk_recursive`。这个函数按分隔符 `split` 后，给每段补回分隔符时用的是 `part is not parts[-1]`，也就是按对象身份判断“是不是最后一段”。CPython 会缓存单字符字符串和空字符串，所以如果首段和末段内容相同，且是单字符或空串，它们就是同一个对象，首段会被当成末段，分隔符就丢了。结果是切出来的块拼不回原文。

- Issue 里的复现：`'a\n\nbbbbb\n\na'`（size=6, overlap=0）得到 `['a', 'bbbbb\n\n', 'a']`，`join` 后不等于原文。
- 我额外发现一个更常见的情形：文本以分隔符开头并以分隔符结尾，比如 `'\n\nbbbbbbbb\n\n'`。首尾两段都是 `''`，修复前结果是 `['bbbbbbbb\n']`，丢了 3 个字符。
- 修复方案就是 issue 里给的：改成用 `enumerate` 的下标判断。

注意：issue 写的路径是 `cuga-apps/mcp_servers/text/server.py`。这个路径在 cuga-agent 仓库**不存在**（clone 后 grep `_chunk_recursive` 没有结果，github.com 上对应 blob 返回 404），实际在同一组织下的独立仓库 **cuga-project/cuga-apps** 中，仓库根目录下有一层 `cuga-apps/` 子目录，路径完全对得上。issue 作者 anupamamurthi 是 cuga-agent 的维护者（合并过 #602），也是 cuga-apps 仅有的两个已合并 PR（#3、#4）的作者。所以这个 issue 是统一记在 cuga-agent 跟踪器里的。最近一天 cuga-apps 收到二十来个外部 PR（例如 #23 也是修 mcp-text 的），说明外部贡献者正是按这种方式去 cuga-apps 提 PR。

## 合理性判断

- 维护者亲自开的 issue，带 `good first issue` 标签。cuga-agent 的 CONTRIBUTING 规定外部贡献者可以直接做 `good first issue`，不需要事先批准。
- Bug 真实存在：在 cuga-apps main 上复现了，结果与 issue 描述完全一致。
- AI 政策：cuga-agent 有 AGENTS.md、CLAUDE.md、`.claude/skills`，CONTRIBUTING 里有 “AI Agent Skills” 一节，对 AI 持欢迎态度。cuga-apps 的 CONTRIBUTING 没有提到 AI。label 描述中没有“仅限人类”之类的限制。（cuga-agent 有一个 `ai-spam` 标签，用来标“Suspected spam or low-quality contribution”，所以 PR 必须小而准确。）

## 改动

- `cuga-apps/mcp_servers/text/server.py`：`for part in parts:` 改为 `for i, part in enumerate(parts):`，`part is not parts[-1]` 改为 `i < len(parts) - 1`，与 issue 给出的写法一致（共 2 行）。
- `cuga-apps/tests/test_mcp_tools.py`：在 `TestMcpText` 中新增 `test_chunk_text_recursive_keeps_separators`。写法与已有的 chunk 测试一致，通过 MCP 调用工具，覆盖上面两个输入，断言拼接结果等于原文。仓库的测试全部是连真实服务的集成测试，没有纯单元测试目录，所以按现有风格写。

## 验证

环境：在 `/home/user/work/cuga-apps-822` 里用 `uv venv .venv -p 3.11`，然后 `uv pip install "mcp>=1.0,<2" "pytest>=7" httpx`，装到的 mcp 版本是 1.30.0。mcp 限定 `<2`，与 #5 中 pin 的范围一致。docling、tiktoken 没装，它们只在 count_tokens/extract_text 里惰性 import，这次不测。

仓库 conftest 在 `localhost:3001`（UI）没有监听时会跳过全部测试。所以验证脚本（`run_red_green.sh`，逻辑如下）的做法是：在 29106 端口只启动 mcp-text，再用 python 在 3001 上开一个空的 socket 监听，然后跑 chunk 相关的测试：

```bash
cd cuga-apps
MCP_BIND_HOST=127.0.0.1 ../.venv/bin/python mcp_servers/text/server.py &          # mcp-text on 29106
../.venv/bin/python -c "import socket,time;s=socket.socket();s.bind(('127.0.0.1',3001));s.listen();time.sleep(120)" &
CUGA_TEST_HOST=127.0.0.1 ../.venv/bin/python -m pytest tests/test_mcp_tools.py -k "TestMcpText and chunk"
```

| 步骤 | 结果 |
|---|---|
| issue 复现命令（未修复） | `['a', 'bbbbb\n\n', 'a'] False` |
| 保留新测试，把 server.py 回退到 main 版本 | **1 failed**, 4 passed：`['a', 'bbbbb\n\n', 'a'] != ['a\n\n', 'bbbbb\n\n', 'a']` → red |
| 加上修复 | **5 passed** → green |
| issue 复现命令（修复后） | `['a\n\n', 'bbbbb\n\n', 'a'] True` |
| 随机测试：20,000 条由 `a b \n\n \n ". " " "` 组成的文本，size 1–12，overlap=0 | 修复前 10,618 条拼不回原文，修复后 0 条 |
| `python3 -m py_compile` 两个文件（CONTRIBUTING 清单要求） | OK |
| `ruff check --select E,F,W`（仓库没有 lint 配置，仅作参考） | 改动前后都是同样的 3 个既有问题，没有新增 |

没跑的：完整的 `make test`。它需要 `docker compose up` 起整套服务（包括 LLM 和外部 API key），本机条件不允许。

## 需要提交者注意

1. **PR 要开到 cuga-project/cuga-apps，不是 cuga-agent。** PR 描述里写了 `Closes cuga-project/cuga-agent#822`（跨仓库引用）。如果合并后 issue 没有自动关闭，可以在 issue 下留言附上 PR 链接。
2. **DCO 必须**（两个仓库的 CONTRIBUTING 都要求，issue 清单也写了 “Include git sign-off”）。patch 中已带 `Signed-off-by: anyingiit <49945850+anyingiit@users.noreply.github.com>`（按 WORKER_BRIEF 规则：仓库要求时允许加）。如果你想用自己的 sign-off 邮箱，`git am` 之后执行 `git commit --amend -s` 并删掉旧的那一行。
3. 提交信息和 PR 标题都是 Conventional Commits 格式，标题直接用了 issue 建议的标题。cuga-agent 使用 squash merge，PR 标题会成为最终提交信息。
4. 同文件存在 open PR **#23**（overlap 校验），它改的是 `chunk_text` 函数体和 docstring，以及在 `TestMcpText` 中加 `test_chunk_text_bad_overlap`。我们改的是 `_chunk_recursive` 两行和另一个新测试，逻辑上互不影响。若 #23 先合并，测试文件可能需要做一次很小的 rebase。
5. 仓库提交了 `__pycache__/*.pyc`。本地跑测试会改动这些文件，**不要**把它们一起提交（patch 里没有）。
6. cuga-agent 有 `ai-spam` 标签，且当天很多 agent 在提 PR。这个 PR 只有 2 行修复加 1 个测试，描述里写了 disclosure，保持简洁。

## 如何提交

```bash
gh repo fork cuga-project/cuga-apps --clone && cd cuga-apps
git checkout -b fix/mcp-text-chunk-separators origin/main      # base: main
git am /path/to/0001-fix-mcp-text-keep-separators-when-the-first-and-last.patch
git push -u origin fix/mcp-text-chunk-separators
gh pr create --repo cuga-project/cuga-apps --base main --head anyingiit:fix/mcp-text-chunk-separators \
  --title "$(cat pr_title.txt)" --body-file pr_body.md
```

PR 标题见 `pr_title.txt`，正文见 `pr_body.md`。

## 工作目录

- 修改所在的 clone：`/home/user/work/cuga-apps-822`（分支 `fix/mcp-text-chunk-separators`，提交 `17d49820bf86`）
- cuga-agent 参考 clone（只读，未改动、未执行）：`/home/user/work/cuga-agent-822`

## 独立复核

复核时间 2026-10-01 23:35 UTC，由独立复核 agent 完成：

- Issue 状态：#822 仍为 open，无 assignee，Development 区无关联 PR。cuga-apps 中按 `chunk` / `separator OR 822 OR recursive` 搜索 PR，只有 #23（overlap 校验），它修的是另一个 bug，不算重复。
- 补丁内容：只改了 `_chunk_recursive` 的 2 行，和 issue 给的修法一致。`server.py` 里已经没有别的 `is not parts[...]` 这类身份判断。递归子调用和 overlap 逻辑都没动。直接调用函数验证：两个输入分别返回 `['a\n\n', 'bbbbb\n\n', 'a']` 和 `['\n\n', 'bbbbbbbb\n', '\n']`，拼接后都等于原文。
- 红/绿测试：只起 mcp-text，3001 端口放一个占位监听，跑 `-k TestMcpText`。把 `server.py` 回退到 main 后是 5 failed / 5 passed，加上修复后是 4 failed / 6 passed，多出来的那个通过项就是新测试。剩下 4 个失败是 count_tokens/extract_text 测试，原因是本机没装 tiktoken/docling，跟这次改动无关，回退前后都一样失败。
- Lint：`py_compile` 两个文件都通过。`ruff check --select E,F,W` 在改动前后报的问题完全一样（2 个 E402 + 12 个 E501，用的是 ruff 默认行宽，所以数量和前面写的“3 个”对不上），没有新增。
- 交付物：`0001-*.patch` 和 `git format-patch -1 HEAD` 的输出逐字节一致。作者是 anyingiit <49945850+anyingiit@users.noreply.github.com>，带 DCO sign-off，patch 里没有出现任何 AI 模型名。`pr_body.md` 是英文，包含 Motivation/disclosure 段和 `Closes cuga-project/cuga-agent#822`。仓库没有 changelog 或 news fragment，不需要补。
- 小问题：前文提到的 `run_red_green.sh` 并没有留在 workdir 里，不过命令都已经写在“验证”一节，可以照着手动复现。
- 未发现需要修改的问题，提交没有 amend。

Status: ✅ ready：修复正确且完整，新测试修复前失败、修复后通过，交付物齐全且彼此一致。
