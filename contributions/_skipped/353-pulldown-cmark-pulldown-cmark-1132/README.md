# pulldown-cmark/pulldown-cmark#1132 — ENABLE_HEADING_ATTRIBUTES: ATX heading swallows next line after lone CR

| 项 | 值 |
|---|---|
| Issue | https://github.com/pulldown-cmark/pulldown-cmark/issues/1132 |
| Tier | 自由 |
| Labels | 无 |
| Status | ⏭ skipped — master 已修复（PR #1091, commit 8e9ee37 "Recognize lone CR as a line ending in scan_nextline"），issue 是针对已发布的 0.13.4 报告的 |
| 重复 PR 检查 | 2026-10-01：`/pulls?q=1132` 与 "heading CR" 关键字均无针对本 issue 的 PR |

## 问题理解
开启 `ENABLE_HEADING_ATTRIBUTES` 时，ATX 标题若以单独的 `\r` 结尾，会把下一行吞进标题（`"# a\r$"` → 标题 0..5、文本 `"a\r$"`）。根因：该分支用 `scan_nextline` 求标题行尾，而旧的 `scan_nextline` 只认 `\n`。

## 结论（为何跳过）
- 在 master @ c61583e 上复现失败：带/不带该选项，`"# a\r$"`、`"#\u{b}\r$"`、`"# a {#x}\r$"` 的 HTML 与 offset 完全一致且正确。
- 把 `scan_nextline` 改回只认 `\n`（即 #1091 之前的实现）后，回归测试立即失败（`right: "<h1>a\r$</h1>\n"`），证实 #1091（2026-05 合入，早于 issue 的 2026-08-09）就是修复，只是尚未发布（reporter 用的是 0.13.4）。
- 因此不需要代码改动；纯测试 PR 价值有限，故跳过。

## 需要提交者注意（可选）
若愿意，可在 issue 下留言告知已在 master 修复，例如：

> This looks already fixed on master by #1091 (`scan_nextline` now treats a lone CR as a line ending). On c61583e, `"# a\r$"` and `"#\u{b}\r$"` give the same events/offsets with and without `ENABLE_HEADING_ATTRIBUTES`, so it should be resolved in the next release.

下面是验证用的回归测试（未提交，供参考；放在 `pulldown-cmark/tests/html.rs` 末尾）：

```diff
diff --git a/pulldown-cmark/tests/html.rs b/pulldown-cmark/tests/html.rs
index f02a7c1..fee0889 100644
--- a/pulldown-cmark/tests/html.rs
+++ b/pulldown-cmark/tests/html.rs
@@ -395,3 +395,25 @@ fn issue_1131_crlf() {
 
     assert_eq!(expected, s);
 }
+
+// Can't easily use regression.txt due to newline normalization.
+#[test]
+fn issue_1132_heading_attributes_lone_cr() {
+    for (original, expected) in [
+        ("# a\r$", "<h1>a</h1>\n<p>$</p>\n"),
+        ("# a {#x}\r$", "<h1 id=\"x\">a</h1>\n<p>$</p>\n"),
+        ("#\u{b}\r$", "<h1></h1>\n<p>$</p>\n"),
+    ] {
+        let mut without = String::new();
+        html::push_html(&mut without, Parser::new(original));
+        let mut with = String::new();
+        html::push_html(
+            &mut with,
+            Parser::new_ext(original, Options::ENABLE_HEADING_ATTRIBUTES),
+        );
+        assert_eq!(expected, with, "input: {original:?}");
+        if !original.contains('{') {
+            assert_eq!(without, with, "input: {original:?}");
+        }
+    }
+}
```

验证命令：`CARGO_TARGET_DIR=... cargo test -q --test html issue_1132` → master 上 1 passed；回退 scanner 后 1 failed。
