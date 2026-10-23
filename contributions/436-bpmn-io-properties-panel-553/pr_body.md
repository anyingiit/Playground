### Proposed Changes

Closes #553

As analysed in the issue, the `:disabled` checkbox rule has the same specificity as the `:checked` rule and comes later. It therefore replaces the accent background with the near-white `--input-disabled-background-color`, but keeps the white checkmark `background-image`, so a checked, disabled checkbox looks unchecked.

This adds a dedicated `:checked:disabled` rule, as suggested in the issue:

- A new token, `--checkbox-checked-disabled-background-color`, defaults to `--input-disabled-color` (`--bio-text-subtlest`), a muted grey.
- Checked, disabled checkboxes use this token for their background and border. The checkmark stays white, and the control still reads as disabled rather than as the active accent.
- Unchecked disabled and enabled checkboxes are unchanged.

The checkmark contrast against the background goes from about 1.07:1 to about 3.6:1, which meets the WCAG 3:1 minimum for non-text contrast.

**Try it out:** render `<input class="bio-properties-panel-input" type="checkbox" checked disabled />` inside a `.bio-properties-panel` (for example via `npm run start:styles` and adding `disabled` to the checkbox in the styling spec). The checkmark is now visible on a grey box.

**Tests:** a new spec in `test/spec/styling.spec.js` computes the contrast between the checked, disabled checkbox's background and the white checkmark and requires at least 3:1.

- Without the CSS change, it fails with `expected 1.0706310998416164 to be at least 3`.
- With the change, `npm test` passes (791 passing, 2 skipped).
- `npm run lint` and `npm run lint:theme` also pass.

This change was prepared with AI assistance (Claude Code). I reviewed the diff and ran the tests above myself.

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
