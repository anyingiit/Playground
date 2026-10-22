Fixes #1567.

A method without a comment of its own counts as documented when the method it aliases, or the method it overrides, is documented (`MethodAttr#documented?` follows `is_alias_for` and then `see`). But `Stats#undoc_params` parsed only the method's own, empty comment. So `rdoc -C1` listed every parameter of such a method as undocumented, even when the original documents all of them.

`undoc_params` now takes the comment from the first method with one, following the same `is_alias_for` / `see` chain as `documented?` all the way up, not just one level (the question raised in the review of #1780). That covers aliases of aliases and overrides several classes down. A guard stops the walk if the chain loops back on itself. A method that has its own comment is still checked against that comment.

With the example from the issue (plus an alias of an alias), `rdoc -C1` now reports `Parameters: 8 (0 undocumented)` instead of 6 undocumented, and undocumented overrides of a documented superclass method are no longer flagged either, matching what `rdoc -C` already counts as documented. Only the coverage report changes.
