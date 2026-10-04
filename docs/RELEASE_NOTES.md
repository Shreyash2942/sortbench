# SortBench v1.0.0

SortBench compares how four sorting algorithms behave as integer datasets grow
and their ordering changes. This first release completes the seven-day
assignment's implementation, measurements, analysis, and documentation.

- Four manual sorting implementations: Bubble, Selection, Insertion, and Merge.
- Four reproducible dataset orderings at 1,000, 5,000, 10,000, and 50,000 elements.
- Sequential sorting-only timing with correctness validation and saved metadata.
- All 64 primary measurements, an independent audit, and preserved run history.
- Six performance charts, comparison tables, and exact-scenario recommendations.
- A three-page performance analysis, recommendation guide, and retrospective.
- 363 passing tests, including protection against overwriting analysis inputs.
- A dependency lock file verified in a clean Windows/Python 3.14.4 environment.

Merge Sort had the lowest recorded time in all 12 random, reverse-sorted, and
partially sorted groups. Bubble led three sorted groups and Insertion one.
These are single-trial observations, not statistical guarantees. A separate
diagnostic changed the sorted 10,000-element ranking. Memory trade-offs are
theoretical; memory was not profiled. The initial apparent-pause attempt and
diagnostic remain separate from the primary full repeat.

Read the [project documentation](https://github.com/Shreyash2942/sortbench/tree/v1.0.0)
for setup, reproduction commands, results, and limitations. The attached PDF
contains the final performance analysis. Additional algorithms, repeated-trial
statistics, CI, and an interactive interface remain future work.
