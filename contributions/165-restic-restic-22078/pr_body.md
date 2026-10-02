What does this PR change? What problem does it solve?
-----------------------------------------------------

Fixes the race described in #22078: when the sftp session fails to start (e.g. `ssh: connect to host ... Connection refused`), restic sometimes exits without printing ssh's error line, mostly on loaded hosts.

Root cause (two parts, matching the reporter's Build A / Build B analysis):

1. `startClient` copies ssh's stderr from a goroutine that nothing waits for. When `sftp.NewClientPipe` fails, the error is returned right away and restic may exit before that goroutine has logged anything.
2. The stderr reader came from `cmd.StderrPipe()`, which `cmd.Wait()` closes as soon as the process exits, so output that was still unread could be dropped.

Change in `internal/backend/sftp/sftp.go`:

- stderr now goes through an `os.Pipe()` (`cmd.Stderr = w`). `cmd.Wait()` does not close it, so the reader always drains everything up to EOF. The parent closes its copy of the write end right after start, so EOF arrives when ssh exits.
- The reader goroutine closes a `stderrDone` channel. If `NewClientPipe` fails, `startClient` waits for that channel before returning, bounded by the existing `closeTimeout` (2s). The bound means a child that keeps stderr open, or a session that fails while the process is still running, can't hang restic.

I didn't make the `cmd.Wait()` goroutine block on stderr. That avoids a possible hang in `Close()` if a grandchild process (e.g. a backgrounded ControlMaster) inherits stderr.

A regression test, `TestOpenFailurePrintsStderr`, uses `sftp.command` to run a `sh` command. The command closes stdout, so the session fails immediately, and then prints an error to stderr after 0.5s. Without the fix, `Open` returns before the line is logged.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as listed below. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it, no hard feelings at all 🙂

Was the change previously discussed in an issue or on the forum?
----------------------------------------------------------------

Closes #22078

Checklist
---------

- [x] I have added tests for all code changes, see [writing tests](https://restic.readthedocs.io/en/stable/090_participating.html#writing-tests)
  - `go test -count=1 -v ./internal/backend/sftp/`: all pass, including `TestBackendSFTP` against a local `sftp-server` and the new `TestOpenFailurePrintsStderr`. The new test fails without the fix (`stderr of the command was not logged before Open returned, got []`).
  - `go test -race -count=10 -run TestOpenFailurePrintsStderr ./internal/backend/sftp/`: ok
  - `golangci-lint run ./internal/backend/sftp/...`: 0 issues; `go vet` and `gofmt -l` are clean
  - Manual repro from the issue (`restic -r sftp://127.0.0.1:2222//tmp/nope cat config`, 100 runs with 6 busy-loop CPU hogs on 4 cores): before 85/100 runs printed ssh's line, after 100/100
- [ ] I have added documentation for relevant changes (in the manual): n/a, no user-facing option changed
- [x] There's a new file in `changelog/unreleased/` that describes the changes for our users (`changelog/unreleased/issue-22078`)
- [x] I'm done! This pull request is ready for review.
