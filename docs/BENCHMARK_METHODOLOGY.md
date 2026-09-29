# Benchmark methodology

This is the Day 1 experimental design, not a record of completed benchmarks.

## Required matrix

- Algorithms: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort.
- Dataset types: random, sorted, reverse-sorted, partially sorted.
- Sizes: 1,000, 5,000, 10,000, 50,000.
- Coverage: 4 × 4 × 4 = **64 scenarios**.

## Dataset definitions

Use a local `random.Random(seed)` instance, not global random state. Set the
base seed to 506 and derive each size's seed as `506 + size`.

For each size, generate `size` integer draws using `randint(0, 10 * size)`.
Duplicates are allowed. Use this same base multiset for all four orderings:

| Type | Construction |
|---|---|
| Random | The original seeded draws. |
| Sorted | The base values arranged in ascending order. |
| Reverse-sorted | The sorted base values reversed, giving nonincreasing order. |
| Partially sorted | Start with sorted base values; perform `size // 20` swaps, each using two distinct random indices from a local generator seeded with `seed + 1`. |

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

## Planned output

`results/benchmark_results.csv` will have this header:

```csv
algorithm,dataset_type,size,trial,seed,execution_time_seconds,valid
```

Use `trial=1` initially, seconds as the time unit, and `valid=True` only after
validation. Record the timestamp, Python version, platform/processor, seed rule,
trial count, and timing conditions alongside the CSV in a run metadata file.
The CSV is intentionally absent until real benchmark measurements exist.

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
