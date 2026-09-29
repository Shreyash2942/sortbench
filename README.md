# SortBench

A Python assignment comparing Bubble, Selection, Insertion, and Merge Sort
across four dataset orderings and four sizes. The question is: **how do sorting
performance and scalability change with input size and ordering?**

**Status:** Day 1 setup and design. Algorithm implementation starts on Day 2.
The module and test files are documented placeholders. Full benchmarks, charts,
and performance recommendations are scheduled for later days.

## Setup and run

From this repository directory in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Calling the virtual environment's interpreter directly avoids requiring a
PowerShell activation script. On macOS/Linux use `.venv/bin/python` instead.
The Day 1 entry point and runtime spike use only the standard library and can
also be run directly with `python main.py` and `python scripts/runtime_spike.py`.

When Day 2 tests are implemented, run:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Day 1 has no correctness tests yet; pytest would currently report no tests
collected. The setup does not claim the planned algorithms are working.

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
main.py                 Entry point (status display on Day 1)
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
- [Day 1 runtime spike](docs/RUNTIME_SPIKE.md)
- [Performance analysis — pending](docs/PERFORMANCE_ANALYSIS.md)
- [Recommendation guide — pending](docs/RECOMMENDATION_GUIDE.md)
- [Retrospective — pending](docs/RETROSPECTIVE.md)

The target release is `v1.0.0` after seven development days. The original
assignment includes the release checklist and future portfolio enhancements.
