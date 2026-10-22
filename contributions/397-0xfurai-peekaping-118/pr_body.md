Closes #118

TCP and DNS monitors built their address with `fmt.Sprintf("%s:%d", ...)`, so an IPv6 host or resolver such as `::1` turned into `::1:53`. Go rejects that with `too many colons in address`. As you suggested in the issue, they now use `net.JoinHostPort`, which writes `[::1]:53`. The places changed:

- `executor/tcp.go`: the dialled address. A host already written in brackets (`[::1]`, which worked before as a workaround and which the web's `formatHostPort` expects) is unwrapped first, so it isn't bracketed twice.
- `executor/dns.go`: the resolver address, computed once and used by the `net.Resolver` dial (A, AAAA, CNAME, MX, NS, PTR, SRV, TXT) and by both `miekg/dns` exchanges (CAA, SOA).

IPv4 addresses and host names come out exactly as before.

Tests (`executor/tcp_test.go`, `executor/dns_test.go`):
- `TestTCPExecutor_Execute_IPv6` and `TestDNSExecutor_Execute_IPv6Resolver` (A and SOA) listen on `[::1]` and expect the monitor to be UP. They skip on a host without IPv6 (new `listenIPv6Loopback` helper in `common_test.go`). `startDNSServer` gained a `startDNSServerOn(addr)` variant for this.
- `TestTCPExecutor_Execute_IPv6AddressIsWellFormed` and `TestDNSExecutor_Execute_IPv6ResolverAddressIsWellFormed` run everywhere. They point at `::1` on a closed port and check the failure isn't `too many colons in address`. The TCP one also tries `[::1]`, which must not become `[[::1]]` ("missing port in address"). On `main` the `::1` cases fail with exactly that message, and with the change all of them pass.

My sandbox has no IPv6 at all, so the two `[::1]` listener tests skipped here and I couldn't watch them pass. They should run on a CI runner with IPv6 loopback. `go test ./internal/modules/healthcheck/...` passes apart from the `Ping` tests, which need ICMP and fail the same way on `main` in my sandbox. `go vet` is clean. A CHANGELOG line is under Unreleased → Fixed.

Not changed: the HTTP proxy address in `http.go`, the SMTP notification provider and the MQTT and Postgres monitors build `host:port` the same way. I left them out to keep this to the issue, and can follow up if you want them.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂
