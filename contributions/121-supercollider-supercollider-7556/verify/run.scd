(
Server.program = "/home/user/work/supercollider/build/server/scsynth/scsynth";
fork {
	var t = TestCoreUGens.new;
	UnitTest.reset; TestCoreUGens.runTest("TestCoreUGens:test_linexp_mixedRateInputs");
	40.wait; "PASSES: %".format(UnitTest.passes.size).postln;
	"FAILURES: %".format(UnitTest.failures.size).postln;
	0.exit;
};
)
