# 434 — bpmn-io/bpmn-to-image#65: README 说明 CLI 分隔符随平台不同（Windows 用 `;`）

| 项 | 内容 |
|---|---|
| Issue | https://github.com/bpmn-io/bpmn-to-image/issues/65 |
| 层级 | 高星生态（bpmn.io / Camunda） |
| Labels | backlog, bug, pr welcome |
| 维护者态度 | nikku 解释过：Windows 路径里会有 `:`，所以不能统一用它当分隔符；真正的修法是把输入和输出拆成两个参数，属于破坏性改动。报告人请求至少在文档里注明平台差异，nikku 点了 👍。之后 nikku 取消了自己的指派，issue 回到 backlog。 |
| Base 分支 | `main`（补丁基于 d9907a1） |
| 状态 | ✅ 可提交（复核 PASS） |
| 重复检查 | 2026-10-22：仓库没有开着的 PR；#66（报告人）和 #67（nikku 草稿）都是改 CLI 语法的，已关闭；没有改文档的 PR。issue 无人指派。 |
| AI 政策 | 无 |
| CLA/DCO | **需签 CLA assistant**（和 432 同一个 bpmn-io CLA，签一次即可） |

## 改动
- 只改 README：在 Usage 代码块后加一段 Note，说明以下几点：
  - 分隔符是 `path.delimiter`，在 Linux/macOS 上是 `:`，在 Windows 上是 `;`；
  - `--help` 会显示当前平台用的分隔符；
  - 第一个示例在 Windows 下的写法，并加了引号（PowerShell/Bash 里 `;` 是命令分隔符）。
- 用 `Related to #65`，不关闭 issue，因为拆分参数的正式修法还没做。

## 验证
- `node cli.js --help` 在 Linux 下显示 `<diagramFile>:<outputConfig>`，说明帮助文本是动态的（cli.js 用 `${pathDelimiter}`）。
- `require('path').win32.delimiter === ';'`。`'C:\\x\\diagram.bpmn;diagram.png'.split(';')` 得到输入和输出两部分，和 Note 描述一致。
- 纯文档改动，没有可写的红→绿测试。

## 如何提交
```
git clone https://github.com/bpmn-io/bpmn-to-image && cd bpmn-to-image && git checkout -b docs-cli-delimiter origin/main
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
- 新克隆后 origin/main 仍为 d9907a1。`git am` 干净应用，`git diff --check` 无问题。
- 维护者态度：nikku 给报告人"至少更新文档"的评论点了 👍，标签含 pr welcome。信号不算强，但没有拒绝。
- 已核实的事实：
  - cli.js 的帮助、拆分和报错信息都用 `${pathDelimiter}`；
  - win32 下分隔符为 `;`；
  - PowerShell 和 Bash 需要加引号；
  - cmd 和 npm shim 下加引号也无害，说明没有误导。
- PR 模板标题和清单逐字一致，有 AI 披露段落；作者正确，没有模型名。
- 没有竞争 PR（#66、#67 改的是 CLI 语法，均已关闭）。
- 可选小问题：Windows 示例没有 `$` 前缀。不改。
- 提交前需签 bpmn-io CLA（和 432 是同一个）。
- 结论：PASS
