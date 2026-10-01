## Description

Part of the Cucumber-JVM 8.0.0 recipes in #63: the "`AbstractTestNGCucumberTests.scenarios()` is now `scenarios(ITestContext)`" item.

Cucumber-JVM 8.0.0 changed the TestNG `@DataProvider` on `AbstractTestNGCucumberTests` from `scenarios()` to `scenarios(ITestContext)`. Runners that override `scenarios()` (the usual way to get `@DataProvider(parallel = true)`) then no longer override anything: `@Override` fails to compile, and without it TestNG sees two `scenarios` data providers.

The new `AddTestContextToScenarios` recipe:

- matches method declarations that override `io.cucumber.testng.AbstractTestNGCucumberTests scenarios()`, directly or through an intermediate base class;
- adds an `ITestContext context` parameter (`testContext` if the body already declares a `context` variable) and imports `org.testng.ITestContext`;
- passes that parameter on to `super.scenarios()`, if the override calls it.

Unrelated `scenarios()` methods and runners that don't override it are left alone.

Notes for review:

- The recipe is standalone and not added to any composite yet. It shouldn't go into `UpgradeCucumber7x`: on 7.x the new signature would just add an overload. I'd expect it to be chained into the upcoming `UpgradeCucumber8x`. Happy to wire it in here instead if you prefer.
- The `ITestContext` parameter is templated against a one-line `dependsOn` stub. That way the recipe artifact doesn't have to ship a TestNG type table. If you'd rather use `parserClasspath("org.testng:testng:7.+")` with `classpathFromResources`, I can switch it.
- For the tests, `org.testng:testng:7.+` is added to `testParserClasspath` (for `@DataProvider` / `ITestContext`) and the test type table is regenerated with `createTestTypeTable`. That regeneration also picked up the current 7.34.9 / junit-jupiter 6.1.3 / cucumber-expressions 20.1.0 releases. The `datatable` entry left the test table, since it is now a `parserClasspath` dependency.
- `recipes.csv` gets the new row.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Part of #63

## Checklist

- [x] Tests pass locally: `./gradlew test --tests '*AddTestContextToScenariosTest'` passes 6/6. Before the fix, the 4 rewrite cases fail with "Recipe was expected to make a change". `./gradlew check` runs 137 tests, and the only failures are 6 `CucumberJava8ToCucumberJavaTest$StepMigration` cases. Those fail identically on `main` in my environment because it only resolves an older rewrite (8.90.4) from Maven Central (no Code Genome credentials). `license` and `recipeCsvValidate` pass.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, no changelog in this repo
- [ ] Documentation is updated (if applicable) — n/a, the recipe documents itself via `displayName` / `description` and `recipes.csv`
