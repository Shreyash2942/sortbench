# Benchmark methodology

This is the experimental design established on Day 1, with dataset generation
implemented on Day 3 and the timing/export pipeline implemented on Day 4.
The full required experiment was completed on Day 5; see
[DAY5_OBSERVATIONS.md](DAY5_OBSERVATIONS.md) for measurements and conditions.

## Required matrix

- Algorithms: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort.
- Dataset types: random, sorted, reverse-sorted, partially sorted.
- Sizes: 1,000, 5,000, 10,000, 50,000.
- Coverage: 4 × 4 × 4 = **64 scenarios**.

## Dataset definitions

Use a local `random.Random(seed)` instance, not global random state. Set the
base seed to 506 and derive each size's seed as `506 + size`.

The implemented API applies this rule when `seed` is omitted or None. Every
generator also accepts an explicit integer seed, including zero or negative
integers, so custom comparisons can use the same base multiset. Do not mix
different seeds when comparing orderings for one scenario. Record the effective
integer seed, not None, in the CSV. See [DATA_GENERATION.md](DATA_GENERATION.md).

For each size, generate `size` integer draws using `randint(0, 10 * size)`.
Duplicates are allowed. Use this same base multiset for all four orderings:

| Type | Construction |
|---|---|
| Random | The original seeded draws. |
| Sorted | The base values arranged in ascending order. |
| Reverse-sorted | The sorted base values reversed, giving nonincreasing order. |
| Partially sorted | Start with sorted base values; perform `size // 20` swaps, each using two distinct random indices from a local generator seeded with `seed + 1`. |

Each swap chooses its indices using `rng.sample(range(size), 2)`. This separate
generator keeps the swap sequence independent of how many base values were
drawn. All generators preserve Python's global random state.

The partially sorted rule performs 5% as many swaps as there are elements; it
does **not** guarantee exactly 5% of elements are displaced. Repeated indices
and equal values can reduce the actual disorder. For sizes below 20, perform
zero swaps. Tests should check this specified construction, not an exact
percentage of displaced elements. Sorting to construct datasets is outside the
timed interval and does not substitute for the four handwritten algorithms.

## Timing and correctness

1. Generate the original list and compute `expected = sorted(original)`.
2. Copy the original immediately before each algorithm call.
3. Read `time.perf_counter()`, call the algorithm, and immediately read the timer
   again. The difference is elapsed wall-clock seconds.
4. Check output equality with `expected` outside timing. Equality checks both
   order and the multiplicity of every value. Check the shared return contract.
5. Write a validated CSV record outside timing, flushing completed records so
   slow later scenarios do not require discarding earlier measurements.

Use one recorded trial per scenario for the initial 64-row dataset. This
lightweight design does not support statistical confidence claims. If noisy
results require repeated trials on Day 5, repeat the comparison set consistently,
keep individual rows with distinct trial numbers, and document the revised
method before using averages. Do not selectively retain only the fastest run.

Run sequentially in a fixed documented algorithm order (Bubble, Selection,
Insertion, Merge) on one machine/environment. Close avoidable background work
and record any interruptions. Fixed order can introduce drift; discuss this
limitation in the final analysis. No threaded or parallel experiment execution.

## Implemented output

The full Day 5 dataset will be `results/benchmark_results.csv`. The runner uses
this header for every output file:

```csv
algorithm,dataset_type,size,trial,seed,execution_time_seconds,valid
```

The runner uses `trial=1`, seconds as the time unit, and `valid=True` only after
validating list identity, sorted values, and finite nonnegative elapsed time.
It records timestamps, Python version, platform/processor, effective seeds,
trial count, timing method, scenario order, and completion status in an adjacent
`<stem>.metadata.json` file. Both outputs must be new files. Validated CSV rows
are flushed as they finish; caught errors and interrupts update metadata.

Day 4's `results/day4_smoke.csv` contains 32 real pipeline-check measurements
at sizes 10 and 100. It is separate from the required 64 scenarios and provides
no final algorithm rankings. The full `benchmark_results.csv` now contains
the 64 primary Day 5 measurements.
See [BENCHMARK_RUNNER.md](BENCHMARK_RUNNER.md) for commands and failure semantics.

## Day 5 run selection and diagnostics

The initial complete run had an apparent long pause during the 50,000-element
reverse-sorted Bubble Sort measurement. Its CSV and metadata are preserved
unchanged in `results/initial_run/` and excluded from timing conclusions.
The full matrix was repeated using identical code, seeds, scenario order, and
one trial per scenario. Only that complete repeat supplies the primary CSV;
no rows were selected individually between attempts and no averages were
calculated. Windows received a temporary stay-awake request for the repeat,
released afterward without changing saved power settings.

A further 32-scenario diagnostic repeated all algorithms/types at sizes 5,000
and 10,000 to check ranking changes and irregular small measurements. Those rows
remain in `results/diagnostic_5000_10000.csv` and are neither substituted into nor
averaged with the primary data. Conditions, hashes, and limitations are documented
in [RESULT_VALIDATION.md](RESULT_VALIDATION.md) and the observations report.

## Runtime feasibility

The Day 1 spike in `scripts/runtime_spike.py` measures a small selection-style
comparison loop at 1,000, 2,000, and 4,000 elements, with three trials per size.
This illustrates quadratic growth without implementing the Day 2 algorithms.
Use the exact comparison-count ratio to project a possible 50,000-element cost.
The projection is neither a measured runtime nor a prediction for every
quadratic sorting algorithm; assignments, swaps, input order, and machine state
affect full sorting time.

Keep 50,000-element cases in the final experiment. If a case cannot finish,
document the scenario, elapsed duration, reason, and rerun status separately;
never fabricate its CSV measurement or describe the full matrix as completed.
