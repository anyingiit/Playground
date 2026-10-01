## Description

Values files passed through a test suite's `values:` list (and through the `--values` CLI flag) were parsed with the strict `yaml.v3` decoder, which rejects duplicated mapping keys (`mapping key "some-key" already defined at line M`). Helm itself parses values with `sigs.k8s.io/yaml`, which accepts such files and lets the last occurrence win, so a chart that renders fine with `helm template` could not be unit-tested.

This adds `common.YmlUnmarshalValues`, which unmarshals the document into a `yaml.v3` node tree, keeps only the last occurrence of each duplicated mapping key (recursively, using the same key comparison as yaml.v3's duplicate check) and then decodes the cleaned tree. It is used only for user values files in `TestJob.getUserValues` and `TestRunner` values loading; test suite files, snapshots, etc. keep the strict parser. Number types and other decoding behaviour stay unchanged, because decoding still goes through yaml.v3.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #848

## Checklist

- [x] Tests pass locally: new `TestV4RunJobWithValuesFileContainingDuplicateKeys` fails on `main` (`mapping key "nameOverride" already defined at line 1`) and passes with the fix; new unit tests for `YmlUnmarshalValues` in `internal/common`. `gofmt -l -s .` is clean, `go vet` passes, and `go test ./...` passes except `TestV4RunnerOkWithPostRenderer` / `TestV3RunnerWith_Fixture_Chart_PostRenderer`, which fail identically on `main` in my environment (only the Python `yq` is installed there, not mikefarah/yq)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, left for the release notes
- [ ] Documentation is updated (if applicable) — n/a, behaviour now simply matches Helm
