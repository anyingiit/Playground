This adds the two deny-list counterparts to the existing layer constraints, as asked for in #154 and #190:

```java
layeredArchitecture()
        .consideringAllDependencies()
        .layer("Controllers").definedBy("..controller..")
        .layer("Services").definedBy("..service..")
        .layer("Repositories").definedBy("..repository..")
        .whereLayer("Controllers").mayNotAccessLayers("Repositories")
        .whereLayer("Repositories").mayNotBeAccessedByLayers("Controllers");
```

`mayNotAccessLayers(..)` forbids dependencies from the layer to the given layers, and `mayNotBeAccessedByLayers(..)` forbids dependencies from the given layers to the layer. Everything else stays allowed, including dependencies from or to classes outside of any layer.

### Motivation

The allow-list methods (`mayOnlyAccessLayers(..)`, `mayOnlyBeAccessedByLayers(..)`) also forbid dependencies from or to classes that are not part of any layer. So a rule like "controllers must not use repositories directly" can't be written with them unless every class that touches the repositories is put into a layer. That's what #1372 ran into, and #190 describes the "list every other layer" workaround. In #154 the first step was the allow-list `mayOnlyAccessLayers()` (#592), with the deny-list left open in case it is still wanted. #190 and #1372 show it still is. (#154 is still assigned to @GiorgadzeLuka from that first step; I hope it's fine to pick up the remaining part.)

### Implementation

`LayerDependencySpecification` keeps the forbidden layers in their own set. When that set isn't empty, the rule checks that no relevant dependency has its origin (or target) in one of the forbidden layers. It reuses the same `ifDependencyIsRelevant(..)` handling, so the dependency settings and `ignoreDependency(..)` apply as before. Both methods use the same argument checks as the allow-list variants (at least one layer, all layers must exist). They also reject the layer's own name, since forbidding a layer to access itself would flag every dependency inside the layer, while the allow-lists always permit the own layer.

Following the concern in #190 about deny-lists, the Javadoc of both methods points out that the allow-list variants are usually the safer choice, since a deny-list won't catch indirect accesses through other classes.

### Tests

Three new tests in `LayeredArchitectureTest` reuse the `mayonlyaccesslayers` test classes. They check the descriptions and the exact violations: only the direct dependencies between the two layers are reported, and dependencies on `Object` are not, unlike with `mayOnlyAccessLayers(..)`. In the `mayNotBeAccessedByLayers(..)` test, one class accessing the layer is not part of any layer, and its access is not reported. They also check that unknown, missing, or the layer's own names are rejected.

Resolves #154
Resolves #190

### Disclosure

I wrote this with help from an AI coding assistant (Claude Code). I reviewed the change, ran the tests locally, and I'm responsible for it.
