# Architecture

SortBench is a local Python program built from small modules. The following
diagram describes the intended full system. As of Day 2, the four sorting
functions, algorithm tests, and a demonstration entry point are implemented.
Dataset generation, benchmarking, analysis, and plotting remain placeholders.

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
  expose an optional keyword `seed` for random and partially sorted data. Reject
  invalid sizes clearly. The runner supplies the documented scenario seed.
- The timing utility accepts a sorting callable and an already copied list;
  it returns the sorting result and elapsed seconds. It performs no generation,
  copying, validation, or CSV output inside the timed interval.
- The runner owns configuration, scenario iteration, copies, expected results,
  validation, and CSV export. It records a row only after correctness validation.
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
as a valid measurement. Already written valid rows may remain for diagnosis.

Detailed dataset definitions and timing rules are in
[BENCHMARK_METHODOLOGY.md](BENCHMARK_METHODOLOGY.md).
