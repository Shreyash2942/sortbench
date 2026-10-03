# Day 5 performance observations

All 64 required scenarios completed and passed the independent persisted-result
audit. This is the Day 5 evidence and initial comparison, not the final Day 6
charts, recommendation engine, or 2-3 page performance analysis.

## Evidence and conditions

- Primary data: [benchmark_results.csv](../results/benchmark_results.csv).
- Environment/status: [metadata](../results/benchmark_results.metadata.json).
- Integrity checks and hashes: [validation_report.json](../results/validation_report.json).
- Group winners: [scenario_winners.csv](../results/scenario_winners.csv).
- Attempt review: [run_review.json](../results/run_review.json).
- Python 3.14.4 on Windows 11; processor identifier is recorded in metadata.
- Default seeds 1506, 5506, 10506, and 50506; four algorithms, four input
  orderings, and sizes 1,000, 5,000, 10,000, and 50,000.
- Sequential fixed order, one recorded trial per scenario. Generation, copying,
  validation, and output are outside the timed call. Internal sorter allocation
  is included. Every result was checked against the independently sorted original.
- The full repeat took 396.21 seconds wall time and 393.31 seconds process CPU
  time; recorded sorting calls sum to 396.04 seconds. This is approximately
  6 minutes 36 seconds, with no comparable large pause in the repeat.
- Work ran in a normal desktop environment with lightweight progress checks,
  not an isolated benchmark machine. CPU frequency, background scheduling,
  fixed order, and short measurement durations can affect timings.

The run occurred on October 2, 2026 local time; its metadata timestamps are UTC
(October 3). No final-result rows are missing or replaced by projections.

## Suspect initial attempt and complete repeat

The initial attempt also completed 64 validated sorts, but reverse-sorted Bubble
Sort at 50,000 recorded 3,927.573 seconds. Shortly after that case, the process
had used only about 380 seconds of total CPU time. This suggests a substantial
pause or suspension/scheduling gap; the exact cause was not confirmed.

The original CSV and metadata are retained unchanged in
[initial_run/benchmark_results.csv](../results/initial_run/benchmark_results.csv)
and [its metadata](../results/initial_run/benchmark_results.metadata.json).
They are excluded from timing conclusions. The entire comparison matrix was
repeated using the same algorithms, inputs, and ordering. Windows received a
temporary stay-awake request for the repeat; it was released afterward without
changing saved power settings. The primary dataset is that full repeat, not a
mixture of whichever individual timings looked best. No averages across
attempts are calculated. The suspect case took 79.516 seconds in the repeat.

## Primary measurements

All times below are seconds, rounded for display; the CSV retains the recorded
precision. Each row compares four algorithms for the same size and ordering.

| Dataset | Size | Bubble (s) | Selection (s) | Insertion (s) | Merge (s) | Fastest observed |
|---|---:|---:|---:|---:|---:|---|
| random | 1,000 | 0.0200816001 | 0.0090734 | 0.00936879998 | 0.000968499982 | Merge Sort |
| random | 5,000 | 0.5022723 | 0.2112194 | 0.2222659 | 0.00557719998 | Merge Sort |
| random | 10,000 | 5.0826998 | 2.0534055 | 1.6178932 | 0.0118036 | Merge Sort |
| random | 50,000 | 61.1791862 | 23.6448514 | 27.0068737 | 0.0731335 | Merge Sort |
| sorted | 1,000 | 2.60000234e-05 | 0.00942260004 | 4.70000086e-05 | 0.000829200028 | Bubble Sort |
| sorted | 5,000 | 0.000123800011 | 0.2054049 | 0.000216900022 | 0.00495859998 | Bubble Sort |
| sorted | 10,000 | 0.000688600005 | 1.4292428 | 0.000465199992 | 0.0117053 | Insertion Sort |
| sorted | 50,000 | 0.00127290003 | 29.2820558 | 0.00259529997 | 0.0694641 | Bubble Sort |
| reverse_sorted | 1,000 | 0.0257541 | 0.00927820004 | 0.0185465 | 0.000830799981 | Merge Sort |
| reverse_sorted | 5,000 | 0.6573185 | 0.2248567 | 0.4481109 | 0.00502879999 | Merge Sort |
| reverse_sorted | 10,000 | 3.6950638 | 1.4034784 | 2.2991532 | 0.0111588 | Merge Sort |
| reverse_sorted | 50,000 | 79.5162674 | 28.0274392 | 52.9517419 | 0.0631464 | Merge Sort |
| partially_sorted | 1,000 | 0.0124068 | 0.00897239998 | 0.00122070004 | 0.000888599956 | Merge Sort |
| partially_sorted | 5,000 | 0.4450339 | 0.4565956 | 0.0467901 | 0.0117023 | Merge Sort |
| partially_sorted | 10,000 | 1.4837731 | 0.9168046 | 0.1248626 | 0.0113740001 | Merge Sort |
| partially_sorted | 50,000 | 40.892852 | 26.2688121 | 3.2474878 | 0.081903 | Merge Sort |

## Initial comparisons

- Merge Sort was fastest in all 12 random, reverse-sorted, and partially sorted
  groups. On 50,000 random values it took 0.0731 seconds, compared with 61.18
  seconds for Bubble Sort, 23.64 for Selection Sort, and 27.01 for Insertion Sort.
- Sorted input favored the adaptive algorithms: Bubble Sort won 3 size groups
  and Insertion Sort won the 10,000-element group in this primary run. At 50,000,
  Bubble took 0.00127 seconds and Insertion 0.00260, versus Merge's 0.06946.
- Insertion Sort benefited from partial ordering: at 50,000 it took 3.247 seconds,
  compared with 27.007 on random data and 52.952 on reversed data. Merge was still
  faster on the partially sorted dataset at 0.08190 seconds.
- Selection Sort took 23.64-29.28 seconds across all four 50,000-element orderings;
  already sorted input did not remove its suffix scans.
- Growth with size was much steeper for quadratic sorts: random-data Bubble
  increased from 0.0201 seconds at 1,000 to 61.18 at 50,000, while Merge increased
  from 0.000969 to 0.0731. Exact ratios are descriptive, not fitted complexity
  estimates or confidence claims.

## Diagnostic check and limits of one-trial rankings

The primary sorted 10,000-element winner differed from the neighboring sizes,
and Merge's partially sorted time at 5,000 (0.0117023 seconds) slightly exceeded
its 10,000 time (0.011374). To investigate, all algorithms and dataset types at
both sizes were rerun as a separate 32-scenario comparison set. See
[diagnostic CSV](../results/diagnostic_5000_10000.csv) and
[metadata](../results/diagnostic_5000_10000.metadata.json).

In the diagnostic sorted 10,000 case, Bubble took 0.0004349 seconds and Insertion
0.0004361: Bubble won by only about 1.2 microseconds, reversing the primary
ranking. That is weak evidence for a meaningful advantage. In the diagnostic
partially sorted cases, Merge took 0.0055908 seconds at 5,000 and 0.0199814 at
10,000, restoring increasing times but also showing run-to-run variability.
The diagnostic took 17.08 seconds wall time and 16.91 CPU seconds.

All diagnostic results passed runtime correctness checks; none were substituted
into or averaged with the primary measurements. The tables report fastest
observed algorithms, not universal recommendations. One trial per scenario
cannot establish timing variance, confidence intervals, or a stable winner for
nearly tied short runs. Day 6 should preserve this distinction in charts and
recommendations. Further statistical experiments can be added in a later phase.
