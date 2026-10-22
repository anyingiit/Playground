Fixes #372.

`NotFoundException` formats its message as `"%s not found!"`, so it expects the name of the missing object. Four places passed a whole sentence instead, and clients got messages like `RuleSet not found not found!`:

| Where | Before | After |
|---|---|---|
| `ConstraintRuleSetService` update and delete | `RuleSet not found not found!` | `RuleSet not found!` |
| `ConstraintRuleSetService#resolveAccessibleVsum` | `VSUM not found not found!` | `Vsum id not found!` |
| `FileStorageService#updateFile` | `File not found not found!` | `File not found!` |
| `METAMODEL_IDS_NOT_FOUND_IN_THIS_VSUM_NOT_FOUND_ERROR` (used by `VsumService`, `MetaModelRelationService` and `VsumBuildInputCollector`) | `MetaModel Ids not found in this VSUM not found!` | `MetaModel Ids in this VSUM not found!` |

The callers now use constants from `messages/Error`, like the other `NotFoundException` callers:

- a new `RULE_SET_NOT_FOUND_ERROR = "RuleSet"`;
- the existing `VSUM_ID_NOT_FOUND_ERROR` and `FILE_ID_NOT_FOUND_ERROR`.

So the VSUM lookup in `ConstraintRuleSetService` now reads the same as every other VSUM lookup. The metamodel constant keeps its name, and only its value changes.

### Tests

The existing not-found tests in `ConstraintRuleSetServiceTest` used `hasMessageContaining`, so they passed with the doubled wording. They now check the exact message. `FileStorageServiceTest` and `VsumBuildInputCollectorTest` gain message checks for the file and metamodel cases. Without the change in `app/src/main`, 5 of these assertions fail, for example `expected: <File not found!> but was: <File not found not found!>`. The controller test's stub now throws `new NotFoundException("RuleSet")`, matching how the service builds it.

`mvn verify -pl app -am` (Spotless and the 487 app tests) passes. I didn't run the CI Checkstyle action locally.

I prepared this with help from an AI coding assistant (Claude Code), reviewed the change myself, and ran the tests above.

Note: #377 renames `USER_DOSE_NOT_HAVE_ACCESS`, which sits next to the imports this adds in `ConstraintRuleSetService`. Whichever PR merges second needs a one-line conflict fix in that import block.
