# mpdf/mpdf#2232: SVG 表单对象无条件写透明组，macOS 打印丢失其后内容

| 项 | 值 |
|---|---|
| Issue | https://github.com/mpdf/mpdf/issues/2232 |
| Tier | 高星（mpdf/mpdf，~4.4k★） |
| Labels | SVG, bug/fix, help wanted |
| Status | ✅ ready（patch + PR 文本就绪，未提交） |
| 重复 PR 检查 | 2026-10-22 20:00 UTC：open PR 列表（#2233 #2230 #2227 …）无相关；issue 0 评论、无 assignee、无关联 PR |
| AI 政策 | CONTRIBUTING："AI-made PRs are not disapproved of, but must be declared as such, preferably with a co-authorship note in the third line of the commit message"。commit 第三行已写 `Assisted-by: Claude Code`（不写模型名，符合 owner 规则） |
| Base | `development` @ a981bb7（默认分支，不是 master） |
| DCO / CLA | 无 |
| 需先认领 | 否 |

## 问题理解
`FormWriter` 给每个 SVG form XObject 写 `/Group <</S /Transparency>>`。issue 作者手改 PDF 证明：去掉 form 级 group 后 macOS 打印正常。group 只在 SVG 有半透明时才需要。

## 改动
- `src/Image/Svg.php`：新增私有属性 `$usesTransparency`，在 fill/stroke opacity < 1（路径与文字两处）、渐变 stop-opacity < 1（两处）、内嵌带 alpha mask 的图片时置 true；`ImageSVG()` 开头重置，返回值带 `'transparency'`。
- `src/Writer/FormWriter.php`：仅当 `transparency` 为真时写 `/Group` 及 group 对象。WMF 不再有 group（WMF 无透明）。
- `tests/Issues/Issue2232Test.php`：1 个不透明 + 5 个半透明数据集。
- `CHANGELOG.md`：8.3.x Bugfixes。
- 遵守 PHP 5.6 下限（无 ??、无类型声明），tab 缩进。

## 验证
- 红：回退 src → 不透明用例失败；把置 true 全改 false → 5 个半透明用例失败。绿：6/6。
- 全量 `vendor/bin/phpunit` → 992 tests，唯一错误 ImbTest（缺 bcmath，base 同样失败）。
- phpcs（ruleset.xml）干净；PHPStan 2.3.1 No errors。
- 渲染对比：issue 复现脚本（不透明 + fill-opacity 0.5 两版）用 pdftoppm 光栅化，前后像素完全相同；pdfinfo 解析正常。
- 未跑：snapshot 测试（需 imagick+ghostscript）、macOS 实机打印。

## 需要提交者注意
- base 分支是 `development`。
- commit 第三行 `Assisted-by: Claude Code` 是仓库要求的 AI 声明，保留。

## 如何提交
```
tools/submit_pr.sh contributions/333-mpdf-mpdf-2232 mpdf/mpdf development fix/2232-svg-transparency-group contributions/333-mpdf-mpdf-2232/pr_title.txt contributions/333-mpdf-mpdf-2232/pr_body.md
```

## 独立复核（2026-10-22 20:13 UTC）
- Issue #2232：WebFetch 确认仍 open、无 assignee、无评论、无关联 PR/分支。PR 搜索（`repo:mpdf/mpdf 2232`、`transparency`、open 的 `svg` PR）无竞争 PR。注意：open 的 #2196（给 SVG form XObject 加 `/Resources`）改的是 `FormWriter::writeFormObjects()` 同一循环，两者谁后合入都可能有小的文本冲突，但不是竞争实现。
- 全新 clone `development`@a981bb7，`git am` 干净应用；作者 `anyingiit <49945850+anyingiit@users.noreply.github.com>`；commit 消息为单行标题 + 空行 + `Assisted-by: Claude Code`（第三行声明 AI，不含模型名）。
- 测试：新测试 6/6 通过；全量 `vendor/bin/phpunit` 992 tests，唯一错误是 ImbTest（缺 bcmath），在 base 上同样失败。phpcs（ruleset.xml）对 3 个 php 文件无输出；PHPStan 2.3.1 `[OK] No errors`。
- 红→绿：只回退 src 时，不透明用例失败（1 failure）；把所有 `usesTransparency = true` 改成 false 时，5 个半透明数据集全部失败。与 PR 描述一致。
- 正确性：Svg.php 里所有会写入透明 ExtGState 或 SMask 的地方都已覆盖，包括路径 fill/stroke opacity（svgStyle）、两处文字 opacity、线性和径向渐变的 `trans`（TGS）、带 alpha mask 的内嵌栅格图。另外用 14 个边界用例对比了 base 和补丁的输出：`<g opacity>` 继承、`<g style="fill-opacity">`、嵌套 `<svg>`、`<tspan>` 的 fill-opacity、文字 stroke-opacity、径向渐变 stop-opacity、alpha PNG 都保留 group；不透明矩形、不透明 PNG、`opacity="1"` 都去掉了 group。`rgba()` 填色和 `opacity="50%"` 也没有 group，因为 mPDF 原本就会把它们的 alpha 算成 1（输出里 `/ca 1`，这是既有 bug），去掉 group 不改变任何渲染。`<use>` 本来就不支持。WMF（Wmf.php）没有 ExtGState 或透明，跳过 group 是安全的。
- 渲染：14 个用例用 pdftoppm 光栅化，前后 PNG 字节完全相同；pdfinfo 都能正常解析。对象编号：用多个 SVG 混合（不透明/半透明/不透明/SVG 背景图）的文档校验，xref 25 个对象的偏移全部指向正确的 `N 0 obj`，唯一的 form `/Group 18 0 R` 指向 `/S /Transparency` 对象。`writer->object()` 按顺序递增编号，省掉 group 对象不会留下空洞。
- 兼容性：没有 `??`，没有类型声明，`private $usesTransparency = false;` 在 PHP 5.6 下可用；新增行都用 tab 缩进；属性已声明（Svg 本身不用 Strict trait，但已声明，所以不受影响）。测试的 namespace 和风格与 tests/Issues 下的其他测试一致。
- PR 正文和 README：992 tests、6 tests、PHPStan 2.3、CHANGELOG 放在 8.3.x Bugfixes、CONTRIBUTING 的 AI 声明引文，都已核实无误。仓库没有 PR 模板。
- 附注（不阻塞）：严格来说，非隔离、非 knockout、Normal 混合模式的 form group 与不加 group 合成结果相同，所以维护者也可能倾向于完全去掉 group。当前做法（半透明 SVG 输出保持不变）更保守，也符合 issue 的提议；代价是半透明 SVG 在 macOS 打印时可能仍有这个问题。可在 review 中讨论。
- 复核过程中共享磁盘一度满盘，只影响一次被丢弃的 cp；所有检查都在磁盘正常时完成或重跑过。复核用的 clone 已删除。
- 结论：PASS
