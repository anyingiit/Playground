# Kozea/WeasyPrint #453 — Support the print-color-adjust property

| 项 | 值 |
|---|---|
| Issue | https://github.com/Kozea/WeasyPrint/issues/453 |
| Tier | 高活跃高Star |
| Labels | feature, good first issue |
| Status | ✅ ready（需先在 issue 下询问，见“需要提交者注意”） |
| 重复 PR 检查 | issue 没有评论、没有指派人，Development 栏显示 “No branches or pull requests”；在 PR 中搜索 `print-color-adjust` 只找到一个无关的 #303（2026-10-01） |
| Base | `main` @ 369b15340ea97c5d649af65e8e10330b8d08f01f |

## ⚠️ 需要提交者注意

WeasyPrint 的 `.github/CONTRIBUTING.md` 指向 CourtBouillon 的 [Guidelines for Contributors](https://www.courtbouillon.org/code-of-conduct/#guidelines-for-contributors)，其中有几条要求：

1. **"Ask before sending code. Open an issue or write a comment and wait for more information."**
   提交 PR 之前，请先**亲自**在 #453 下留言，询问维护者是否接受这种做法（只解析/保存该属性，两个取值渲染结果相同），**等到回复后再提交**。
2. **"Use your own words, write with your keyboard. Stay short."**
   这条规则没有提到 AI，但明确要求文字由本人亲手写。因此 issue 留言和 PR 描述**请用自己的话重写**，并且写短。`pr_body.md` 只能作为要点参考，不要直接粘贴。
   披露段落可以保留，也可以改成一句自己写的话，例如 “prepared with help of Claude Code”。
3. **"Don't open a pull request if you have another pull request opened on our projects."**
   提交前请确认你在 Kozea/CourtBouillon 的项目（WeasyPrint、tinycss2、pydyf、cssselect2 等）里没有其他未合并的 PR。
4. 不需要 DCO 或 Signed-off-by。仓库也没有 PR 模板。changelog 由维护者在发版时统一写，本 PR 没有修改它。
5. 维护者可能希望同时支持 `-webkit-print-color-adjust`。issue 原文问的就是带前缀的写法。WeasyPrint 只认 `-weasy-` 前缀，所以本 PR 没有加这个别名。PR 描述里已经说明，可以按维护者的意见补上。

## 问题理解

用户希望支持 `print-color-adjust`（以及 `-webkit-print-color-adjust`），特别是 `exact` 这个值，用来强制打印背景。目前 WeasyPrint 不认识这个属性，遇到它会给出 "unknown property" 警告并忽略。

## 合理性判断

- 这是 CSS Color Adjustment Level 1（CRD）中的标准属性。WeasyPrint 已经支持同一规范里的 `color-scheme`，`properties.py` 里也有 “Color Adjustment 1” 这一节。
- 按规范，`economy` 只表示 UA “可以”做调整，所以不做任何调整也符合规范。WeasyPrint 本来就始终渲染背景，因此支持这个属性的实际含义是：接受它、作为继承属性计算出值、不再报警告，并在文档里说明。这样改动很小，风险也很低。

## 改动

- `weasyprint/css/properties.py`：在 `INITIAL_VALUES` 里加入 `print_color_adjust: 'economy'`，并把它加入 `INHERITED`。
- `weasyprint/css/validation/properties.py`：新增 `print_color_adjust` 校验器（`@single_keyword`，只接受 `economy`/`exact`）。
- `docs/api_reference.rst`：新增 “CSS Color Adjustment Module Level 1” 一节，说明支持 `color-scheme` 和 `print-color-adjust`（两个值效果相同），不支持 `forced-color-adjust`。
- 测试：在 `tests/css/test_validation.py` 中新增合法值和非法值的测试，在 `tests/css/test_common.py` 中新增继承测试。

## 验证（Python 3.11，venv：`pip install -e '.[test]' pytest-xdist ruff`）

- red：先只改测试、不改源码，运行 `pytest tests/css/test_validation.py tests/css/test_common.py -k print_color_adjust`，结果 **7 failed**（unknown property 和 KeyError）。
- green：加上修复后，同一条命令 **7 passed**。
- 全量：`pytest -q -n 4` 的结果为 3595 passed、763 failed、43 xfailed。这 763 个失败在 base 上完全相同（用 diff 对比过失败列表），原因都是本机没有安装 Ghostscript（`gs`），属于 draw/api 类测试，与本改动无关。
- `python -m ruff check`：All checks passed。

## 如何提交

```bash
# 前提：已在 #453 留言并得到维护者认可（见上文）
git clone https://github.com/anyingiit/WeasyPrint && cd WeasyPrint
git remote add upstream https://github.com/Kozea/WeasyPrint && git fetch upstream
git checkout -b print-color-adjust upstream/main
git am /path/to/0001-Support-the-print-color-adjust-property.patch
git push origin print-color-adjust
gh pr create --repo Kozea/WeasyPrint --head anyingiit:print-color-adjust \
  --title "$(cat pr_title.txt)" --body-file pr_body.md   # 先按上文要求，用自己的话改写 body
```

## PR title

Support the print-color-adjust property

## PR body

见 `pr_body.md`（提交前请用自己的话改写）。
