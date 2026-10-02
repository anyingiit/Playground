## Description

Adds an optional `enabled` field to `spec.metrics.serviceMonitor`, so users can deploy the metrics exporter without the operator creating a `ServiceMonitor`. This is useful when Prometheus runs outside the cluster and the `ServiceMonitor` CRD is not installed. Today `reconcileMetrics` requeues with "ServiceMonitor CRD not installed in the cluster" and never gets to the exporter.

- `ServiceMonitor.Enabled *bool` (`json:"enabled,omitempty"`). It defaults to `true` when unset, so existing `MariaDB`/`MaxScale` resources keep their current behavior.
- New helpers `ServiceMonitor.IsEnabled()`, `MariaDB.IsServiceMonitorEnabled()` and `MaxScale.IsServiceMonitorEnabled()`.
- `MariaDBReconciler.reconcileMetrics` and `MaxScaleReconciler.reconcileMetrics`: if the ServiceMonitor is disabled, they skip the `ServiceMonitorExist()` discovery check and `reconcileServiceMonitor`. The exporter config, `Deployment` and `Service` are still reconciled as before.
- The `ServiceMonitor` struct is shared by `MariaDB` and `MaxScale`, so the field is in both CRDs, and both controllers honor it.
- `docs/metrics.md` documents the field. The generated files (deepcopy, CRDs, `deploy/crds`, the CRDs helm chart and `docs/api_reference.md`) were regenerated with `make manifests code manifests-crds helm-crds docs-api`. `make crd-size` reports 784 KB.

Note: switching `enabled` from `true` to `false` does not delete a `ServiceMonitor` that was already created. This matches how `metrics.enabled: false` behaves today, and the object is still garbage-collected with its owner. I can add explicit cleanup if you prefer.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #1828

## Checklist

- [x] Tests pass locally
  - New Ginkgo tables: `IsServiceMonitorEnabled` in `api/v1alpha1/mariadb_types_test.go` and `api/v1alpha1/maxscale_types_test.go`, covering metrics unset, metrics disabled, and `serviceMonitor.enabled` unset, `true` and `false`. With the gating reverted, the `serviceMonitor.enabled false` entries fail. With the change, they pass.
  - `make test` (api, pkg, helmtest and webhook suites with envtest 1.36): all 37 suites pass.
  - `golangci-lint run ./...` (v2.13.2): 0 issues. `go build ./...` and `go vet ./api/... ./internal/controller/...` both pass.
  - I did not run the controller integration tests (`make test-int-*`) because they need a KIND cluster.
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (the repo has no changelog file)
- [x] Documentation is updated (if applicable) — `docs/metrics.md`, plus the regenerated `docs/api_reference.md`
