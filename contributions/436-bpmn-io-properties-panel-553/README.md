# 436 — bpmn-io/properties-panel#553: 已勾选且禁用的复选框，对勾看不见

| 项 | 内容 |
|---|---|
| Issue | https://github.com/bpmn-io/properties-panel/issues/553 |
| 层级 | 高星生态（bpmn.io / Camunda，桌面版和 Web Modeler 共用） |
| Labels | a11y, backlog, good first issue, pr welcome（维护者 barmac 9-30 加的） |
| Base 分支 | `main`（补丁基于 193caac，即 3.58.0） |
| 状态 | ✅ 可提交（复核 PASS） |
| 重复检查 | 2026-10-22：issue 没有关联 PR，也没有指派；仓库只开着 2 个 renovate PR |
| AI 政策 | 无 |
| CLA/DCO | **需签 bpmn-io CLA**（与 432/434 同一个） |

## 改动
- `properties-panel.css`：
  - 新增 token `--checkbox-checked-disabled-background-color`，默认值为 `var(--input-disabled-color)`，即 `--bio-text-subtlest`，hsl(225,10%,55%)。
  - 新增 `:checked:disabled` 规则，把背景和边框都设为这个 token，对勾保持白色。
- `styling.spec.js`：新增测试，计算禁用且勾选状态下背景与白色对勾的对比度，要求 ≥ 3:1（WCAG 非文本对比度），并附带两个小 helper。

## 验证
- 红：只回退 CSS，新测试失败，`expected 1.0706310998416164 to be at least 3`。
- 绿：`npm test` 结果 793 个测试，791 通过，2 跳过，0 失败。`npm run lint` 和 `npm run lint:theme` 都通过。
- 改后对比度约 3.6:1。
- 环境说明：
  - 要先 `npm run build`，因为测试依赖构建产物。
  - Chromium 以 root 运行需要 `--no-sandbox`，用的是 /home/user/work/bin/chrome-nosandbox 包装脚本。
- 设计取舍：
  - 用灰色背景配白色对勾，接近原生禁用复选框的样子，又与启用状态的蓝色区分开。
  - issue 里提到的另一种方案（深色对勾配浅色背景）需要再写一个 data URI，而且不能用 CSS 变量，所以没选。
- 没有截图。模板的 Screenshots 项未勾，PR 正文给了对比度数据和试用步骤。

## 如何提交
```
git clone https://github.com/bpmn-io/properties-panel && cd properties-panel && git checkout -b fix-disabled-checked-checkbox origin/main
git am /path/to/0001-*.patch
```

## 独立复核（2026-10-22）
- 新克隆后 origin/main 仍为 193caac，`git am` 干净应用。修法采用 issue 给出的第一种方案。
- CSS：
  - 新规则特异性 (0,3,1)，高于 `:checked` 和 `:disabled` 的 (0,2,1)，位置也在两者之后。
  - token 命名一致；仓库里没有需要同步的文档或 token 清单。
  - forced-colors 模式不受影响。
  - headless 截图确认改后是灰底白勾，清晰可见。
- 测试：
  - 793 个，791 通过，2 跳过。
  - 红：新用例报 `expected 1.07… to be at least 3`；绿：全部通过。
  - lint 和 lint:theme 通过。
  - 对比度公式正确。
- 首轮唯一的必改项：对比度应为 **3.59:1**（背景 rgb(129,135,152)），不是 3.9。已在 PR 正文和本文件改为约 3.6:1，结论不变。
- 建议（未做）：
  - 边框单独加一个 token。
  - 提交时附改前和改后截图，并勾选 Screenshots。barmac 在 issue 里要过截图。本地提交方如有条件可以补，也可以等维护者要求时再补。
- 结论：PASS
