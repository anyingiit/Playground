## Description

A client may pipeline the chunk right after the `BDAT` command without waiting for the reply (RFC 3030 §2), so the server has to consume the chunk even when it rejects the command. Previously `handleBdat` returned early on "Missing RCPT TO", an unknown second argument or too many arguments without reading the chunk, so its bytes were then parsed as SMTP commands.

The size argument is now parsed first. Once it's known, every rejection path reads and drops the chunk through a small `discardChunk` helper before writing the error reply. If the size itself is missing or malformed, the chunk length is unknown and nothing can be discarded, so those cases behave as before. The helper also turns off the line limit while discarding. As a result, the existing `MaxMessageBytes` path no longer trips over long lines in a chunk that is being dropped.

The regression test `TestServer_Chunking_rejectedChunkDiscarded` covers the two cases from the issue (no MAIL FROM, and MAIL FROM without RCPT TO) plus a bad argument and too many arguments. In each case the chunk is `QUIT\r\n`, and a following `NOOP` must still get `250`. Without the fix, all four subtests fail with `221 Bye`.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open good-first-issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it — please feel free to close it, no hard feelings at all 🙂

## Related issue

Closes #315

## Checklist

- [x] Tests pass locally (`gofmt -l .` → clean, `go vet .` → ok, `go test ./...` → ok; new test fails on master, passes with the fix)
- [ ] `CHANGELOG.md` is updated (if applicable) — n/a, repo has no changelog
- [ ] Documentation is updated (if applicable) — n/a, internal protocol behavior
