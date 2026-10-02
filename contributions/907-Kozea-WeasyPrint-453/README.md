# Kozea/WeasyPrint#453 — Support the print-color-adjust property

| 项 | 值 |
|---|---|
| Issue | https://github.com/Kozea/WeasyPrint/issues/453 |
| Tier | 高活跃高Star |
| Labels | feature, good first issue |
| Status | ✅ ready（但提交前必须先在 issue 里询问维护者，见下） |
| 重复 PR 检查 | 2026-10-01：PR 搜索 `453`、`color-adjust` 均无相关 PR；issue 无 assignee、无评论认领 |
| Base | `main` @ 369b153 |
| Patch | `0001-Support-the-print-color-adjust-property.patch` |

## 需要提交者注意（重要）

WeasyPrint 的 `.github/CONTRIBUTING.md` 指向 CourtBouillon 的 [Guidelines for Contributors](https://www.courtbouillon.org/code-of-conduct/#guidelines-for-contributors)，原文规则：

- **Use your own words, write with your keyboard.** → PR 描述/评论必须由你本人用自己的话手写。`pr_body.md` 只是参考，请务必自己重写，不要直接粘贴。
- **Stay short… Don't use long chapters with titles.** → 所以 `pr_body.md` 故意没有用 chefs-pick 模板的标题结构，只写了几行。
- **Ask before sending code. Open an issue or write a comment and wait for more information.** → 提交 PR 之前，先在 #453 下评论一句（例如问维护者：WeasyPrint 一直打印背景，是否接受“只解析并接受 `print-color-adjust`、两个值输出相同”的实现？），**等维护者回复后**再开 PR。
- **Don't open a pull request if you have another pull request opened on our projects.** → 若你在 Kozea/CourtBouillon 的任何项目（WeasyPrint、tinycss2、cssselect2、pydyf、Flask-WeasyPrint…）已有 open PR，先别提这个。
- 规则未禁止 AI 生成代码，但明显反感 AI 写的文字；PR 里保留一行简短披露。
- 不需要 DCO / Signed-off-by。changelog 由维护者在发版时写，无需改 `docs/changelog.rst`。

## 问题理解

用户问 WeasyPrint 是否支持 `-webkit-print-color-adjust: exact`（强制打印背景）。CSS Color Adjustment Level 1 定义了标准属性 `print-color-adjust: economy | exact`（继承，初始值 economy）。目前 WeasyPrint 不认识这个属性，`print-color-adjust: exact` 会触发 “unknown property” 警告。

## 合理性判断

- 维护者给 issue 打了 `feature` + `good first issue`，issue 仍 open。
- WeasyPrint 本来就总是完整绘制背景和颜色；规范中 `economy` 只是“允许” UA 做调整，不调整也合规。所以“支持”= 正确解析/继承该属性，不改变渲染，不会破坏现有输出。
- `-webkit-` 前缀：WeasyPrint 只处理 `-weasy-` 前缀，其他厂商前缀统一以 debug 级别忽略（不会产生警告），本 patch 不改变此设计。旧的 `color-adjust` 简写也未加（可在 PR 讨论中按维护者意见补）。

## 改动

- `weasyprint/css/properties.py`：`INITIAL_VALUES` 增加 `print_color_adjust: 'economy'`，并加入 `INHERITED`。
- `weasyprint/css/validation/properties.py`：新增 `print_color_adjust` 校验器（`@single_keyword`，接受 `economy`/`exact`）。
- `docs/api_reference.rst`：新增 “CSS Color Adjustment Module Level 1” 小节（说明 `color-scheme` 与 `print-color-adjust` 支持情况）。
- `tests/css/test_validation.py`：`test_print_color_adjust`（economy/exact）与 `test_print_color_adjust_invalid`（auto/none/`exact economy`/1px）。

## 验证

环境：Python 3.11 venv，`pip install -e '.[test]'` + ruff。本机无 Ghostscript。

- Red（无修复，仅测试）：`venv/bin/python -m pytest -q tests/css/test_validation.py -k print_color_adjust` → **6 failed**（unknown property）。
- Green（有修复）：同命令 → **6 passed**。
- 手动检查：`<html style="print-color-adjust: exact">` 下子元素 style 为 `exact`（继承生效），默认为 `economy`。
- `venv/bin/python -m ruff check` → All checks passed!
- 全量 `venv/bin/python -m pytest -q tests`：修复后 763 failed / 3594 passed / 43 xfailed；base 上 763 failed / 3585 passed（多出的 9 个就是新测试）。失败列表前后**完全一致**，几乎全部是缺 Ghostscript 的 `FileNotFoundError: 'gs'`（draw 测试），以及 `tests/test_url.py` 的少量与沙箱网络相关的失败，均与本改动无关。
- `tests/css` 全部通过。

## 如何提交

1. 先在 #453 评论询问并等待维护者回复（见上）。
2. ```bash
   git clone https://github.com/<你的fork>/WeasyPrint && cd WeasyPrint
   git checkout -b print-color-adjust origin/main
   git am /path/to/0001-Support-the-print-color-adjust-property.patch
   python -m pytest tests/css/test_validation.py -k print_color_adjust && python -m ruff check
   git push -u origin print-color-adjust
   gh pr create --repo Kozea/WeasyPrint --head anyingiit:print-color-adjust --title "$(cat pr_title.txt)" --body-file pr_body.md
   ```
   （body 建议先按自己的话改写。）

## PR title

Support the print-color-adjust property

## PR body（参考草稿，按仓库规则应短、无标题、用自己的话改写）

见 `pr_body.md`。
