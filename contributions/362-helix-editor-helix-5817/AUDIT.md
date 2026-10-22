# AUDIT: helix-editor/helix @ ba40e54

同 360/361（同一克隆）：build.rs 只拉取/编译语法和读 git 哈希（已用 `HELIX_DISABLE_AUTO_GRAMMAR_BUILD=1` 关闭）；无其它执行面。

额外：用本地 hx 的 `--grammar fetch/build`（XDG_CONFIG_HOME 指向临时目录，`use-grammars = { only = ["ruby"] }`）只拉取并编译了 languages.toml 指定提交的 tree-sitter-ruby（ad907a6），复制到 runtime/grammars/ruby.so 供集成测试使用（被 .gitignore 忽略，不在补丁里）。

结论：安全。
