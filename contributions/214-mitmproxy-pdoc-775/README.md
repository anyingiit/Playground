# 214 — mitmproxy/pdoc#775: Google 风格转换把代码块里的 "ABC:" 当成小节

| 项 | 内容 |
|---|---|
| Issue | https://github.com/mitmproxy/pdoc/issues/775 |
| 层级 | 自由（约 2.2k stars） |
| Labels | bug |
| Base 分支 | `main`（补丁基于 00e18eb） |
| 状态 | ✅ 可提交 |
| 重复检查 | 2026-10-22：无指派、无关联 PR；`pulls?q=775`、`google code block`、`fenced` 均无相关 PR |
| AI 政策 | CONTRIBUTING 无 AI 条款；要求补丁带测试、100% 覆盖 |
| CLA/DCO | 无 |

## 问题理解
`--docformat google` 时 `docstrings.google()` 的小节正则作用于整个 docstring，包括 ``` 代码块，导致代码块里的 `ABC:` + 缩进行被转成标题和引用。维护者 mhils："Clearly a bug … contributions welcome!"

## 改动
- `google()` 只对 fenced 代码块之外的文本做小节转换（新 helper `_outside_fenced_code_blocks`）。
- 逐行线性扫描（不用回溯正则，避免大 docstring 上的二次复杂度）：只跳过行首（不缩进）的 ``` / ~~~ 代码块，按 CommonMark 规则由同字符、长度不短于开头的 fence 闭合（````md 内嵌 ``` 也正确）；缩进在小节内部的代码块（如 `Examples:` 下的示例）仍属于该小节，行为不变。未闭合的 fence 当普通文本，行为不变。
- NumPy 风格理论上有类似问题，未扩大范围，PR 正文说明。
- CHANGELOG Unreleased 加一行（仓库注释说 PR 链接由 CI 自动补）。

## 验证
- 新测试 `test_google_fenced_code_block`：main 上失败（红），修复后通过。
- `pytest --cov=pdoc -m "not slow"` 155 passed，docstrings.py 100%（总 99% 是 doc_types.py:195，基线相同，与环境有关）；全量 `pytest test/` 360 passed（快照测试全部不变）；ruff check/format、mypy 通过。

## 独立复核
- 独立 agent 复核：可提交。复现了全部测试数字与红测试。指出原正则版本在大量未闭合带 info 的 fence 时为二次复杂度（30000 段 106s），且不处理更长 fence。
- 已改为逐行扫描：同一输入 0.035s；补充两条断言（````md 内嵌 ```、未闭合 fence 照常转换），旧代码上测试仍为红。

## 需要提交者注意
- 维护者最近一次合并在 2026-04，有 21 个 PR 排队，合并可能较慢。

## 如何提交
```
git clone https://github.com/mitmproxy/pdoc && cd pdoc && git checkout -b google-fenced-code origin/main
git am /path/to/0001-*.patch
```
