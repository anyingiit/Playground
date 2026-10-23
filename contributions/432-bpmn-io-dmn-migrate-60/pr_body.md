### Proposed Changes

Closes #60

DMN 1.1 references imported types with XML QNames, for example `typeRef="types:Applicant"`. DMN 1.2 and later use a FEEL qualified name built from the import's `name`, for example `types.Applicant` (see DMN12-94). Until now, `migrateDiagram` gave imports a generated name (`Import_…`) and kept the QName, so these type references could not be resolved after migration.

When migrating from 1.1, this change now does the following:

- An import without a `name` takes the namespace prefix declared for its namespace. For example, `xmlns:types="urn:example:types"` gives the import the name `types`.
- Every `typeRef` that uses one of those prefixes becomes `<prefix>.<localName>`. This covers `itemDefinition`, `variable`, `literalExpression`, and any other element with a `typeRef`.
- Imports with no declared prefix keep the existing ID-based name. So do imports whose prefix contains `-` or `.`, because `my-types.Thing` would be ambiguous in FEEL; their type references stay unchanged.
- Other type references, such as `string` or a prefix that does not belong to an import, are left unchanged.

I did not add an explicit error for QNames that cannot be migrated. That follows the discussion in the issue.

This builds on the approach of #61, which was closed because of the CLA; its author invited others to pick it up. Of the two review points raised there, prefixes that are not valid FEEL names are now handled as above. Prefixes are still resolved from the namespace declarations on `<definitions>` only; re-declaring an import prefix on a nested element is not handled.

**Try it out:** migrate `test/fixtures/imported-types.dmn` with `migrateDiagram`. The output declares `<import name="types" …>` and `typeRef="types.Applicant"`. It also validates against the DMN 1.3 XSD (see the new `imports` specs).

**Tests:** the new `imports` specs in `test/spec/migrateDiagramSpec.js`:

- Without the change, the specs for the import name, the migrated type references and the FEEL name guard fail.
- With the change, `npm run all` passes: lint, build, 20 specs, and 2 distro specs.

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
