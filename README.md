# SortBench

A Python assignment comparing Bubble, Selection, Insertion, and Merge Sort
across four dataset orderings and four sizes. The question is: **how do sorting
performance and scalability change with input size and ordering?**

**Version:** v1.0.0. Implementation and Day 7 quality assurance are complete:
**363 tests pass**, all **64 benchmark scenarios** are recorded, and the final
charts, recommendations, [Word report](docs/SortBench_Final_Project_Report.docx),
and Markdown reports are included. All project work is pushed to GitHub.
Creating a GitHub Release page is deferred by user request.

## Setup and run

From this repository directory in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe main.py
```

Calling the virtual environment's interpreter directly avoids requiring a
PowerShell activation script. On macOS/Linux use `.venv/bin/python` instead.
The lock file captures the verified Windows/Python 3.14.4 environment;
`requirements.txt` lists direct dependencies for a flexible installation. Other
Python versions and platforms have not been verified.
The sorting demonstration and Day 1 runtime spike use only the standard library and can
also be run directly with `python main.py` and `python scripts/runtime_spike.py`.

Run the complete correctness test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

`main.py` runs each algorithm on `[8, 3, 1, 6, 4]` and displays
`[1, 3, 4, 6, 8]`, followed by examples of all four dataset types using 20
elements and seed 0. This demonstration does not time sorts or generate
benchmark results.

Use an algorithm directly:

```python
from algorithms import merge_sort

values = [8, 3, 1, 6, 4]
result = merge_sort(values)
assert result is values
assert values == [1, 3, 4, 6, 8]
```

Every algorithm modifies and returns the supplied list.

Generate reproducible datasets:

```python
from data import SIZES, generate_random, generate_partially_sorted

assert SIZES == [1000, 5000, 10000, 50000]
random_values = generate_random(1000)  # Default seed: 506 + 1000
partial_values = generate_partially_sorted(1000)
assert sorted(random_values) == sorted(partial_values)
```

All generators accept a keyword `seed` override and return fresh lists.

Run a small benchmark from the repository root:

```powershell
.\.venv\Scripts\python.exe -c "from benchmark import run_benchmarks; run_benchmarks('results/my_smoke.csv', sizes=[10, 100])"
```

This writes 32 validated rows and `results/my_smoke.metadata.json`. Each run
requires a new output filename. Existing results are never overwritten.
The committed [Day 4 smoke results](results/day4_smoke.csv) verify the
pipeline and are not the final experiment dataset.

The full [benchmark CSV](results/benchmark_results.csv),
[metadata](results/benchmark_results.metadata.json), and
[audit report](results/validation_report.json) are available. The primary
dataset uses one trial per scenario; no averages across attempts or
selectively chosen fastest measurements are reported.

## Analysis and charts

Regenerate the derived outputs from the audited primary CSV:

```powershell
.\.venv\Scripts\python.exe -m analysis.performance_analyzer
```

This command regenerates derived analysis artifacts from the audited primary
CSV. It does not rerun benchmarks or change measurements.

![Execution time versus dataset size](docs/figures/time_vs_size.png)

Merge Sort had the lowest recorded time in all 12 random, reverse-sorted,
and partially sorted groups. Bubble won three sorted groups and Insertion
one; the separate diagnostic changed their ranking at 10,000 elements.
These are single-trial observations, not statistically established advantages.
See the [performance analysis](docs/PERFORMANCE_ANALYSIS.md),
[recommendation guide](docs/RECOMMENDATION_GUIDE.md), and
[ordering comparison chart](docs/figures/dataset_comparison.png).

## Required experiment

| Dimension | Values |
|---|---|
| Algorithms | Bubble, Selection, Insertion, Merge |
| Dataset types | Random, sorted, reverse-sorted, partially sorted |
| Sizes | 1,000; 5,000; 10,000; 50,000 |
| Total | 64 scenarios |

Timing uses `time.perf_counter()`. Each algorithm receives an independent copy
of equivalent data, and every result is checked against `sorted(original)`.
Generation, copying, validation, and CSV writing are outside the timed interval.

## Repository layout

```text
main.py                 Sorting and dataset-generation demonstration
requirements.txt        pytest, pandas, matplotlib
algorithms/             Four sorting algorithms (Day 2)
data/                   Dataset generation (Day 3)
benchmark/              Timer and runner (Day 4)
analysis/               Summaries and recommendations (Day 6)
visualization/          Charts (Day 6)
results/                Actual measured data and generated charts
tests/                  Correctness and integration tests (Days 2 onward)
scripts/runtime_spike.py Bounded Day 1 feasibility experiment
docs/                   Final reports, figures, and recommendation guide
```

## Project documents

- [Documentation index](docs/README.md)
- [Project guide](docs/PROJECT_GUIDE.md)
- [Final Word report](docs/SortBench_Final_Project_Report.docx)
- [APA-style project report source](docs/APA_PROJECT_REPORT.md)
- [Performance analysis](docs/PERFORMANCE_ANALYSIS.md)
- [Measured recommendation guide](docs/RECOMMENDATION_GUIDE.md)

Version `v1.0.0` contains the completed seven-day implementation. Dashboards,
additional algorithms, CI, and repeated-trial statistics remain future
portfolio enhancements.
