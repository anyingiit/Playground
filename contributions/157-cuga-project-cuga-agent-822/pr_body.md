## Description

Fixes the separator loss in the `text` MCP server's recursive chunking reported in cuga-project/cuga-agent#822
(the issue is filed on cuga-agent, but `mcp_servers/text/server.py` lives here in cuga-apps).

**Root cause.** `_chunk_recursive` decided whether a piece was the last one with the identity check
`part is not parts[-1]`. When the first and last pieces are equal one-character or empty strings, CPython hands back
the same cached object for both, so the first piece is treated as the last and loses its separator. The chunks then
no longer join back to the input:

```python
_chunk_recursive("a\n\nbbbbb\n\na", 6, 0, _RECURSIVE_SEPARATORS)
# before: ['a', 'bbbbb\n\n', 'a']   -> "".join(...) != text
# after:  ['a\n\n', 'bbbbb\n\n', 'a']

_chunk_recursive("\n\nbbbbbbbb\n\n", 6, 0, _RECURSIVE_SEPARATORS)   # text starting/ending with a separator
# before: ['bbbbbbbb\n']            (leading "\n\n" and one "\n" lost)
# after:  ['\n\n', 'bbbbbbbb\n', '\n']
```

**Fix.** Use the loop index, as proposed in the issue: `for i, part in enumerate(parts)` with
`sep if i < len(parts) - 1 else ""`. Nothing else in the function changes.

**Test.** Added `TestMcpText::test_chunk_text_recursive_keeps_separators` to `tests/test_mcp_tools.py`, in the same
style as the existing `chunk_text` tests (it calls the tool over MCP). It checks that both inputs above join back to
the exact text with `overlap=0`.

This touches the same file as the open #23 (overlap validation in `chunk_text`), but different lines. If both are
merged, the only possible conflict is the new tests sitting next to each other in `TestMcpText`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes cuga-project/cuga-agent#822

## Checklist

- [x] Tests pass locally. With only `mcp-text` running (`MCP_BIND_HOST=127.0.0.1 python mcp_servers/text/server.py`
      on 29106, plus a placeholder listener on 3001 so the conftest "stack is up" guard passes), from `cuga-apps/`:
      `CUGA_TEST_HOST=127.0.0.1 pytest tests/test_mcp_tools.py -k "TestMcpText and chunk"` gives **5 passed**. With
      the fix reverted, the new test fails (`['a', 'bbbbb\n\n', 'a'] != ['a\n\n', 'bbbbb\n\n', 'a']`) and the other 4 pass.
- [x] The repro from the issue now prints `['a\n\n', 'bbbbb\n\n', 'a'] True`.
- [x] Extra check: 20,000 random texts built from `a`, `b`, `\n\n`, `\n`, `. `, ` ` with sizes 1–12 and `overlap=0` give 0 join
      mismatches after the fix, compared with 10,618 before.
- [x] `python3 -m py_compile` passes on both touched files (CONTRIBUTING checklist).
- [x] Commit is signed off (DCO).
- [ ] `CHANGELOG.md` is updated (if applicable): n/a, the repo has no changelog.
- [ ] Documentation is updated (if applicable): n/a, no behaviour or API change beyond the bug fix.
