## Description

Adds `serializeLayer()` and `SerializedFields` for the QUIC v1 layers, as part of the serialization rollout tracked in #2278 (QuicLayer had no PR listed there yet).

The fields follow the class hierarchy, each level calling its parent's `serializeLayer()` and continuing its field IDs (same scheme as `GreLayer` / `GREv0Layer`, with a `MaxID` on every struct):

| Class | Fields |
|---|---|
| `QuicV1Layer` | `packetType` (same names as `toString()`: `Initial`, `0-RTT`, `Handshake`, `Retry`, `Version Negotiation`, `1-RTT`), `headerForm` (`Long`/`Short`), `fixedBit` |
| `QuicV1LongHeaderLayer` | `version` (hex), `destinationConnectionId`, `sourceConnectionId` (hex strings) |
| `QuicV1EstablishmentLayer` (Initial, 0-RTT, Handshake) | `payloadLength` (the Length field; named so it doesn't clash with the common `length`) |
| `QuicV1InitialLayer` | `token` (hex string) |
| `QuicV1RetryLayer` | `retryToken`, `retryIntegrityTag` (hex strings) |
| `QuicV1VersionNegotiationLayer` | `supportedVersions` (array of hex values) |
| `QuicV1OneRttLayer` | `spinBit`, `keyPhaseBit` (booleans) |

The packet-type names are moved from `toString()` into a small static helper so both use the same strings; `toString()` output is unchanged. Everything is read through the existing getters, which already return empty values for truncated packets.

Tests (`Tests/Packet++Test/Tests/QuicTests.cpp`): JSON output for each packet type in `QuicV1ParsingTest` (Initial, Handshake, 0-RTT, Retry, Version Negotiation, 1-RTT), and `all()` size plus gap-free IDs for all nine classes. Without the source change the parsing test fails (only the common fields are written).

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Part of #2278 (QuicLayer)

## Checklist

- [x] Tests pass locally on Linux (GCC 13): `Packet++Test -t quic` → 2/2 passed; full `Packet++Test` → 280/280 passed. Built with `-DPCAPPP_BUILD_PCAPPP=OFF -DPCAPPP_USE_PCAP=OFF -DPCAPPP_BUILD_EXAMPLES=OFF` (no libpcap in my environment), so Pcap++Test and examples were not run (this change only touches Packet++)
- [x] Formatted with clang-format 19.1.6
- [ ] `cppcheck` pre-commit hook not run locally (not installed)
- [x] New public API documented with Doxygen
