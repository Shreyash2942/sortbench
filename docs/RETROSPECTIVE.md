# SortBench retrospective

## Outcome

The seven-day implementation produced four sorting algorithms, four seeded
dataset generators, a sequential benchmark runner, 64 primary measurements,
six charts, measured recommendations, and a three-page performance report.
The release candidate passes 363 tests in a clean Python 3.14.4 environment.
GitHub release publication is tracked separately in [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md).

## What worked

Separating algorithms, data generation, timing, persistence, and analysis made
each stage reviewable. The common in-place list contract enabled shared tests.
Exhaustive small-input checks, seeded cases, stability checks, and an independent
sorting oracle established correctness before expensive measurements began.
Using independent copies of equal seeded multisets made ordering comparisons
fairer. Focused Git commits preserved the progression from planning to evidence.

Keeping timing boundaries explicit prevented dataset generation and file output
from entering the measurements. The runner's correctness checks and saved
metadata complemented the later file audit: neither was treated as a substitute
for the other. Charts and recommendations use the same audited primary data.

## Difficulties and changes from the plan

The first full experiment contained a 3,927.57-second reverse-sorted Bubble
measurement and a substantial wall-time/CPU-time discrepancy. A long pause is
suspected, but its cause was never confirmed. The response was to retain the
original attempt and repeat the entire matrix with a temporary system-awake
request. The complete repeat became primary; individual fast rows were not
selected across attempts. Additional diagnostics remained separate.

Those diagnostics changed the sorted 10,000-element Bubble/Insertion ranking,
demonstrating why one short timing cannot establish a stable advantage. The
original recommendation ideas were therefore revised around observed results:
Merge won every random, reverse-sorted, and partially sorted group, including
the smallest measured size. No claim is made about arrays below 1,000 elements.

Day 7 review expanded source-file collision protection from selected analysis
tables to every generated filename, including provenance and charts. Regression
tests cover this without running expensive benchmarks. Dependency versions were
recorded and installed in a fresh environment to verify setup independently of
the working environment. A small formatter creates the required three-page PDF
from the Markdown report using the existing plotting dependency.

## Lessons and next steps

Correct output, complete coverage, credible timings, and clear conclusions are
different checks. Recording raw evidence and limitations made anomalies visible
and prevented accidental overstatement. Returning the same list also does not
mean an algorithm uses constant extra space: Merge uses an auxiliary buffer.

A future iteration should collect repeated trials with varied seeds, randomize
algorithm execution order, and report distributions and uncertainty. Memory
profiling and additional partial-order definitions would improve recommendations.
Python's built-in sort, additional algorithms, CI, and a configurable interface
remain future work from the original plan. These improvements are not required
to interpret the transparent, single-trial v1.0.0 experiment.
