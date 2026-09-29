# SortBench

A Python assignment comparing Bubble, Selection, Insertion, and Merge Sort
across four dataset orderings and four sizes. The question is: **how do sorting
performance and scalability change with input size and ordering?**

**Status:** Days 1 and 2 complete. All four sorting algorithms are implemented
and pass 93 automated tests. Dataset generation, full benchmarks, charts, and
performance recommendations are scheduled for later days; their modules remain
documented placeholders.

## Setup and run

From this repository directory in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Calling the virtual environment's interpreter directly avoids requiring a
PowerShell activation script. On macOS/Linux use `.venv/bin/python` instead.
The sorting demonstration and Day 1 runtime spike use only the standard library and can
also be run directly with `python main.py` and `python scripts/runtime_spike.py`.

Run the algorithm correctness tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

`main.py` runs each algorithm on `[8, 3, 1, 6, 4]` and displays
`[1, 3, 4, 6, 8]`. This is a correctness demonstration; it does not time sorts
or generate benchmark results.

Use an algorithm directly:

```python
from algorithms import merge_sort

values = [8, 3, 1, 6, 4]
result = merge_sort(values)
assert result is values
assert values == [1, 3, 4, 6, 8]
```

Every algorithm modifies and returns the supplied list. See the
[algorithm guide](docs/ALGORITHMS.md) for behavior and complexity.

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
main.py                 Four-algorithm correctness demonstration
requirements.txt        pytest, pandas, matplotlib
algorithms/             Four sorting algorithms (Day 2)
data/                   Dataset generation (Day 3)
benchmark/              Timer and runner (Day 4)
analysis/               Summaries and recommendations (Day 6)
visualization/          Charts (Day 6)
results/                Actual measured data and generated charts
tests/                  Correctness and integration tests (Days 2 onward)
scripts/runtime_spike.py Bounded Day 1 feasibility experiment
docs/                   Requirements, plans, methodology, and reports
```

## Project documents

- [Original assignment plan](docs/ASSIGNMENT_PLAN.md)
- [Progress and next steps](docs/PROJECT_PLAN.md)
- [Requirements](docs/REQUIREMENTS.md)
- [Architecture and benchmark workflow](docs/ARCHITECTURE.md)
- [Benchmark methodology](docs/BENCHMARK_METHODOLOGY.md)
- [Test plan](docs/TEST_PLAN.md)
- [Algorithm implementations and complexity](docs/ALGORITHMS.md)
- [Day 1 runtime spike](docs/RUNTIME_SPIKE.md)
- [Performance analysis — pending](docs/PERFORMANCE_ANALYSIS.md)
- [Recommendation guide — pending](docs/RECOMMENDATION_GUIDE.md)
- [Retrospective — pending](docs/RETROSPECTIVE.md)

The target release is `v1.0.0` after seven development days. The original
assignment includes the release checklist and future portfolio enhancements.
