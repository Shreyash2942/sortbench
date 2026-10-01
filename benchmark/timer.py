"""Measure the sorting call with Python's monotonic performance counter."""

from collections.abc import Callable
from time import perf_counter


def time_sort(
    sorter: Callable[[list[int]], list[int]], values: list[int]
) -> tuple[list[int], float]:
    """Return the sorter's result and elapsed seconds for an already copied list.

    Generation, copying, validation, and persistence belong to the caller.
    Allocations inside the sorter are included. Sorter exceptions propagate;
    failed calls do not produce a timing result.
    """
    start = perf_counter()
    result = sorter(values)
    elapsed = perf_counter() - start
    return result, elapsed
