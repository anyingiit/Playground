// Standalone harness for supercollider#7556 (not part of the patch).
#include "../supercollider/server/plugins/LFUGens.cpp"
#include <cmath>
#include <cstdio>
#include <vector>

static const int N = 64;
static const char* rateName(int r) { return r == calc_FullRate ? "ar" : (r == calc_BufRate ? "kr" : "ir"); }

int main() {
    const int rates[3] = { calc_ScalarRate, calc_BufRate, calc_FullRate };
    const float base[5] = { 0.f, -1.0f, 1.0f, 1.0f, 2.0f }; // in(ignored), srclo, srchi, dstlo, dsthi
    int failures = 0, combos = 0;
    for (int code = 0; code < 81; ++code) {
        int r[5];
        r[0] = calc_FullRate;
        int c = code;
        for (int i = 1; i < 5; ++i) { r[i] = rates[c % 3]; c /= 3; }
        // buffers: N valid samples + poison tail; non-audio inputs only have element 0 valid
        std::vector<std::vector<float>> bufs(5, std::vector<float>(4 * N, NAN));
        for (int i = 0; i < 5; ++i) {
            int len = (r[i] == calc_FullRate) ? N : 1;
            for (int s = 0; s < len; ++s) {
                if (i == 0) bufs[i][s] = -1.f + 2.f * s / (N - 1); // ramp over [-1,1]
                else bufs[i][s] = base[i] + (r[i] == calc_FullRate ? 0.001f * s : 0.f);
            }
        }
        if (r[0] == calc_FullRate) bufs[0][0] = 0.5f; // issue value for first sample
        std::vector<float> out(N, 0.f);
        Wire wires[5];
        Wire* wptr[5];
        float* inbuf[5];
        for (int i = 0; i < 5; ++i) {
            wires[i] = Wire();
            wires[i].mCalcRate = r[i];
            wires[i].mBuffer = bufs[i].data();
            wptr[i] = &wires[i];
            inbuf[i] = bufs[i].data();
        }
        float* outbuf[1] = { out.data() };
        LinExp unitStorage;
        memset(&unitStorage, 0, sizeof(unitStorage));
        LinExp* unit = &unitStorage;
        unit->mNumInputs = 5;
        unit->mNumOutputs = 1;
        unit->mCalcRate = calc_FullRate;
        unit->mInput = wptr;
        unit->mInBuf = inbuf;
        unit->mOutBuf = outbuf;
        unit->mBufLength = N;
        LinExp_Ctor(unit);
        (unit->mCalcFunc)(unit, N);
        ++combos;
        int bad = -1;
        double got = 0, want = 0;
        for (int s = 0; s < N; ++s) {
            auto v = [&](int i) { return (double)bufs[i][r[i] == calc_FullRate ? s : 0]; };
            want = v(3) * std::pow(v(4) / v(3), (v(0) - v(1)) / (v(2) - v(1)));
            got = out[s];
            if (!(std::fabs(got - want) <= 1e-4 * std::fabs(want))) { bad = s; break; }
        }
        if (bad >= 0) {
            ++failures;
            printf("FAIL srclo=%s srchi=%s dstlo=%s dsthi=%s sample %d: got %g want %g\n", rateName(r[1]),
                   rateName(r[2]), rateName(r[3]), rateName(r[4]), bad, got, want);
        }
    }
    // the exact case from the issue: LinExp.ar(DC.ar(0.5), -1, 1, 1, DC.ar(2)) -> 1.6817928
    printf("%d/%d rate combinations wrong\n", failures, combos);
    return failures ? 1 : 0;
}
