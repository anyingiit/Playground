# 285 tuProlog/2p-kt#1005 — skipped as a duplicate of 433

On 2026-10-22, thread 270–299 built bundle 285 for the same issue (ceiling/1 saturating). Another thread had already pushed bundle 433 at 21:54 UTC, before 285 was committed, so 285 was removed and 433 stays the one to submit.

If 433 is ever dropped, 285's version can be rebuilt from its approach. It used `setScale(0, RoundingMode.CEILING).toBigInteger()` and added `testIsCeilingOfLargeReal` to test-solve TestIs (±1e30, 2.1, -0.5), wired into TestPrologIs and TestProblogIs. An independent review passed it.

Lesson: before starting an issue, grep READY_TO_SUBMIT.md and the contributions/ folder names right before writing code, not only at scouting time. Other threads pick from the same repos.
