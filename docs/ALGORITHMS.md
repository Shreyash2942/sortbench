# Day 2 sorting algorithms

All four functions accept `list[int]`, arrange values in ascending order,
modify the supplied list, and return that same object. Empty lists, duplicates,
and negative integers are supported. No implementation calls `sorted()` or
`list.sort()`; the tests use `sorted()` as an independent correctness oracle.

| Algorithm | Approach | Best time | Average time | Worst time | Extra space | Stable |
|---|---|---|---|---|---|---|
| Bubble Sort | Swap adjacent inversions; stop after a pass with no swaps | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | Select the smallest value in the remaining suffix | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | Shift larger prefix values right to insert the next value | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | Recursively split index ranges and merge sorted halves | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |

These are theoretical bounds for the implementations, not measured project
results. Stability means retaining the original relative order of equal keys.
Selection Sort's distant swaps do not preserve that property.

## Implementation notes

- **Bubble Sort:** each pass places the largest remaining value at the end.
  The next pass excludes that settled position. Only strict inversions swap,
  so equal values retain their order.
- **Selection Sort:** each pass scans the remaining suffix and performs a swap
  only when its minimum is not already at the start. It performs at most n − 1
  swaps, but still scans the suffix even when the input is already sorted.
- **Insertion Sort:** before each iteration, the prefix is sorted. Larger
  values shift right until the current value reaches its insertion position.
- **Merge Sort:** half-open index ranges avoid allocating recursive slices.
  One O(n) buffer is allocated per call and reused by all merges; recursion adds
  O(log n) stack depth. Taking the left item on ties makes merging stable.
  Returning the original list does not imply O(1) auxiliary space.

Inputs are expected to be integer lists as specified by the project. The
algorithms do not add per-element type validation to the future timed path.
They hold no global state, so independent calls do not share working storage.

## Example and validation

```python
from algorithms import bubble_sort, selection_sort, insertion_sort, merge_sort

original = [8, 3, 1, 6, 4]
for sort in (bubble_sort, selection_sort, insertion_sort, merge_sort):
    working = original.copy()
    result = sort(working)
    assert result is working
    assert result == [1, 3, 4, 6, 8]
```

Run `python main.py` for the demonstration and `python -m pytest -q` for the
test suite in the configured environment. Day 2 has 93 passing tests; see
[TEST_PLAN.md](TEST_PLAN.md) for coverage. The complete 64-scenario performance
experiment is recorded in `results/benchmark_results.csv`; the final
interpretation is in [PERFORMANCE_ANALYSIS.md](PERFORMANCE_ANALYSIS.md).
