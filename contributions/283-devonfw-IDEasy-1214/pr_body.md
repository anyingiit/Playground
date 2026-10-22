### This PR fixes #1214

As @quando632 analysed in the issue, the only place in `upgrade-settings` that changes the line endings is `UpgradeSettingsCommandlet.updateRepositoryPropertiesFile`: it rewrote the updated `settings/repositories/*.properties` files with `Files.write`, which always uses the platform line separator. On Windows an LF file became CRLF (and on Linux/macOS a CRLF file became LF), so the settings git repository showed unwanted diffs. This PR follows the narrowed scope suggested there.

### Implemented changes:

* `updateRepositoryPropertiesFile` now reads the file as a string, detects whether it uses CRLF or LF, and writes the updated lines back with the same line separator. A missing final newline now stays missing (before, `Files.write` always appended one).
* Added `UpgradeSettingsCommandletTest.testUpdateRepositoryPropertiesPreservesLineEndings`, which creates a CRLF and an LF legacy repository properties file (created in the test, since `.gitattributes` normalizes committed files to LF) and checks the exact content after the upgrade.
* Added the issue to `CHANGELOG.adoc`.

---

### Testing instructions

1. Run `mvn -Dtest=UpgradeSettingsCommandletTest test` in the `cli` folder. The new test fails without the change in `UpgradeSettingsCommandlet` (the CRLF file is written back with LF on Linux/macOS) and passes with it.
2. Manually: in a project whose `settings/repositories` (or legacy `settings/projects`) contains a `*.properties` file with CRLF line endings and a legacy entry such as `eclipse=import`, run `ide upgrade-settings`. The entry is migrated to `import=eclipse` and `git diff` in the settings folder shows only that line change, not a change of every line.

---

### Checklist for this PR

Make sure everything is checked before merging this PR. For further info please also see
our [DoD](https://github.com/devonfw/IDEasy/blob/main/documentation/contributing/DoD.adoc).

- [x] When running `mvn clean test` locally all tests pass and build is successful (in `cli`; locally `NetworkProxyTest` and one `GlobalToolCommandletTest` case fail on `main` as well because of my environment's proxy settings, unrelated to this change)
- [x] PR title is of the form `#«issue-id»: «brief summary»` (e.g. `#921: fixed setup.bat` and not `feature/921 fixed setup.bat`).
  If no issue ID exists, title only.
- [x] PR top-level comment summarizes what has been done and contains link to addressed issue(s)
- [ ] PR and issue(s) have suitable labels
- [ ] Issue is set to `In Progress` and assigned to you *or* there is no issue (might happen for very small PRs)
- [x] You followed all [coding conventions](https://github.com/devonfw/IDEasy/blob/main/documentation/contributing/coding-conventions.adoc)
- [x] You have added the issue implemented by your PR in [CHANGELOG.adoc](https://github.com/devonfw/IDEasy/blob/main/CHANGELOG.adoc) unless issue is labelled
  with `internal`
- [x] You have not changed any dependency in `pom.xml` files or otherwise if runtime dependencies changed,
  you have updated our [LICENSE.adoc](https://github.com/devonfw/IDEasy/blob/main/documentation/LICENSE.adoc)
- [x] You have formulated clear instructions on how to test your contribution under "Testing instructions"

### Checklist for tool commandlets

Have you added a new `«tool»` as commandlet? There are the following additional checks:

- [ ] The tool can be installed automatically (during setup via settings) or via the commandlet call
- [ ] The tool is isolated in its IDEasy project, see [Sandbox Principle](https://github.com/devonfw/IDEasy/blob/main/documentation/sandbox.adoc)
- [ ] The new tool is added to the table of tools in [LICENSE.asciidoc](https://github.com/devonfw/IDEasy/blob/main/documentation/LICENSE.adoc)
- [ ] The new commandlet is a [command-wrapper](https://github.com/devonfw/IDEasy/blob/main/documentation/cli.adoc#command-wrapper) for `«tool»`
- [ ] Proper help texts for all supported languages are added [here](https://github.com/devonfw/IDEasy/tree/main/cli/src/main/resources/nls)
- [ ] The new commandlet installs potential dependencies automatically
- [ ] The variables `«TOOL»_VERSION` and `«TOOL»_EDITION` are honored by your commandlet
- [ ] The new commandlet is tested on all platforms it is available for or tested on all platforms that are in scope of the linked issue

### Checklist for GUI contributions

Did you make user-facing changes to the GUI? There are the following additional checks:

- [ ] You followed the [ui-contribution-process.adoc](https://github.com/devonfw/IDEasy/blob/main/documentation/contributing/ui-contribution-process.adoc) and [ui-structure.adoc](https://github.com/devonfw/IDEasy/blob/main/documentation/contributing/ui-structure.adoc)
- [ ] The UI changes are designed in the Figma project and the design was approved in the team review
- [ ] You have added screenshots of the UI changes to the PR description
