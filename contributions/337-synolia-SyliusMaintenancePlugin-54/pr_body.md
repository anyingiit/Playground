| Q             | A
| ------------- | ---
| Bug fix?      | yes
| New feature?  | no
| BC breaks?   | no
| Fixed issue | #54

`ChannelChecker` (priority 60) runs before `ProfilerChecker` (30) and `TokenChecker` (20). On a store with several channels, a request whose hostname matches no channel makes `ChannelContextInterface::getChannel()` throw `ChannelNotFoundException`. During maintenance that exception escapes the voter, so `/_profiler` and `/_wdt` return a 500, as described in #54. A maintenance token on such a host can't get through either, because `TokenChecker` is never reached.

Of the two options suggested in the issue, this PR takes the second: `ChannelChecker` catches `ChannelNotFoundException` and returns `ACCESS_DENIED`, so the voter moves on to the remaining checkers. When no channel matches, the plugin can't tell whether the request belongs to a channel in maintenance, so it neither grants access nor fails. Raising `ProfilerChecker`'s priority would also fix the profiler, but not the token case. Requests that do resolve to a channel behave as before.

`tests/PHPUnit/Checker/ChannelCheckerTest.php` is a plain unit test that mocks the channel context. It covers a channel outside maintenance, a channel in maintenance, and no matching channel; without the change, the last case throws `ChannelNotFoundException`. I wrote it as a unit test because the existing functional tests need the full test application and a database, which I couldn't set up. If you'd rather have a case in `MultiChannelMaintenanceTest`, I'm happy to add one.

How I checked it: the new tests pass (3 tests, 3 assertions), and with only `src/` reverted the no-channel case errors out. PHPStan at level `max`, using `ruleset/phpstan.neon`'s ignore list, reports no errors on the changed files. I couldn't run ECS here, so the formatting follows the surrounding code by hand.

**Motivation / disclosure:** I had some spare AI-assistant quota (Claude Code) and am using it to try to help projects with open issues. The change was prepared with Claude Code and verified as described above. If it doesn't fit, isn't up to your bar, or you'd simply rather not take it, please feel free to close it. No hard feelings at all 🙂
