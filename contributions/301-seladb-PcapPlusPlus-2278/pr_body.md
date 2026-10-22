## Description

Adds `serializeLayer()` and `SerializedFields` for `GtpV1Layer` and `GtpV2Layer`, as part of the serialization rollout tracked in #2278 (GtpLayer v1/v2 had no PR listed there yet).

**GtpV1Layer** (after the common `Layer` fields):
- `version`, `protocolType` (1 = GTP, 0 = GTP'), `messageType` (raw integer), `messageTypeName` (`getMessageTypeAsString()`), `messageLength` (host byte order), `teid` (hex)
- `sequenceNumber`, `npduNumber`: only when the corresponding flag is set
- `extensions`: array of header extension types, only when the extension header flag is set

**GtpV2Layer**:
- `messageType` (raw integer from the header, so unknown types keep their value), `messageTypeName` (`GtpV2MessageType::toString()`), `messageLength`, `piggybacking` (bool), `sequenceNumber`
- `teid` (hex) and `messagePriority`: only when their flags are set
- `informationElements`: array of IE types (same style as RADIUS attributes / DHCP options)

Optional fields are omitted when absent, the same way NTP omits `keyID`/`digest`. Field IDs start at `Layer::SerializedFields::MaxID + 1`; array item descriptors use ID 0, as in `RadiusLayer`. Each field has a Doxygen comment covering byte order/format.

**Small fix needed for this:** `GtpV2Layer`'s IE accessors computed the IE area length as `m_Data + getHeaderLen() - getIEBasePtr()`. When a packet's `messageLength` is shorter than the fixed header (e.g. `48 20 00 00 de ad be ef 00 00 01 00`, which passes `isDataValid()`), that subtraction wraps to a huge `size_t` and the TLV reader reads past the layer (AddressSanitizer: heap-buffer-overflow in `GtpV2InformationElement::getDataSize`). This was already reachable through `getFirstInformationElement()` / `getInformationElementCount()`, but serialization would now hit it for every such packet, so the four accessors now go through a small private `getIEDataLen()` helper that clamps the length to 0.

Tests (`Tests/Packet++Test/Tests/GtpTests.cpp`):
- JSON output for every fixture in `GtpV1LayerParsingTest` and `GtpV2LayerParsingTest`: GTP-U with sequence number, GTP-U with a header extension, GTP-U over IPv6 with no optional fields, GTP-C, GTPv2 with TEID and 9 IEs, both messages of the piggyback capture (incl. message priority), the malformed piggyback capture, GTPv2 over TCP and the non-zero CR-flag capture;
- a newly created GTPv1 layer with sequence and N-PDU numbers;
- `all()` size and consecutive IDs for both layers;
- regression test: two headers whose message length is shorter than the fixed header yield no IEs and `"informationElements":[]`.

Without the serialization change both parsing tests fail (the inherited `Layer::serializeLayer` writes only the common fields). Without the `getIEDataLen()` clamp, the regression test reports a heap-buffer-overflow under AddressSanitizer.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

## Related issue

Part of #2278 (GtpLayer v1/v2)

## Checklist

- [x] Tests pass locally on Linux (GCC 13): `Packet++Test -t gtp` → 6/6 passed; full `Packet++Test` → 280/280 passed. Built with `-DPCAPPP_BUILD_PCAPPP=OFF -DPCAPPP_USE_PCAP=OFF -DPCAPPP_BUILD_EXAMPLES=OFF` since libpcap isn't available in my environment, so Pcap++Test and examples were not run (this change only touches Packet++).
- [x] Formatted with clang-format 19.1.6 (`clang-format -i -style=file` on the changed files)
- [ ] `cppcheck` pre-commit hook not run locally (not installed)
- [x] New public API documented with Doxygen
