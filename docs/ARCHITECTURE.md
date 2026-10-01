# Architecture

SortBench is a local Python program built from small modules. The following
diagram describes the intended full system. As of Day 4, sorting, data generation,
the timer, benchmark runner, CSV/metadata output, tests, and a demonstration
entry point are implemented. Analysis and plotting remain placeholders.
`main.py` stays a quick demonstration; the benchmark API is invoked separately
as described in [BENCHMARK_RUNNER.md](BENCHMARK_RUNNER.md).

```text
main.py
  -> benchmark/benchmark_runner.py
       -> data/data_generator.py          create equivalent source datasets
       -> benchmark/timer.py              time a sorting call
            -> algorithms/*.py            sort a working copy
       -> results/benchmark_results.csv   save validated measurements
  -> analysis/performance_analyzer.py     read CSV, summarize results
       -> visualization/charts.py         save results/charts/
       -> analysis/recommendation.py      identify measured winners
  -> docs/                               interpret results and trade-offs
```

## Component contracts

- Each sorting function accepts `values: list[int]`, sorts that list in ascending
  order, and returns the same list. Bubble Sort uses an early-exit flag. Merge
  Sort may allocate an auxiliary buffer while preserving the shared interface.
  Its allocation is part of the sorting time. No implementation calls `sorted()`
  or `list.sort()`.
- Generators return a fresh `list[int]`, accept a nonnegative integer `size`, and
  expose an optional keyword `seed` for all four orderings. An omitted or None
  seed resolves to `506 + size`. Explicit integer seeds override it. Equal
  sizes/seeds produce equal value multisets across orderings. Invalid size/seed
  types (including booleans) raise TypeError; negative sizes raise ValueError.
  The runner records the effective seed in its result rows.
- The timing utility accepts a sorting callable and an already copied list;
  it returns the sorting result and elapsed seconds. It performs no generation,
  copying, validation, or CSV output inside the timed interval.
- The runner owns configuration, scenario iteration, copies, expected results,
  validation, and CSV export. It records a row only after correctness validation.
  It flushes each row and writes adjacent JSON metadata with run status and
  environment details. Existing output files are protected from overwriting.
- Analysis and plotting consume CSV data. They do not rerun sorting to obtain
  values. Recommendations identify the measured winner for a scenario and
  explicitly flag ties or missing data.

## Benchmark workflow

```text
Select size and dataset type
           |
Generate original data once; compute expected = sorted(original)
           |
For each algorithm: working = original.copy()
           |
perf_counter() -> sort(working) -> perf_counter()
           |
Check result == expected and shared contract
           |
Record validated elapsed time -> append CSV row
           |
Continue through 64 scenarios -> summarize -> charts and written analysis
```

Dataset generation and expected-result calculation happen before timing. The
working-copy cost is excluded equally for all algorithms; temporary storage
allocated inside a sorting implementation is included. A failed validation
raises an error naming the scenario and prevents that result from being treated
as a valid measurement. Already written valid rows remain for diagnosis, and
metadata records failed/interrupted status and the scenario that stopped the run.

Detailed dataset definitions and timing rules are in
[BENCHMARK_METHODOLOGY.md](BENCHMARK_METHODOLOGY.md).
