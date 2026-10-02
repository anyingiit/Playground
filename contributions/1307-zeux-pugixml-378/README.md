# zeux/pugixml#378 — PugiXML incorrectly handles char8_t in C++20

| 项 | 值 |
|---|---|
| Issue | https://github.com/zeux/pugixml/issues/378 |
| Tier | 自由 |
| Labels | 无 |
| Status | ⏭️ skipped — 维护者已亲自尝试修复并主动放弃 (PR #719 closed unmerged, 2026-05-18) |
| Duplicate-PR check | `pulls?q=378` 和 `pulls?q=char8_t`（2026-10-01 23:05 UTC）：#719（zeux 本人，closed 未合并），#529 "Add char8_t mode"（gix，open since 2022，维护者称与 #378 "a little related"） |

## 问题理解

C++20 下 `xml_attribute::set_value(u8"text")` 的实参类型为 `const char8_t*`，无法隐式转换为 `const char_t*`，于是走了指针→`bool` 的标准转换，选中 `set_value(bool)`，属性值被写成 `"true"`。Issue 无评论、未指派。

## 合理性判断 / 跳过原因

- 维护者 zeux 本人在 2026-05 开了 PR #719（"Delete xml_attribute::set_value/xml_text::set overloads for char8_t*"，直接引用 #378）。
- 评论中有人建议改用 `reinterpret_cast` 实现 char8_t 重载（即 scout 建议的方案 A），zeux 明确拒绝：不打算给出 char8_t 支持的假象。
- 随后 zeux 自己关闭了 #719：认为 `wchar_t`/`char` 之间存在同类问题，真正的解法是删除 `const void*` 一类的重载，但会破坏现有代码且无法验证，因此暂不处理。
- 也就是说，scout 提出的两种方案（加 char8_t 重载 / 拦截指针→bool）维护者都已考虑过并决定不做。现在提交外部 PR 会与维护者近期的明确决定相冲突，因此跳过。
- 未 clone、未运行任何代码（不需要 AUDIT.md）。不在排除列表中（已 grep 确认）。
