# SortBench Project Guide

This guide explains how to set up, run, test, and understand the completed
SortBench project.

## Project purpose

SortBench compares four sorting algorithms:

- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort

The project measures how execution time changes across four dataset orderings
and four input sizes:

| Category | Values |
|---|---|
| Dataset orderings | random, sorted, reverse-sorted, partially sorted |
| Sizes | 1,000; 5,000; 10,000; 50,000 |
| Total benchmark scenarios | 64 |

The final measured results are already included in `results/`, so you do not
need to rerun the long benchmark to review the completed assignment.

## Repository layout

| Path | Purpose |
|---|---|
| `main.py` | Small demonstration of sorting and dataset generation |
| `algorithms/` | Manual implementations of Bubble, Selection, Insertion, and Merge Sort |
| `data/` | Dataset generators for all required input orderings |
| `benchmark/` | Timing, benchmark runner, metadata, and result validation |
| `analysis/` | Analysis tables and recommendation logic |
| `visualization/` | Chart generation code |
| `results/` | Recorded benchmark evidence and derived analysis outputs |
| `docs/` | Final report files, guide, recommendation notes, and figures |
| `tests/` | Automated correctness, runner, validation, and analysis tests |

## Setup

From the repository root, create a virtual environment and install the locked
dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

The lock file records the verified Windows and Python 3.14.4 environment. The
shorter `requirements.txt` file lists the direct dependencies only.

## Run the demonstration

Run:

```powershell
.\.venv\Scripts\python.exe main.py
```

The demonstration sorts `[8, 3, 1, 6, 4]` with each algorithm and prints a small
sample of each dataset type. It does not run the full benchmark.

## Run tests

Run the full test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The completed project was verified with 363 passing tests. These tests cover
algorithm correctness, dataset generation, benchmark timing, persisted-result
validation, analysis logic, recommendations, and chart behavior.

## Review the completed benchmark results

The primary benchmark data is stored here:

- `results/benchmark_results.csv`
- `results/benchmark_results.metadata.json`
- `results/validation_report.json`

The benchmark used one recorded trial per scenario. Each algorithm received an
independent list copy, and every result was validated against Python's
`sorted(original)` output.

## Regenerate analysis outputs

To regenerate derived tables and chart images from the committed benchmark CSV:

```powershell
.\.venv\Scripts\python.exe -m analysis.performance_analyzer
```

This command reads the existing benchmark evidence and regenerates analysis
outputs. It does not rerun the long benchmark and does not change the measured
source data.

Derived outputs include:

- `results/analysis/comparison.csv`
- `results/analysis/growth.csv`
- `results/analysis/observed_winners.csv`
- `results/analysis/recommendations.json`
- `results/analysis/charts/*.png`

Copies of the final chart images are also available in `docs/figures/` for the
report package.

## Run a small benchmark

Use a small custom output file when testing the runner:

```powershell
.\.venv\Scripts\python.exe -c "from benchmark import run_benchmarks; run_benchmarks('results/my_smoke.csv', sizes=[10, 100])"
```

Each benchmark output path must be new. The runner refuses to overwrite existing
CSV evidence.

The full required benchmark can take several minutes because the quadratic
algorithms sort up to 50,000 elements. The submitted project already includes
the full completed benchmark results.

## Final report files

The docs folder contains the final report package:

- `SortBench_Final_Project_Report.docx`
- `APA_PROJECT_REPORT.md`
- `PERFORMANCE_ANALYSIS.md`
- `RECOMMENDATION_GUIDE.md`
- `figures/`

The Word document is the submission-ready report. The Markdown files remain in
the repository so the report content and measured interpretation can be reviewed
directly on GitHub.

## Main findings

Merge Sort was the fastest measured algorithm for every tested random,
reverse-sorted, and partially sorted scenario. Bubble Sort won three sorted
input groups, and Insertion Sort won one sorted input group. These findings
match the expected trade-off: Merge Sort scales well on disordered data, while
adaptive simple algorithms can be efficient when the input is already sorted.

Because each scenario has one recorded trial, the report presents the results
as project evidence rather than statistically generalized performance claims.
