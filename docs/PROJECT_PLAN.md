# Seven-day implementation checklist

The original brief is preserved in [ASSIGNMENT_PLAN.md](ASSIGNMENT_PLAN.md).
This file tracks implementation status rather than treating planned work as done.

| Day | Work | Current status |
|---|---|---|
| 1 | Repository, structure, README, requirements, architecture, benchmark method, runtime spike | Complete |
| 2 | Implement and test four sorting algorithms | Complete |
| 3 | Implement and test four dataset generators | Complete |
| 4 | Implement timer, runner, validation, CSV export | Complete |
| 5 | Execute and validate the complete performance matrix | Complete |
| 6 | Analyze results, generate charts and recommendations, draft analysis | Complete |
| 7 | Final tests, documentation, retrospective, release | Complete for requested scope; GitHub Release deferred by user |

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

## Day 3 deliverables

- [x] Implement random, sorted, reverse-sorted, and partially sorted generators.
- [x] Support configurable nonnegative integer sizes and export required SIZES.
- [x] Add deterministic default seeds and explicit integer seed overrides.
- [x] Preserve the common multiset across all four orderings for a size/seed.
- [x] Implement the documented `size // 20` partial-swap rule.
- [x] Verify size, ordering, reproducibility, fresh storage, and global RNG isolation.
- [x] Document methodology, API examples, validation, and seed limitations.

Validation on 2026-09-30: `.venv/Scripts/python.exe -m pytest -q` reports
**268 passed** (93 algorithm tests plus 175 dataset/integration tests).
All required generation sizes, including 50,000, are exercised. Small integration
cases verify all 16 algorithm/dataset combinations. The demonstration includes
all four generated orderings; it produces no benchmark results.
See [DATA_GENERATION.md](DATA_GENERATION.md) for the implemented contracts.

## Day 4 deliverables

- [x] Implement sorting-only `time.perf_counter()` timing.
- [x] Iterate through all algorithms, dataset types, and selected sizes.
- [x] Generate each dataset once and copy it independently for every algorithm.
- [x] Validate sorted values, list identity, and finite nonnegative elapsed time.
- [x] Export validated CSV rows with an adjacent environment/status JSON file.
- [x] Preserve prior valid rows and record failure/interruption context.
- [x] Add tests for timing boundaries, isolation, validation, and persistence.
- [x] Run a separate small real smoke experiment and verify the saved results.

Validation on 2026-10-01: **301 tests pass** (93 algorithm, 175 dataset/integration,
33 timer/benchmark). The real [smoke CSV](../results/day4_smoke.csv) contains 32
validated measurements for sizes 10 and 100; its [metadata](../results/day4_smoke.metadata.json)
reports complete. This checks the pipeline but does not complete the required
Day 5 experiment. At the Day 4 checkpoint, the full benchmark CSV had not been created.

## Day 5 deliverables

- [x] Run all 64 required combinations, including 50,000-element cases.
- [x] Preserve and review the initial run's apparent long-pause anomaly.
- [x] Repeat the full matrix and use that entire repeat as the final dataset.
- [x] Audit schema, coverage, duplicates, times, seeds, and metadata.
- [x] Compare algorithms by size and ordering and identify observed winners.
- [x] Check noisy 5,000/10,000-element groups in a separate diagnostic run.
- [x] Document conditions and limitations without averaging or cherry-picking.
- [x] Add automated tests for persisted-result validation.

Validation on 2026-10-02 (local date): **338 tests pass**. The final CSV has
64 unique validated rows and complete metadata. The full repeat took 396.21
seconds wall time and 393.31 seconds CPU time. Merge Sort was fastest in 12
size/type groups, Bubble Sort in 3, and Insertion Sort in 1 in the primary run.
See [DAY5_OBSERVATIONS.md](DAY5_OBSERVATIONS.md) for timings and diagnostic
findings. Initial and diagnostic runs remain separate from the primary dataset.

## Day 6 deliverables

- [x] Load the primary CSV only after a complete metadata and coverage audit.
- [x] Export comparison tables, observed winners, and measured growth ratios.
- [x] Generate six labeled PNG charts for size and ordering comparisons.
- [x] Implement exact-scenario recommendations with ties and missing-data handling.
- [x] Write the performance analysis draft and Big-O/space/stability table.
- [x] Complete the measured recommendation guide and reproduction workflow.
- [x] Preserve original evidence and record derived-artifact SHA-256 hashes.
- [x] Test summaries, recommendations, chart data, and end-to-end generation.

Validation on 2026-10-03: **358 tests pass**, including 20 new analysis tests.
The generated comparisons retain all 64 measurements. Recommendations cover
all 16 size/type groups; charts show one observation per scenario without
statistical uncertainty estimates. The separate diagnostic ranking change
is disclosed. See [ANALYSIS_WORKFLOW.md](ANALYSIS_WORKFLOW.md) and
[PERFORMANCE_ANALYSIS.md](PERFORMANCE_ANALYSIS.md).

## Day 7 deliverables

- [x] Review source code, docstrings, deliverables and incremental Git history.
- [x] Extend analysis input protection to all generated filenames.
- [x] Pass all 363 tests in a fresh environment installed from the lock file.
- [x] Verify dependency consistency, the demo, result hashes, and document links.
- [x] Finalize the analysis as a three-page PDF with editable Markdown source.
- [x] Complete the README, recommendation guide, and retrospective.
- [x] Preserve the original assignment and all benchmark evidence.
- [x] Prepare v1.0.0 release notes and an evidence-based release checklist.
- [x] Push the completed project and annotated v1.0.0 tag to GitHub.
- GitHub Release publication is deferred by user request and is not required now.

See [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) for verification evidence and
publication status. All requested work is complete and pushed. The original
plan remains unchanged; the user chose to defer its GitHub Release publication
step and finish with the repository push.

## Day 1 decisions to carry forward

- All algorithms sort the supplied list and return that same list.
- All four orderings for a size share the same seeded multiset.
- Partially sorted means `size // 20` random swaps of a sorted list.
- The first experiment uses one recorded trial for each of 64 scenarios.
- Runtime projections belong in the spike report, not the benchmark CSV.
- Recommendations and final conclusions wait for actual measured results.
