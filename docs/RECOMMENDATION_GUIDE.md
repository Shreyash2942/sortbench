# Measured recommendation guide

These recommendations use the complete Day 5 repeat: one trial per scenario.
They identify observed minima, not statistically established universal winners.
The initial attempt and separate diagnostic are excluded from these rankings.

| Dataset type | Elements | Observed recommendation | Seconds |
|---|---:|---|---:|
| random | 1,000 | Merge Sort | 0.0009685 |
| random | 5,000 | Merge Sort | 0.0055772 |
| random | 10,000 | Merge Sort | 0.0118036 |
| random | 50,000 | Merge Sort | 0.0731335 |
| sorted | 1,000 | Bubble Sort | 0.0000260 |
| sorted | 5,000 | Bubble Sort | 0.0001238 |
| sorted | 10,000 | Insertion Sort | 0.0004652 |
| sorted | 50,000 | Bubble Sort | 0.0012729 |
| reverse_sorted | 1,000 | Merge Sort | 0.0008308 |
| reverse_sorted | 5,000 | Merge Sort | 0.0050288 |
| reverse_sorted | 10,000 | Merge Sort | 0.0111588 |
| reverse_sorted | 50,000 | Merge Sort | 0.0631464 |
| partially_sorted | 1,000 | Merge Sort | 0.0008886 |
| partially_sorted | 5,000 | Merge Sort | 0.0117023 |
| partially_sorted | 10,000 | Merge Sort | 0.0113740 |
| partially_sorted | 50,000 | Merge Sort | 0.0819030 |

## Choosing within the measured scope

Merge Sort was fastest for every tested random, reverse-sorted, and partially
sorted group. Its O(n) auxiliary buffer is a theoretical storage cost; this
study measured elapsed time, not memory consumption. Bubble won three sorted
groups and Insertion one. At sorted 10,000, a separate diagnostic reversed
their primary ranking with only about 1.2 microseconds between them. Treat
Bubble and Insertion as adaptive candidates on already sorted input rather
than claiming a dependable advantage from a single short observation.

Insertion benefited from partial ordering but did not beat Merge under the
specified random-swap construction. For memory-sensitive work, Bubble,
Selection and Insertion use O(1) extra storage; choose among them with
attention to ordering and required stability. Selection is unstable and won
none of these groups. Its limited swap count may matter in other workloads,
but that trade-off was not measured here. Bubble, Insertion and Merge are
stable in these implementations.

The smallest tested size is 1,000. No measured claim is made for tiny arrays,
untested sizes, different partial-order definitions, other hardware, or other
sorting algorithms. A memory limit, stability requirement, or costly element
comparison needs separate assessment; this API ranks elapsed time only.

## Using the recommendation function

```python
from analysis.performance_analyzer import load_results
from analysis.recommendation import recommend

results = load_results()
choice = recommend(results, "random", 50000)
print(choice["algorithms"])  # ['Merge Sort']
print(choice["limitation"])
```

Every exact minimum is returned in `algorithms`; `tied` reports multiple
identical recorded minima. No arbitrary tolerance converts near-ties into
ties. Unsupported sizes/types, missing or duplicate algorithm measurements,
and invalid times raise `ValueError`. The frame must come from `load_results`,
which validates the complete matrix and metadata before recommendations.

Machine-readable outputs are in
[recommendations.json](../results/analysis/recommendations.json). See the
[analysis workflow](ANALYSIS_WORKFLOW.md) to reproduce them and the
[performance analysis](PERFORMANCE_ANALYSIS.md) for interpretation.
