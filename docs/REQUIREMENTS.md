# SortBench requirements

Source: the supplied seven-day assignment plan, preserved in
[ASSIGNMENT_PLAN.md](ASSIGNMENT_PLAN.md). These are planned requirements;
Day 1 establishes the design and does not implement the benchmark.

## Functional requirements

| ID | Requirement | Acceptance evidence | Day |
|---|---|---|---:|
| F1 | Implement Bubble, Selection, Insertion, and Merge Sort manually. | Each algorithm passes the common correctness cases against `sorted(original)`. | 2 |
| F2 | Generate random, sorted, reverse-sorted, and partially sorted integer lists. | Tests verify size, intended ordering, and deterministic seeded output. | 3 |
| F3 | Support sizes 1,000, 5,000, 10,000, and 50,000. | Configuration and final CSV include every required size. | 3–5 |
| F4 | Time sorting with `time.perf_counter()`. | Timing excludes generation, copying, validation, and file output. | 4 |
| F5 | Give algorithms independent copies of equivalent data. | Tests show a run cannot alter the shared original input. | 4 |
| F6 | Validate every output for ordering and preservation of values. | Output equals `sorted(original)`; invalid output stops the run with context. | 4 |
| F7 | Execute and record all 64 combinations. | CSV coverage is exactly the product of four algorithms, four types, and four sizes. | 5 |
| F8 | Export results to CSV. | Each record identifies the algorithm, data type, size, trial, seed, elapsed seconds, and validity. | 4–5 |
| F9 | Create comparison tables and performance charts. | Labeled tables and charts derive from the validated CSV. | 6 |
| F10 | Produce a 2–3 page analysis and recommendation guide. | Conclusions cite measured results and discuss complexity and memory trade-offs. | 6–7 |
| F11 | Maintain documentation and incremental Git history. | Repository contains the planned documents, source, tests, and release artifacts. | 1–7 |

## Non-functional requirements

- **Correctness:** accept empty lists, single elements, duplicates, negative
  integers, and sorted/reverse-sorted lists. Python's built-in sorting is an
  independent validation oracle, not an algorithm implementation.
- **Reproducibility:** use local seeded random generators and record the Python
  version, platform, seed, and experiment method with the results.
- **Fairness:** run algorithms sequentially on the same machine and environment;
  use the same input values per dataset scenario and equal timing boundaries.
- **Maintainability:** keep sorting, data generation, timing, analysis, and
  plotting in separate, small modules with documented contracts.
- **Transparency:** distinguish measurements from projections; report slow or
  interrupted cases and never replace missing measurements with estimates.
- **Portability:** use Python 3 and relative project paths. Day 1 is verified
  with the local Python interpreter; additional versions are not yet validated.
- **Scope:** a local educational program with no database or hosted service.

The four required algorithms and sizes remain in scope even if large quadratic
cases are slow. CLI options, dashboards, additional algorithms, memory profiling,
and CI/CD belong to the future portfolio phase.
