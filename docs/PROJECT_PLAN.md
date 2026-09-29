# Seven-day implementation checklist

The original brief is preserved in [ASSIGNMENT_PLAN.md](ASSIGNMENT_PLAN.md).
This file tracks implementation status rather than treating planned work as done.

| Day | Work | Current status |
|---|---|---|
| 1 | Repository, structure, README, requirements, architecture, benchmark method, runtime spike | Complete |
| 2 | Implement and test four sorting algorithms | Complete |
| 3 | Implement and test four dataset generators | Pending |
| 4 | Implement timer, runner, validation, CSV export | Pending |
| 5 | Execute and validate the complete performance matrix | Pending |
| 6 | Analyze results, generate charts and recommendations, draft analysis | Pending |
| 7 | Final tests, documentation, retrospective, release | Pending |

## Day 1 deliverables

- [x] Use the existing local Git repository and its configured GitHub remote.
- [x] Create the planned module, test, result, and documentation directories.
- [x] Write the project README and preserve the original assignment plan.
- [x] Document functional and non-functional requirements.
- [x] Define the four algorithms, four dataset types, and four sizes.
- [x] Select `time.perf_counter()` and document timing boundaries.
- [x] Define sorting interfaces, data seeds, and partial-order construction.
- [x] Document architecture, workflow, and testing strategy.
- [x] Run and record the bounded quadratic-runtime spike.
- [x] Verify scaffold imports and entry point.
- [x] Create a local virtual environment and install project dependencies.

Verification completed on 2026-09-29 with Python 3.14.4: the entry point runs,
all scaffold Python files compile, 13 project/dependency modules import, and
`pip check` reports no broken requirements. All current documentation links
resolve, the original assignment copy is byte-for-byte preserved, and the spike
CSV contains all nine intended measurements. The virtual environment and Python
caches are excluded by `.gitignore`. Correctness tests were scheduled for Day 2
at that checkpoint and are now complete as described below.

The [runtime spike](RUNTIME_SPIKE.md) measured median times of approximately
0.007749, 0.030656, and 0.113984 seconds at 1,000, 2,000, and 4,000 elements.
These support planning for quadratic growth; they are not full sorting results.

The GitHub repository is [Shreyash2942/sortbench](https://github.com/Shreyash2942/sortbench).
Day 1 work is organized into focused commits for project scaffolding,
requirements and architecture, benchmark methodology and testing, and the
runtime feasibility experiment with its recorded results.

## Day 2 deliverables

- [x] Implement Bubble Sort with early exit for sorted input.
- [x] Implement Selection Sort using suffix-minimum selection.
- [x] Implement Insertion Sort using shifts within a sorted prefix.
- [x] Implement Merge Sort with one reusable auxiliary buffer.
- [x] Document behavior, complexity, stability, and the shared list contract.
- [x] Verify the assignment example manually with all four algorithms.
- [x] Add automated edge-case, exhaustive small-input, and seeded random tests.
- [x] Pass all 93 algorithm tests before benchmark development.

Validation: `.venv/Scripts/python.exe -m pytest -q` reports **93 passed** on
Python 3.14.4. Each function returns the same list object and matches the
independent built-in sorting oracle. The demonstration entry point runs all
four algorithms without producing benchmark measurements. Details are in
[ALGORITHMS.md](ALGORITHMS.md) and [TEST_PLAN.md](TEST_PLAN.md).

## Day 3 starting point

Implement and test the four dataset generators using the common seeded
multiset and partial-swap rule in [BENCHMARK_METHODOLOGY.md](BENCHMARK_METHODOLOGY.md).
Check sizes, ordering, equal value multiplicities, reproducibility, and isolation
from global random state before integrating the Day 4 benchmark runner.

## Day 1 decisions to carry forward

- All algorithms sort the supplied list and return that same list.
- All four orderings for a size share the same seeded multiset.
- Partially sorted means `size // 20` random swaps of a sorted list.
- The first experiment uses one recorded trial for each of 64 scenarios.
- Runtime projections belong in the spike report, not the benchmark CSV.
- Recommendations and final conclusions wait for actual measured results.
