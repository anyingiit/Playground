## Description

Over TCP, `receive()` treated every `Conn.Read` as if it were a UDP datagram. TCP is a byte stream, so a large response (e.g. a big `GetBulk`) can arrive split over several segments, and several responses can arrive in one segment. In the first case the decoder only sees the first segment and fails with `error verifying packet sanity: Got 1448 Expected: 2611`; the remaining bytes are then read as a new message and fail with `invalid packet header`.

This change adds a small `receiveStream()` used when the transport is TCP (and the conn is not a `net.PacketConn`). Following RFC 3430, it reads the outer SEQUENCE tag and BER length first, then `io.ReadFull`s exactly the announced number of bytes. Each call therefore returns one complete message and never consumes bytes of the next one, so no extra buffering state is needed. A clean EOF before a message still returns `io.EOF`, so the existing reconnect logic in `sendOneRequest` keeps working. UDP handling is unchanged.

Tests (in `marshal_test.go`, `marshal` tag):
- `TestSendOneRequest_TCP_SegmentedResponse`: a TCP server returns a ~5.8 KB `GetResponse` in 1000-byte chunks; `Get` must return all 50 varbinds. Without the fix it fails with `error verifying packet sanity: Got 1000 Expected: 5835`.
- `TestReceive_TCP_Framing`: over `net.Pipe`, one message is split across three writes (including inside the header) and two more are coalesced into one write; `receive()` must return the three messages one by one.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to
help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed
below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to
close it, no hard feelings at all 🙂

## Related issue

Closes #591

## Checklist

- [x] Tests pass locally (`go test -tags helper|marshal|misc|api .` all ok; `go test -race -tags marshal -run 'TCP|SendOneRequest' .` ok; `go vet -tags all ./...`, `gofmt -l .` and `make lint` clean; `FuzzUnmarshal` 15 s ok; the two new tests fail without the fix. `end2end`/netsnmp tests need a local snmpd and were not run.)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, recent PRs don't update it; happy to add a `[BUGFIX]` line if wanted
- [ ] Documentation is updated (if applicable) — n/a
