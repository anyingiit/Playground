### Proposed Changes

Related to #65

As discussed in #65, the CLI separates `<diagramFile>` and `<outputConfig>` with `path.delimiter`, because `:` can be part of a path on Windows. The README, however, only shows the `:` form. That is what tripped up the reporter, who asked for at least a note in the docs.

This adds a short note below the usage block. It says that the separator is `:` on Linux and macOS and `;` on Windows, and that `--help` prints the right one. It also shows the Windows form of the first example, quoted, because PowerShell and Bash treat a bare `;` as a command separator.

It does not change the CLI. The proper fix discussed in the issue (separate arguments for input and output) is a breaking change and is left to the maintainers.

**Try it out:** read the new note in `README.md` under _Usage_. On Linux, `node cli.js --help` prints `<diagramFile>:<outputConfig>`, and `require('path').win32.delimiter` is `';'`, so `"C:\x\diagram.bpmn;diagram.png"` splits into the input and output as described.

This change was prepared with AI assistance (Claude Code). I reviewed the diff and checked the behaviour above myself.

### Checklist

Ensure you provide everything we need to review your contribution:

<!--
Do not alter this checklist beyond checking items; provide context above.
-->

* [x] Contribution __meets our [definition of done](https://github.com/bpmn-io/.github/blob/main/resources/DEFINITION_OF_DONE.md)__
* [x] Pull request __establishes context__
  * [x] __Link to related issue(s)__, i.e. `Closes {LINK_TO_ISSUE}` or `Related to {LINK_TO_ISSUE}`
  * [x] __Brief textual description__ of the changes
  * [ ] __Screenshots or short videos__ showing UI/UX changes
  * [x] __Steps to try out__, i.e. [using the `@bpmn-io/sr` tool](https://github.com/bpmn-io/sr)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
