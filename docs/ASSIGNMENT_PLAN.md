# SortBench - Sorting Algorithm Performance Analyzer

## Project Overview

**SortBench** is a Python-based sorting algorithm comparison tool designed to implement, test, benchmark, and analyze the performance of multiple sorting methods on datasets with different sizes and ordering characteristics.

The first version of this project is a **7-day college-level implementation** focused on demonstrating core software engineering practices, algorithm analysis, performance testing, documentation, visualization, and Git-based version control.

The project compares the following sorting algorithms:

- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort

Each algorithm will be tested against multiple dataset types and sizes so that execution-time differences, scalability, and practical trade-offs can be observed.

---

## Project Goal

The main goal of SortBench is to build a structured performance analysis tool that answers the following question:

> How do different sorting algorithms perform when dataset size and data ordering change?

The project will combine algorithm implementation, dataset generation, automated timing, result analysis, charts, and recommendation logic into one organized Python application.

---

## Project Scope

### Sorting Algorithms

The project will implement four sorting algorithms:

1. Bubble Sort
2. Selection Sort
3. Insertion Sort
4. Merge Sort

### Dataset Types

The benchmark system will generate four types of datasets:

1. Random data
2. Already sorted data
3. Reverse-sorted data
4. Partially sorted data

### Dataset Sizes

Each algorithm will be tested with the following dataset sizes:

- 1,000 elements
- 5,000 elements
- 10,000 elements
- 50,000 elements

### Benchmark Coverage

The complete benchmark will include:

```text
4 algorithms x 4 dataset types x 4 dataset sizes = 64 benchmark scenarios
```

---

## Success Criteria

The project will be considered successful when:

- All four sorting algorithms correctly sort arrays of different sizes.
- The data generator correctly produces all four required dataset types.
- The benchmark system measures algorithm execution time consistently.
- All 64 required benchmark scenarios are executed and recorded.
- Performance differences are visible in tables and charts.
- The written analysis explains algorithm trade-offs correctly.
- The recommendation guide provides practical guidance based on dataset characteristics.
- The codebase is organized, documented, tested, and maintained through Git.

---

## Recommended Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Main programming language |
| `time.perf_counter()` | High-resolution execution timing |
| `random` | Dataset generation |
| `copy` | Creating independent benchmark inputs |
| `csv` | Benchmark result storage |
| `pandas` | Result analysis and tabular processing |
| `matplotlib` | Performance visualization |
| `pytest` | Automated testing |
| Git | Version control |
| GitHub | Repository hosting and project history |

---

## Development Approach

### Project Level

The first version of SortBench is treated as a **small structured software engineering project**.

The project is appropriate for a lightweight structured process because it:

- is completed by one developer;
- has clearly defined requirements;
- contains multiple reusable modules;
- requires correctness testing and performance testing;
- includes documentation and analysis;
- does not require databases, authentication, cloud infrastructure, or production deployment.

### Development Process

A **Hybrid Agile / Scrum-Lite** development approach will be used.

The project has fixed core requirements, but development will be completed incrementally across seven days. Each day has one major objective, smaller implementation tasks, testing activities, and Git commits.

### Sprint Goal

> Develop, test, benchmark, analyze, document, and release a working sorting algorithm performance comparison tool within seven development days.

---

## Project Architecture

The application will be divided into separate components so that sorting logic, data generation, benchmarking, analysis, visualization, and testing remain independent.

```text
SortBench
|
|-- Sorting Algorithms
|-- Dataset Generator
|-- Benchmark / Timing Engine
|-- Result Storage
|-- Performance Analyzer
|-- Chart Generator
`-- Recommendation Generator
```

### Planned Repository Structure

```text
sortbench/
|
|-- README.md
|-- requirements.txt
|-- main.py
|
|-- algorithms/
|   |-- __init__.py
|   |-- bubble_sort.py
|   |-- selection_sort.py
|   |-- insertion_sort.py
|   `-- merge_sort.py
|
|-- data/
|   |-- __init__.py
|   `-- data_generator.py
|
|-- benchmark/
|   |-- __init__.py
|   |-- timer.py
|   `-- benchmark_runner.py
|
|-- analysis/
|   |-- performance_analyzer.py
|   `-- recommendation.py
|
|-- visualization/
|   `-- charts.py
|
|-- results/
|   |-- benchmark_results.csv
|   `-- charts/
|
|-- tests/
|   |-- test_algorithms.py
|   |-- test_data_generator.py
|   `-- test_benchmark.py
|
`-- docs/
    |-- PROJECT_PLAN.md
    |-- REQUIREMENTS.md
    |-- ARCHITECTURE.md
    |-- TEST_PLAN.md
    |-- PERFORMANCE_ANALYSIS.md
    |-- RECOMMENDATION_GUIDE.md
    `-- RETROSPECTIVE.md
```

---

# 7-Day Implementation Plan

## Day 1 - Project Setup, Requirements, and Architecture

### Major Objective

Establish the repository, project structure, requirements, architecture, and benchmark methodology before algorithm development begins.

### Tasks

- Create the GitHub repository.
- Create the initial project directory structure.
- Write the initial `README.md`.
- Document functional and non-functional requirements.
- Define the four algorithms, dataset types, and dataset sizes.
- Select `time.perf_counter()` as the benchmark timing method.
- Perform a short technical spike to understand the expected runtime of O(n^2) algorithms on large datasets.
- Create the initial architecture and benchmark workflow documentation.

### Expected Deliverables

- Repository created
- Project structure created
- README created
- Requirements documented
- Architecture documented
- Benchmark strategy defined

### Planned Git Commits

```bash
git commit -m "Initialize SortBench project structure"
git commit -m "Add project requirements and architecture documentation"
git commit -m "Define benchmark methodology and test scenarios"
```

### Quality Gate

Before Day 2 begins:

- Requirements must be documented.
- Repository structure must be finalized.
- Benchmark methodology must be defined.
- Architecture must be understandable and lightweight.

---

## Day 2 - Sorting Algorithm Implementation

### Major Objective

Implement and verify all four required sorting algorithms.

### Tasks

- Implement Bubble Sort.
- Implement Selection Sort.
- Implement Insertion Sort.
- Implement Merge Sort.
- Add clear function documentation and comments.
- Manually test each algorithm using small arrays.
- Create automated unit tests.
- Verify that all algorithms produce the same correctly sorted output.

### Example Validation Input

```python
[8, 3, 1, 6, 4]
```

### Expected Output

```python
[1, 3, 4, 6, 8]
```

### Additional Test Cases

```text
[]
[1]
[2, 1]
[1, 1, 1]
[-5, 3, 0, -2]
already sorted data
reverse-sorted data
duplicate values
```

### Expected Deliverables

- `bubble_sort.py`
- `selection_sort.py`
- `insertion_sort.py`
- `merge_sort.py`
- Algorithm unit tests

### Planned Git Commits

```bash
git commit -m "Implement bubble and selection sort algorithms"
git commit -m "Implement insertion and merge sort algorithms"
git commit -m "Add unit tests for sorting algorithms"
```

### Quality Gate

All four algorithms must pass correctness tests before performance benchmarking begins.

---

## Day 3 - Dataset Generator

### Major Objective

Create a reusable data generation module that produces all required benchmark datasets.

### Tasks

- Implement random dataset generation.
- Implement sorted dataset generation.
- Implement reverse-sorted dataset generation.
- Implement partially sorted dataset generation.
- Support configurable dataset sizes.
- Add reproducible random seeds.
- Add tests for dataset size and ordering characteristics.
- Document the dataset generation methodology.

### Planned Generator Interface

```python
generate_random(size)
generate_sorted(size)
generate_reverse_sorted(size)
generate_partially_sorted(size)
```

### Required Sizes

```python
SIZES = [1000, 5000, 10000, 50000]
```

### Expected Deliverables

- `data_generator.py`
- Dataset generator tests
- Dataset generation documentation

### Planned Git Commits

```bash
git commit -m "Implement benchmark dataset generator"
git commit -m "Add dataset types and reproducible random seeds"
git commit -m "Add tests for dataset generation"
```

### Quality Gate

Each generator must produce the expected number of values and preserve the intended dataset characteristics.

---

## Day 4 - Benchmark and Timing Engine

### Major Objective

Build an automated benchmarking system that executes, times, validates, and records sorting experiments.

### Tasks

- Create the timing utility.
- Use `time.perf_counter()` for execution timing.
- Build the benchmark runner.
- Automatically iterate through all algorithms.
- Automatically iterate through all dataset types.
- Automatically iterate through all dataset sizes.
- Copy input data before each algorithm runs so algorithms receive equivalent inputs.
- Validate every sorted result.
- Export benchmark results to CSV.

### Benchmark Workflow

```text
Generate Dataset
      |
      v
Copy Dataset
      |
      v
Start Timer
      |
      v
Run Sorting Algorithm
      |
      v
Stop Timer
      |
      v
Validate Sorted Output
      |
      v
Record Result
      |
      v
Save Results to CSV
```

### Planned Result Format

| Algorithm | Dataset Type | Size | Execution Time |
|---|---|---:|---:|
| Bubble Sort | Random | 1000 | Result |
| Merge Sort | Random | 1000 | Result |
| Insertion Sort | Sorted | 5000 | Result |

### Expected Deliverables

- `timer.py`
- `benchmark_runner.py`
- CSV result export
- Benchmark validation logic

### Planned Git Commits

```bash
git commit -m "Implement performance timing utility"
git commit -m "Build automated benchmark runner"
git commit -m "Add benchmark result CSV export"
```

### Quality Gate

Before full benchmark execution:

- Equivalent datasets must be used for algorithm comparisons.
- Dataset copies must prevent one algorithm from affecting another.
- The timer must measure sorting execution consistently.
- Output must be validated after every test.
- Results must save successfully to CSV.

---

## Day 5 - Full Performance Testing

### Major Objective

Execute the complete experiment set and produce the final performance dataset.

### Tasks

- Execute all 64 required benchmark combinations.
- Review suspicious or inconsistent measurements.
- Repeat tests where needed.
- Calculate average execution time if repeated trials are used.
- Compare algorithms by dataset size.
- Compare algorithms by dataset type.
- Identify the fastest algorithm for each scenario.
- Save the final benchmark results.

### Performance Consideration

Bubble Sort, Selection Sort, and Insertion Sort have O(n^2) worst-case behavior, while Merge Sort has O(n log n) behavior.

Large inputs, especially 50,000-element datasets, are therefore expected to produce major runtime differences. These differences are an important part of the project and should be documented rather than removed from the experiment.

### Expected Deliverables

- Completed benchmark results
- Final `benchmark_results.csv`
- Validated performance measurements
- Initial observations for the written analysis

### Planned Git Commits

```bash
git commit -m "Run complete sorting performance benchmark suite"
git commit -m "Add final performance testing results"
git commit -m "Add benchmark result validation"
```

### Quality Gate

All required combinations must either complete successfully or be documented clearly if a performance limitation is observed.

---

## Day 6 - Visualization, Analysis, and Recommendations

### Major Objective

Transform raw benchmark results into understandable charts, written findings, and practical recommendations.

### Tasks

- Load benchmark results from CSV.
- Create performance comparison charts.
- Create dataset-size comparison charts.
- Create dataset-type comparison charts.
- Identify the fastest algorithm for each tested scenario.
- Implement recommendation logic.
- Draft the 2-3 page performance analysis.
- Add a Big-O complexity comparison table.

### Recommended Charts

1. Execution Time vs. Dataset Size
2. Performance on Random Data
3. Performance on Sorted Data
4. Performance on Reverse-Sorted Data
5. Performance on Partially Sorted Data

### Main Comparison Chart

```text
X-axis: Number of Elements
Y-axis: Execution Time
Series: Sorting Algorithms
```

### Recommendation Logic

The final recommendation guide should use measured project results rather than relying only on theoretical complexity.

Initial logic to investigate:

```text
Small dataset
    -> Insertion Sort or Selection Sort may be acceptable

Nearly sorted dataset
    -> Insertion Sort may perform well

Large dataset
    -> Merge Sort should be investigated first

Performance-critical processing
    -> Favor the algorithm that demonstrates the strongest benchmark performance
```

### Expected Deliverables

- Performance charts
- `performance_analyzer.py`
- `recommendation.py`
- Initial written analysis
- Recommendation guide

### Planned Git Commits

```bash
git commit -m "Add performance visualization charts"
git commit -m "Implement sorting recommendation generator"
git commit -m "Add preliminary performance analysis"
```

### Quality Gate

Charts, tables, and recommendations must accurately reflect benchmark results.

---

## Day 7 - Final Testing, Documentation, and Release

### Major Objective

Complete quality assurance, finalize documentation, and prepare the first stable project release.

### Tasks

- Run the complete automated test suite.
- Verify every required deliverable.
- Refactor duplicated or unclear code.
- Complete the main README.
- Complete the 2-3 page written analysis.
- Complete the recommendation guide.
- Add selected charts to the project documentation.
- Complete the project retrospective.
- Review Git history.
- Create the first project release.

### Expected Deliverables

- Fully tested source code
- Final benchmark results
- Final charts
- Written performance analysis
- Recommendation guide
- Final README
- Retrospective
- Stable GitHub release

### Planned Git Commits

```bash
git commit -m "Complete project documentation"
git commit -m "Refactor code and finalize automated tests"
git commit -m "Add final performance analysis and recommendations"
git commit -m "Prepare SortBench v1.0 release"
```

### Planned Release

```text
v1.0.0
```

---

# Project Milestones

| Milestone | Target Day | Completion Requirement |
|---|---:|---|
| M1 - Project Architecture Complete | Day 1 | Repository, requirements, architecture, benchmark strategy |
| M2 - Sorting Algorithms Complete | Day 2 | Four algorithms implemented and tested |
| M3 - Dataset Generator Complete | Day 3 | Four dataset generators working |
| M4 - Benchmark Engine Complete | Day 4 | Automated timing and CSV export working |
| M5 - Performance Results Complete | Day 5 | Required benchmark suite completed |
| M6 - Analysis and Visualization Complete | Day 6 | Charts, analysis, and recommendations created |
| M7 - Final Release | Day 7 | Documentation, tests, and release completed |

---

# Testing Strategy

The project will use three levels of testing.

## 1. Unit Testing

Individual components will be tested independently.

Planned unit-test coverage includes:

- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Dataset Generator
- Timing utility
- Benchmark runner
- Recommendation logic

## 2. Correctness Testing

Every sorting result should be validated against Python's expected sorted result.

Example:

```python
result == sorted(original_data)
```

Testing should include:

- Empty lists
- Single values
- Duplicate values
- Negative values
- Sorted lists
- Reverse-sorted lists
- Random lists
- Large lists

## 3. Performance Testing

The complete required experiment matrix is:

```text
4 algorithms
x 4 dataset types
x 4 dataset sizes
= 64 scenarios
```

If repeated trials are introduced, the project should record individual runs or average execution times consistently.

---

# Benchmark Fairness Rules

To make the performance comparison meaningful:

1. Each algorithm should receive equivalent input data.
2. Input data should be copied before sorting.
3. The same machine and Python environment should be used for comparative runs.
4. Timing should focus on sorting execution rather than unrelated setup work.
5. Every sorted output should be validated.
6. Repeated measurements should use the same methodology.
7. Benchmark conditions should be documented in the final report.

---

# Required Documentation

The first version will keep documentation professional but lightweight.

```text
README.md
PROJECT_PLAN.md
REQUIREMENTS.md
ARCHITECTURE.md
TEST_PLAN.md
PERFORMANCE_ANALYSIS.md
RECOMMENDATION_GUIDE.md
RETROSPECTIVE.md
```

### Required Diagrams and Visuals

The project should include:

1. System Architecture Diagram
2. Benchmark Workflow Diagram
3. Performance Charts

Additional UML diagrams should only be added if they contribute directly to understanding the system.

---

# Written Performance Analysis Plan

The required 2-3 page analysis should be organized as follows.

## Introduction

Explain why algorithm selection matters for software performance and large-data processing.

## Bubble Sort

Discuss:

- basic behavior;
- O(n^2) complexity;
- implementation simplicity;
- scalability limitations;
- performance observed during testing.

## Selection Sort

Discuss:

- O(n^2) complexity;
- predictable comparison behavior;
- limited number of swaps;
- performance limitations on large inputs.

## Insertion Sort

Discuss:

- O(n^2) worst-case complexity;
- adaptive behavior;
- performance with small datasets;
- performance with already sorted or partially sorted data.

## Merge Sort

Discuss:

- O(n log n) complexity;
- scalability;
- additional memory requirements;
- performance on large datasets.

## Experimental Results

Use actual benchmark tables and charts produced by SortBench.

## Practical Recommendations

Explain which algorithms are appropriate for different data characteristics based on observed results and theoretical trade-offs.

## Conclusion

Summarize the main performance differences and explain why algorithm choice matters.

---

# Recommendation Guide Plan

The final recommendation guide should be based on measured results.

A starting structure is shown below.

| Scenario | Algorithm(s) to Investigate |
|---|---|
| Very small dataset | Insertion Sort / Selection Sort |
| Nearly sorted dataset | Insertion Sort |
| Random small dataset | Insertion Sort / Merge Sort |
| Reverse-sorted small dataset | Compare benchmark results |
| Large random dataset | Merge Sort |
| Large sorted dataset | Compare Merge Sort with adaptive behavior of Insertion Sort |
| Large reverse-sorted dataset | Merge Sort |
| Performance-critical processing | Use measured fastest scalable algorithm |
| Minimal implementation complexity | Bubble Sort / Selection Sort |
| Memory-sensitive scenario | Compare in-place algorithms with Merge Sort |

This table will be revised after the benchmark results are available.

---

# Release Checklist

Before the project is marked complete, verify the following items.

## Algorithms

- [ ] Bubble Sort implemented
- [ ] Selection Sort implemented
- [ ] Insertion Sort implemented
- [ ] Merge Sort implemented

## Dataset Generator

- [ ] Random dataset generator works
- [ ] Sorted dataset generator works
- [ ] Reverse-sorted dataset generator works
- [ ] Partially sorted dataset generator works

## Performance Testing

- [ ] 1,000-element testing complete
- [ ] 5,000-element testing complete
- [ ] 10,000-element testing complete
- [ ] 50,000-element testing complete
- [ ] All required benchmark scenarios recorded
- [ ] Correctness automatically validated
- [ ] CSV performance table generated

## Analysis and Visualization

- [ ] Performance charts generated
- [ ] Algorithm comparison completed
- [ ] Recommendation guide completed
- [ ] 2-3 page written analysis completed

## Code Quality and Documentation

- [ ] README completed
- [ ] Requirements documented
- [ ] Architecture documented
- [ ] Test plan completed
- [ ] Code comments and docstrings reviewed
- [ ] Automated tests passing
- [ ] Git history reviewed

## Release

- [ ] Final GitHub push completed
- [ ] Final results included
- [ ] Final charts included
- [ ] Retrospective completed
- [ ] `v1.0.0` release created

---

# Seven-Day Summary

| Day | Main Objective | Main Deliverable |
|---|---|---|
| Day 1 | Planning and Architecture | Repository, requirements, architecture |
| Day 2 | Sorting Algorithms | Four tested sorting algorithms |
| Day 3 | Dataset Generator | Four reusable dataset generators |
| Day 4 | Benchmark Engine | Automated timing and result storage |
| Day 5 | Performance Testing | Complete benchmark result dataset |
| Day 6 | Analysis and Visualization | Charts, analysis, recommendation logic |
| Day 7 | Quality Assurance and Release | Complete documented v1.0 project |

---

# Final Deliverables

At the end of the seven-day implementation, the repository should contain:

- Source code for all four sorting algorithms
- Dataset generator for all required dataset types
- Automated timing and benchmark system
- Performance testing result table
- CSV benchmark dataset
- Performance charts and graphs
- 2-3 page written performance analysis
- Algorithm recommendation guide
- Unit and correctness tests
- Architecture and testing documentation
- Git commit history showing incremental development
- Final `v1.0.0` release

---

# Future Portfolio Upgrade

The first version intentionally stays within the scope of a college software engineering project. After the seven-day implementation is complete, the same repository can be expanded into a stronger mid-level portfolio project.

Possible future enhancements include:

- Quick Sort
- Heap Sort
- Python built-in Timsort comparison
- Command-line interface
- Interactive dashboard
- Configurable benchmark experiments
- Multiple benchmark repetitions and statistical analysis
- Median, variance, and standard deviation reporting
- Memory-usage profiling
- Docker support
- GitHub Actions CI/CD
- Automated test coverage reports
- HTML or PDF performance reports
- Interactive Plotly visualizations
- Larger datasets
- Parallel experiment execution
- Benchmark history tracking

These enhancements are outside the scope of the first seven-day release.

---

## Project Status

**Current Phase:** Planning and Initial Implementation

**Target Version:** `v1.0.0`

**Expected Duration:** 7 development days

**Team Size:** 1 developer

---

## License

A license can be selected before the project is published publicly. An MIT License is a reasonable option for an educational portfolio project.
