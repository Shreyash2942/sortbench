# Day 1 runtime feasibility spike

Measured at 2026-09-29T17:04:03.575147+00:00.

- Python: 3.14.4 (tags/v3.14.4:23116f9, Apr  7 2026, 14:10:54) [MSC v.1944 64 bit (AMD64)]
- Platform: Windows-11-10.0.26200-SP0
- Processor: AMD64 Family 26 Model 36 Stepping 0, AuthenticAMD
- Input: seeded random integers; seed = 506 + size.
- Method: three trials per size, median elapsed seconds, `perf_counter()`.
- Operation: suffix-minimum scanning with no swaps; **not a full sort**.
- Dataset construction and file output are outside timing.

| Size | Comparisons per trial | Measured median seconds |
|---:|---:|---:|
| 1,000 | 499,500 | 0.007749 |
| 2,000 | 1,999,000 | 0.030656 |
| 4,000 | 7,998,000 | 0.113984 |

## Projection, not a measurement

At 50,000 elements the loop would make 1,249,975,000
comparisons. Scaling the measured 4,000-element median by the exact
comparison-count ratio (156.286) gives **17.814 seconds**.
The 50,000-element case was not executed in this spike.

This estimate assumes the same per-comparison cost. Full algorithms also have
swaps, shifts, recursion, allocation, and input-order effects. These numbers
cannot establish which sorting algorithm is fastest. Background system load
was not controlled, and three short runs do not establish statistical precision.

## Day 1 decision

Retain all required sizes, including 50,000, in the final benchmark. Expect
quadratic cases to take substantially longer than these small cases. Run full
experiments sequentially, save validated results as they finish, and document
any incomplete scenario. Do not substitute this projection for measured data.

Raw measurements: [runtime_spike.csv](../results/runtime_spike.csv).
Reproduce from the repository root with `python scripts/runtime_spike.py`.
