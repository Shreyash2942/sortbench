"""Identify observed winners for exact tested scenarios; do not extrapolate."""

import pandas as pd

from benchmark.benchmark_runner import ALGORITHMS, DATASET_GENERATORS
from data import SIZES


def recommend(results: pd.DataFrame, dataset_type: str, size: int) -> dict:
    """Recommend all tied minima from an audited frame returned by load_results.

    Unsupported scenarios and missing algorithm measurements raise ValueError.
    Exact equality defines a recorded tie, not statistical equivalence. Memory
    use and stability are separate theoretical trade-offs, not measured filters.
    """
    if dataset_type not in DATASET_GENERATORS:
        raise ValueError(f"Unsupported dataset type: {dataset_type}")
    if type(size) is not int or size not in SIZES:
        raise ValueError(f"No measured recommendation for size {size!r}; use {SIZES}")
    group = results.loc[(results["dataset_type"] == dataset_type) & (results["size"] == size)]
    if len(group) != len(ALGORITHMS) or set(group["algorithm"]) != set(ALGORITHMS):
        raise ValueError("Recommendation requires one measurement per algorithm")
    times = group.set_index("algorithm")["execution_time_seconds"].reindex(ALGORITHMS)
    if times.isna().any() or not times.map(lambda t: 0 <= t < float("inf")).all():
        raise ValueError("Recommendation requires finite nonnegative timings")
    fastest = float(times.min())
    winners = times.index[times.eq(fastest)].tolist()
    warning = "One trial on one machine; this observed minimum is not a statistically established advantage."
    if dataset_type == "sorted":
        warning += " Bubble/Insertion ranking changed at 10,000 elements in the separate Day 5 diagnostic."
    return {
        "dataset_type": dataset_type, "size": size, "algorithms": winners,
        "execution_time_seconds": fastest, "tied": len(winners) > 1,
        "basis": "Exact scenario in the supplied audited single-trial dataset",
        "limitation": warning,
    }
