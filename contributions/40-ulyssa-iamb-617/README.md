# ulyssa/iamb #617 — option to disable rich (HTML) message rendering

Status: ✅ ready — patch + PR text done

| 项 | 值 |
|---|---|
| Issue | https://github.com/ulyssa/iamb/issues/617 "Option to disable markdown and html rendering" |
| Tier | 自由 (ulyssa/iamb, ~1.3k★, Rust Matrix TUI client; outside PRs merged daily, e.g. #727–#740 by contributor vaw) |
| Labels | configuration, good first issue, ui (maintainer added `good first issue` on 2026-09-23, milestone "Future Release") |
| Status | open, no assignee, no comments, "Development: No branches or pull requests" |
| Duplicate-PR check | 2026-09-24, checked at start and again before finishing: open PR list (#732, #707, #696, #677, #670, #578, #566, #517, #512, #439) has nothing related; PR searches `html`, `formatted`, `617` only return old merged/unrelated PRs (#643 default_markup, #573 link fallback, #509, #486 …) |
| Base | `main` @ `a99b116` (2026-09-24) |
| Patch | `0001-Add-message_html_display-option-to-show-the-plain-te.patch` |

## 选题过程（简记）
- 用 `r.jina.ai` 渲染 GitHub issue 搜索页（Go/Rust，`good first issue` / `help wanted`），再用 shields.io 查 star 数。
- 跳过的候选：saphyr-rs/saphyr #79（`parser/tests/closing_bracket.rs` 已经覆盖 4H7K，问题已修好）、git-pkgs/vers #31（清单全部勾完）、oras-go #1376（依赖 #1451，属于大的 breaking 设计）、deb-sig/double-entry-generator #214（只是重写文档，没法用测试验证）、safedep/vet #739（已经有人认领，而且可能是服务端的问题）、samber/ro #106/#84（有人认领/已有人在做）、sorairolake/lzip-go（9★）、大部分 Stellar 相关的 issue 农场。

## 问题理解
issue 想要一个配置项：不渲染消息的 rich 内容（HTML/markdown），直接显示原始内容。iamb 在 `Message::show_msg`（`src/message/mod.rs`）里，如果消息有 `formatted_body`（`org.matrix.custom.html`）就用 `StyleTree::to_text` 渲染 HTML，否则显示纯文本 `body`。发送方写的 markdown 在发出去之前已经转成了 HTML，所以在接收端，"关掉 markdown 和 html 渲染"就等于"总是显示纯文本 `body`"。

## 合理性判断
- 维护者（ulyssa）加了 `configuration` + `good first issue` + `ui` 标签和 milestone，说明认可这个需求。
- 仓库里没有 AI 政策（`CONTRIBUTING.md`、`.github/` 里都没有 AGENTS/CLAUDE.md，grep LLM/AI/Copilot 也没找到）。CONTRIBUTING 要求：修 bug/加功能要加测试，新功能要写文档，这两条都做了。
- 实现方式照着已有的 `*_display` 布尔 tunable（`message_shortcode_display`、`reaction_display`、`state_event_display`）和最近的 #727（`send_on_enter`：改 `docs/iamb.5`、`src/config`、`src/tests.rs`）来写。

## 改动
- `src/config/mod.rs`：新增 tunable `message_html_display`（`TunableValues: bool`，`Tunables: Option<bool>`，参与 merge，默认 `true`，所以默认行为不变）。
- `src/message/mod.rs`：`show_msg` 在 `if let Some(html) = &self.html && settings.tunables.message_html_display` 时才渲染 HTML，否则走已有的纯文本分支（`message_shortcode_display` 在这里照样生效）。`self.html` 仍然会解析，所以 `:open` 的链接提取（`windows/room/chat.rs`）不受影响。
- 新测试 `message::tests::test_show_msg_html_display`：同一条 HTML 消息（`**hello** <world>` / `<strong>hello</strong> &lt;world&gt;`），默认情况下渲染成 `hello <world>`，设成 `false` 之后显示 `**hello** <world>`。
- `src/tests.rs`：`mock_tunables()` 加上这个字段；`docs/iamb.5` 写了说明；`config.example.toml` 加了一行（`test_load_example_config` 会解析这个文件）。

## 验证
环境：rust 1.98.1（仓库 pin 的是 1.96，因为磁盘不够没有另装，用 `RUSTUP_TOOLCHAIN=1.98.1` 覆盖），`CARGO_PROFILE_DEV_DEBUG=0`，CARGO_HOME/target 都放在 work 目录。

| 命令 | 结果 |
|---|---|
| `cargo test --locked`（patch 分支） | ✅ `test result: ok. 124 passed; 0 failed`（main 上原来是 123 个，新增 1 个） |
| red：只撤回 `show_msg` 里的条件，其他不动，跑 `cargo test --locked html_display` | ❌ `left: "hello <world>"  right: "**hello** <world>"`（符合预期） |
| green：恢复之后 | ✅ `test_show_msg_html_display ... ok` |
| `find src -name '*.rs' \| xargs ./.github/workflows/check-imports-format.sh` | ✅ exit 0 |
| `cargo clippy --all-targets -- -D warnings`（1.98） | 只有 2 个报错，都在**没改动**的文件里（`src/notifications.rs:304` `useless_borrows_in_formatting`，`src/util.rs:113` `question_mark`），是 1.98 新加的 lint，CI 用的 1.96 没有；改动的文件没有任何 clippy 报错 |
| rustfmt | 没装 nightly。stable rustfmt 会忽略 `binop_separator = "Back"`，所以对整个仓库都报差异；把 main 和分支的 `rustfmt --check` 输出做 diff，唯一新增的差异就是这个 let-chain 的 `&&` 放在行尾，这正是仓库用的 `binop_separator = "Back"` 风格（和上面几行已有的 `if let Some(prev) = prev &&` 一致）。 |

没跑的：nightly `cargo fmt --check`、1.96 的 clippy、Windows/macOS CI、nix flake check。

## 需要提交者注意
- 仓库没有 AI 政策，PR 模板也没有要求。commit 里没有 `Signed-off-by`，也不需要 DCO。
- 提交前建议在本地用 1.96 或 nightly 跑一次 `cargo +nightly fmt --all -- --check`。
- 名字 `message_html_display` 是我选的（跟现有的 `message_shortcode_display` 一致）；如果维护者想换名字（比如 `message_formatting_display`），只要改名就行。

## 如何提交
```sh
git clone https://github.com/ulyssa/iamb && cd iamb
git checkout -b message-html-display a99b116   # or latest main
git am /path/to/0001-Add-message_html_display-option-to-show-the-plain-te.patch
git push <fork> message-html-display   # open PR against ulyssa/iamb main
```

## PR title
Add `message_html_display` option to show the plain text body of messages

## PR body
```markdown
## Description

This adds a `message_html_display` setting (default `true`, so nothing changes unless it's set). When it is `false`, `Message::show_msg` skips rendering the formatted (`org.matrix.custom.html`) body and shows the message's plain text `body` instead, i.e. the raw content as it was sent. Markdown is already converted to HTML by the sender, so on the receiving side this turns off both the markdown and the HTML rendering the issue asks about.

The parsed HTML tree is still kept, so link gathering for `:open` works the same as before. `message_shortcode_display` still applies to the plain text path.

Following the existing `*_display` tunables and #727, the change touches:
- `src/config/mod.rs`: new tunable (merge + default)
- `src/message/mod.rs`: the check in `show_msg`, plus a test
- `src/tests.rs`: `mock_tunables()`
- `docs/iamb.5`: documentation
- `config.example.toml`: example entry (also covered by `test_load_example_config`)

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #617

## Checklist

- [x] Tests pass locally: `cargo test --locked` → 124 passed, 0 failed. The new `message::tests::test_show_msg_html_display` fails without the `show_msg` change (renders `hello <world>` instead of `**hello** <world>`) and passes with it. `check-imports-format.sh` passes. Clippy (1.98) reports nothing in the changed files.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog file
- [x] Documentation is updated (if applicable) — `docs/iamb.5` and `config.example.toml`
```
