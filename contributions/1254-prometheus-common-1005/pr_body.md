## Description

@roidelapluie @gotjosh — small fix for #1005.

Since #877 removed the logic that appended the unit to the metric name, `MetricFamilyToOpenMetrics`
(OpenMetrics 0.0.1 / 1.0.0 output) writes the `# UNIT` line verbatim even when the unit is not a
suffix of the metric family name, e.g.

```
# TYPE request_duration gauge
# UNIT request_duration seconds
request_duration 1.5
```

OpenMetrics 1.0 requires the unit to be a suffix of the name, and Prometheus' OpenMetrics parser
rejects such an exposition (`unit "seconds" not a suffix of metric "request_duration"`), so the
whole scrape of the target fails.

This PR follows the first option proposed in the issue: the encoder now writes the `# UNIT` line
only if the unit is a `_<unit>` suffix of the (compliant) metric family name — i.e. after the
`_total` truncation for counters, matching the check in the Prometheus parser. Otherwise the line is
omitted and the samples are written unchanged. This mirrors how counters without a `_total` suffix
are already exposed as `unknown` to avoid invalid output. An empty unit is written as before. The
metric name itself is never changed, and the OpenMetrics 2.0 encoder (where the suffix rule is only a
SHOULD) is untouched. The function's doc comment lists the new behaviour next to the `_total` note.

Tests:
- `TestCreateOpenMetrics` case 16 (`some_measure_total` with unit `seconds`) and `TestEncode` cases
  for OM 0.0.1/1.0.0 (`foo_metric` with unit `seconds`) previously asserted the invalid output; they
  now expect no `# UNIT` line. The OM 2.0 case in `TestEncode` still expects it.
- New cases 18–21: unit not a suffix (the example from the issue), unit glued to the name without
  `_` (`request_durationseconds`), valid suffix on a gauge, and valid suffix on a counter without
  `_total` (exposed as `unknown`).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Fixes #1005

## Checklist

- [x] Tests pass locally: `go test ./expfmt/ ./model/ ./helpers/... ./promslog/... ./route/ ./server/ ./version/` → all ok; `go test ./config/` ok (run without proxy env vars). With the encoder change reverted, `TestCreateOpenMetrics` (cases 16, 18, 19) and `TestEncode` (OM 0.0.1/1.0.0 cases) fail.
- [x] `gofmt -l expfmt` clean, `go vet ./expfmt/` clean, `golangci-lint run ./expfmt/...` (v2.13.1, repo config) → 0 issues
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, the changelog is compiled at release time; happy to add a Bugfixes line if preferred
- [x] Documentation is updated (if applicable) — `MetricFamilyToOpenMetrics` doc comment
