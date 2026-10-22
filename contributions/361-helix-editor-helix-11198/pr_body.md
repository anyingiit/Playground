## Description

Adds [sqls](https://github.com/sqls-server/sqls) as the default language server for `sql`, in the `[language-server]` table:

```toml
sqls = { command = "sqls" }
```

plus `language-servers = [ "sqls" ]` on the `sql` language and the regenerated `lang-support.md` row (`cargo xtask docgen`). sqls speaks LSP over stdio with no arguments (same as nvim-lspconfig's `sqls` config).

#11198 was blocked on sqls-server/sqls#175: older sqls sent keyword completions with `"documentation": {"kind": "", "value": ""}`, which isn't a valid `MarkupKind`, so Helix couldn't deserialize the completion response. That was fixed in sqls-server/sqls#176 (Dec 2025) and is in the current release (v0.2.48). Checked against both versions with the same `SEL` completion request:

- v0.2.27: `{"label":"SELECT","kind":14,"detail":"keyword","documentation":{"kind":"","value":""},...}`; `serde_json::from_str::<helix_lsp_types::CompletionItem>` fails with "data did not match any variant of untagged enum Documentation"
- v0.2.48: `{"label":"SELECT","kind":14,"detail":"keyword","sortText":"9999SELECT"}`; deserializes fine

Without a database connection sqls still offers keyword completion and formatting (it shows a one-time `no database connection` info message on startup); connections are configured in sqls' own config file (`$XDG_CONFIG_HOME/sqls/config.yml`, by default `~/.config/sqls/config.yml`).

Install: `go install github.com/sqls-server/sqls@latest`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all.

## Related issue

Closes #11198

## Checklist

- [x] `cargo xtask docgen` regenerated `lang-support.md` (only the sql row changes)
- [x] `hx --health sql` with sqls v0.2.48 on `PATH` → `✓ sqls`
- [x] Ran sqls v0.2.48 over stdio with no config against a `.sql` file: `initialize` succeeds and completion returns valid items (the v0.2.27 output above is the one that broke Helix)
