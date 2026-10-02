## Description

Part of the Cucumber-JVM 8.0.0 work tracked in #63: the "Removed modules" item.

Cucumber-JVM 8.0.0 dropped the `javax` based `cucumber-openejb` and `cucumber-cdi2` modules, and `cucumber-deltaspike` with no replacement. This adds a declarative `org.openrewrite.cucumber.jvm.ReplaceRemovedCucumber8Modules` recipe that:

- swaps `io.cucumber:cucumber-openejb` for `io.cucumber:cucumber-jakarta-openejb`, and `io.cucumber:cucumber-cdi2` for `io.cucumber:cucumber-jakarta-cdi`, through `ChangeDependency`;
- points a `cucumber.object-factory` property that names the old object factory at the new one (`io.cucumber.cdi2.Cdi2Factory` → `io.cucumber.jakarta.cdi.CdiJakartaFactory`, `io.cucumber.openejb.OpenEJBObjectFactory` → `io.cucumber.jakarta.openejb.OpenEJBObjectFactory`; I checked the class names against the `META-INF/services` entries of the published jars);
- flags `cucumber-deltaspike` with `DependencyInsight`, since there is nothing to migrate it to.

Notes for review:

- The dependency version is kept rather than set. The idea is that a future `UpgradeCucumber8x` runs this recipe and then bumps `io.cucumber:*` to `8.x`, so the Cucumber modules stay aligned. `cucumber-jakarta-cdi` has been published since 6.1.0, but `cucumber-jakarta-openejb` only since 7.5.0. If you'd prefer `newVersion: 8.x` on the swaps, I'm happy to change it.
- I didn't add it to any composite, because `UpgradeCucumber8x` doesn't exist yet and it doesn't belong in `UpgradeCucumber7x`.
- The `javax.*` → `jakarta.*` migration of user code (CDI beans and so on) is left to the existing Jakarta EE recipes in rewrite-migrate-java.
- I added the `recipes.csv` row by hand, using the column layout of the existing rows. Running `recipeCsvGenerate` locally also re-quoted every other row and added a data-tables column.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Part of #63

## Checklist

- [x] Tests pass locally: `./gradlew test --tests '*ReplaceRemovedCucumber8ModulesTest'` → 4/4 pass (all 4 fail before the recipe is added). `./gradlew check` → `license` and `recipeCsvValidate` pass. 135 tests ran and 6 failed, all in `CucumberJava8ToCucumberJavaTest$StepMigration`. The same 6 fail on unmodified `main` in my environment, which has no Code Genome credentials, so it builds against an older rewrite release from Maven Central.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, the recipe description and `recipes.csv` row are the docs
