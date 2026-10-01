# Day 4 benchmark runner

`benchmark.time_sort(sorter, values)` returns `(result, elapsed_seconds)` for
an already copied list. Its two `time.perf_counter()` calls directly bracket
the sorting call. Generation, copying, validation, and output happen in
`benchmark.run_benchmarks`, outside that interval. Internal sorter allocations,
such as Merge Sort's auxiliary buffer, are included.

## Run a small verification experiment

From the repository directory in PowerShell, choose a new output filename:

```powershell
.\.venv\Scripts\python.exe -c "from benchmark import run_benchmarks; rows = run_benchmarks('results/my_smoke.csv', sizes=[10, 100]); print(len(rows))"
```

This runs 4 algorithms × 4 dataset types × 2 sizes = 32 actual sorting calls.
Day 4 already recorded such a run in [day4_smoke.csv](../results/day4_smoke.csv)
and [day4_smoke.metadata.json](../results/day4_smoke.metadata.json). Those small
measurements verify the pipeline; they do not establish the final rankings.

`main.py` remains a quick sorting/dataset demonstration and does not start
benchmark experiments or create result files.

## Full experiment — Day 5

```powershell
.\.venv\Scripts\python.exe -c "from benchmark import run_benchmarks; rows = run_benchmarks(); print(len(rows))"
```

The defaults select sizes 1,000, 5,000, 10,000, and 50,000 and write
`results/benchmark_results.csv` plus `results/benchmark_results.metadata.json`.
That is 64 scenarios, one recorded trial each. This full run has not been
performed on Day 4. Large quadratic sorts take substantially longer than the
small verification run; retain all required sizes in the experiment.

The API is:

```python
run_benchmarks(output_path="results/benchmark_results.csv", *, sizes=None, seed=None)
```

It returns the same validated row dictionaries written to the CSV. `sizes`
accepts a nonempty sequence of distinct nonnegative integers. None selects the
assignment sizes. Boolean, noninteger, negative, empty, or duplicate size
configurations are rejected before creating output files. A custom integer
seed (including 0 or a negative number) overrides `506 + size` for every size.
Paths are relative to the caller's working directory; missing parent folders
are created. The output must have a `.csv` extension.

## Fairness and record format

Scenario iteration is size, then dataset type (`random`, `sorted`,
`reverse_sorted`, `partially_sorted`), then algorithm (Bubble, Selection,
Insertion, Merge). Execution is sequential in that fixed order. Each
size/type dataset is generated once, its expected output is computed once,
and each algorithm receives a fresh copy. Validation requires both output
equality with `sorted(original)` and return of that same working list.

```csv
algorithm,dataset_type,size,trial,seed,execution_time_seconds,valid
```

Only correct outputs with finite, nonnegative elapsed seconds are recorded.
`trial` is 1 and `valid` is True. Each completed row is flushed immediately.
Adjacent metadata records environment details, timestamps, size/seed settings,
scenario order, expected/completed row counts, and run status. The field
`required_sizes_selected` distinguishes assignment sizes from small checks;
only a complete run with all 64 distinct required keys completes Day 5.

## Existing results and incomplete runs

If either output file already exists, the runner raises `FileExistsError`.
Choose a new filename for a repeat run; there is no automatic overwrite, append,
resume, or retry. Keep earlier evidence until any comparison or rerun is reviewed.

An invalid result or sorter exception stops the experiment. Previously flushed
valid rows remain, and metadata records `failed` plus the failing scenario.
Ctrl+C records `interrupted` and re-raises the interrupt. Successful runs record
`complete`. Metadata counts are refreshed when the run exits; a hard process
termination or power loss can leave `running` metadata with stale counts and
a partial final CSV row. Inspect incomplete output rather than treating it as
a completed dataset. Ordinary file flushing does not guarantee disk durability
through power loss.

Only one process should own a run/output pair. Run timing conditions and any
interruptions should be noted in the final analysis. The runner makes no
statistical claims from its single trial, and the Day 4 tests use no fixed
wall-clock performance thresholds.
