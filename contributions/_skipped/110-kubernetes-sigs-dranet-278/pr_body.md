#### What type of PR is this?

/kind feature

#### What this PR does / why we need it:

## Description

Adds an opt-in, read-only hook that lets a cloud provider validate the network configuration DraNet is about to checkpoint, as proposed in #278.

- `pkg/cloudprovider`: new optional interface, next to `ProfileProvider`:

  ```go
  type NetworkConfigValidator interface {
  	ValidateNetworkConfig(id DeviceIdentifiers, config *apis.NetworkConfig) error
  }
  ```

- `pkg/inventory`: `DB.ValidateNetworkConfig(deviceName, config)` type-asserts the configured `CloudInstance` and calls the validator with the device identifiers. If the provider does not implement the interface, it returns `nil` and nothing changes.
- `pkg/driver`: on the netdev path of `prepareDevice`, the final `NetworkInterfaceConfigInPod` (with the routes, rules and neighbors read from the host) is passed to the validator right before `SetDeviceConfig`. I placed the call before the eBPF unpin step, so a rejected attempt does not touch the host. On error:
  - the device error ends up in `PrepareResult.Err` (`device <dev>: provider rejected the network configuration of interface <if>: <provider error>`), and kubelet retries;
  - nothing is persisted, and the interface stays in the host namespace, because it is only moved later by the NRI hooks;
  - an allocated profile is released by the existing `deviceCommitted` cleanup.
- The IB-only path is unchanged, because it carries no host-derived routing state.

This PR only adds the generic hook. Following the ownership boundary from #42, it adds no host-network restoration, delays or policy-table assumptions. I did not implement a validator for any provider (e.g. OKE) or a webhook capability for it, and I'm happy to leave those to the provider owners. The change is small and only touches `cloud.go` additively, so it should not conflict with #357.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

#### Which issue(s) this PR is related to:

Fixes #278

#### Special notes for your reviewer:

## Checklist

- [x] Tests pass locally
  - New tests: `TestValidateNetworkConfig` (inventory: no provider, provider without the interface, accept, reject, device missing from the inventory) and three `TestPrepareResourceClaim` cases (validator gets the final config; a rejection fails the claim and persists nothing; a rejection releases the allocated profile). They fail without the change and pass with it.
  - `go test -race ./pkg/driver/... ./pkg/inventory/... ./pkg/cloudprovider/...`: the new tests pass. My sandbox kernel cannot create `dummy`/`ipvlan` links, so I ran the `TestPrepareResourceClaim` table locally with `lo` in place of `dummy0`. All 22 cases passed. The netlink-dependent tests that fail in this sandbox fail the same way on `main`.
  - `go build ./...`, `go vet ./...`, `gofmt -l` (clean), `golangci-lint` v2.9.0 `run ./...` (0 issues)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a (release notes come from the release-note block)
- [ ] Documentation is updated (if applicable) — n/a: this adds an in-tree Go interface only, documented in its godoc; `site/content/docs/contributing/webhook-providers.md` is unchanged because no webhook capability is added

#### Does this PR introduce a user-facing change?

```release-note
Cloud providers can now implement the optional `cloudprovider.NetworkConfigValidator` interface to validate the final, host-derived network configuration of a device before it is checkpointed; a validation error fails NodePrepareResources so kubelet retries.
```
