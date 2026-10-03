# Test plan

Day 1 validated the structure, imports, entry point, and runtime spike.
Day 2 implemented `tests/test_algorithms.py`: **93 algorithm tests pass**.
Day 3 adds **175 dataset and integration tests** in `tests/test_data_generator.py`.
Day 4 adds **33 timer and benchmark tests** in `tests/test_benchmark.py`.
Day 5 adds **37 persisted-result audit tests** in `tests/test_result_validation.py`.
The complete suite has **338 passing tests** with Python 3.14.4.

The suite checks each algorithm against Python's `sorted()` and verifies that
the returned object is the supplied list. It covers 13 named edge cases, every
list of length 0–5 over `{-1, 0, 1}` (364 inputs per algorithm), seven seeded
random sizes up to 1,000, and repeated independent calls. Additional checks
verify one linear comparison pass for already sorted Bubble/Insertion inputs
and preservation of equal-value order for Bubble, Insertion, and Merge Sort.
Selection Sort makes no stability guarantee. These are correctness checks;
they do not establish measured performance rankings.

Dataset checks exercise all four required sizes, including 50,000, plus zero,
singleton, and the 19/20-element swap boundary. They verify integer value bounds,
ordering, multiset preservation, seeded reference outputs, default/explicit seed
equivalence, fresh list storage, input validation, and unchanged global random
state. Golden swap sequences check both a single swap and repeated swaps that
reuse an index. Small integration cases run every sorter on every dataset type;
large quadratic sorting benchmarks are not part of this suite.

Benchmark tests use a controlled clock to verify exact timing boundaries,
exercise real small-input runs and CSV round-tripping, and check input isolation,
seed recording, bad-result rejection, and metadata. Errors, keyboard interrupts,
and existing-output protection are covered. A test with cheap test doubles
verifies all 64 required configuration keys without running large quadratic
sorts; its synthetic rows exist only in pytest's temporary directory. The
separate committed Day 4 smoke CSV contains 32 actual measurements on sizes
10 and 100. Neither is the final Day 5 experiment.

Day 5 tests reject missing/duplicate/unexpected scenarios, malformed CSV,
invalid timing values, inconsistent seeds, incorrect trial/valid flags,
non-complete metadata, invalid timestamps, and mismatched row order. Synthetic
fixtures remain in temporary directories. The actual primary results also
passed the audit: all 64 unique required scenarios are present, with no invalid
sorting outputs reported during execution. This file audit does not rerun sorts.

| Stage | Checks | Acceptance |
|---|---|---|
| Day 2: algorithms | Empty, singleton, two values, duplicates, negatives, sorted, reversed, seeded random inputs; example `[8, 3, 1, 6, 4]`. | Every output equals `sorted(original)`, modifies the supplied list, and returns that list. |
| Day 3: datasets | Zero and positive sizes, invalid sizes, same-seed reproducibility, sorted/reversed order, equal multisets, specified partial swaps. | All four constructors follow the documented definitions and do not alter global random state. |
| Day 4: timer | Controlled callable and clock values; no real elapsed-time threshold assertions. | Difference is calculated correctly; only the sorting call is inside the timer boundaries. |
| Day 4: runner | Small inputs, separate copies, deliberately incorrect sorter, CSV schema, scenario coverage. | Original data remains unchanged; bad output is rejected; valid records round-trip through CSV. |
| Day 5: performance | All 64 required scenarios; nonnegative finite times and complete keys. | Coverage is complete or limitations are explicitly listed; no invented measurements. |
| Day 6: analysis | Known small result table, tied winners, missing data, chart labels and units. | Summaries and recommendations match measured inputs. |
| Day 7: regression | Complete suite, documented setup, final artifacts. | Tests pass and deliverables match the assignment. |

Run implemented tests from the repository root with `python -m pytest`. Keep
the expensive 50,000-element timing experiments separate from ordinary unit
tests. Compare values against the built-in sorting oracle; never assert that a
specific algorithm must finish within a fixed wall-clock threshold.
