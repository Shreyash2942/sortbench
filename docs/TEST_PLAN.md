# Test plan

Day 1 validates the structure, imports, entry point, and runtime spike. The
test modules are placeholders; algorithm tests begin on Day 2. An empty test
suite is not a passing correctness suite.

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
