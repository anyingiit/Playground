# AUDIT — supabase/terraform-provider-supabase @ 3a95cbe

- `tools/audit_repo.py`: no auto-executing surface, no committed binaries.
  - The only pattern hit is a "secret-paths" false positive, a `tflog.Trace` string in third_party_auth_resource.go.
- The acceptance tests run against gock HTTP mocks (`defaultApiEndpoint` is intercepted).
  - terraform-plugin-testing downloads the terraform CLI from releases.hashicorp.com through hc-install. That is the official HashiCorp source.
  - No Supabase credentials were used and there were no real API calls.
- No Makefile targets were run beyond the equivalent of `TF_ACC=1 go test`.
- AI policy: none found in the repo (CONTRIBUTING is the scaffolding template).
- CLA/DCO: none in the repo.
