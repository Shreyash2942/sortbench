"""Run sequential sorting comparisons and persist only validated measurements."""

import csv
import json
import math
import platform
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

from algorithms import bubble_sort, insertion_sort, merge_sort, selection_sort
from data import (
    BASE_SEED,
    SIZES,
    generate_partially_sorted,
    generate_random,
    generate_reverse_sorted,
    generate_sorted,
)

from .timer import time_sort


# Insertion order defines the documented, sequential experiment order.
ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
}
DATASET_GENERATORS = {
    "random": generate_random,
    "sorted": generate_sorted,
    "reverse_sorted": generate_reverse_sorted,
    "partially_sorted": generate_partially_sorted,
}
CSV_FIELDS = (
    "algorithm", "dataset_type", "size", "trial", "seed",
    "execution_time_seconds", "valid",
)


def _validate_configuration(sizes: Sequence[int] | None, seed: int | None) -> list[int]:
    """Reject ambiguous scenario sets before creating any output files."""
    if sizes is not None and (
        not isinstance(sizes, Sequence) or isinstance(sizes, (str, bytes))
    ):
        raise TypeError("sizes must be a sequence of nonnegative integers")
    selected = list(SIZES if sizes is None else sizes)
    if not selected:
        raise ValueError("sizes must not be empty")
    if any(isinstance(size, bool) or not isinstance(size, int) for size in selected):
        raise TypeError("sizes must contain only nonnegative integers")
    if any(size < 0 for size in selected):
        raise ValueError("sizes must be nonnegative")
    if len(set(selected)) != len(selected):
        raise ValueError("sizes must not contain duplicates")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise TypeError("seed must be an integer or None")
    return selected


def _write_metadata(stream, metadata: dict) -> None:
    """Refresh this run's already reserved metadata file outside sort timing."""
    stream.seek(0)
    json.dump(metadata, stream, indent=2, allow_nan=False)
    stream.write("\n")
    stream.truncate()
    stream.flush()


def run_benchmarks(
    output_path: str | Path = "results/benchmark_results.csv",
    *,
    sizes: Sequence[int] | None = None,
    seed: int | None = None,
) -> list[dict]:
    """Run one trial of each algorithm/type/size combination and return its rows.

    None sizes selects the four assignment sizes (64 scenarios). Smaller sizes
    support verification runs. Each dataset is generated once per size/type,
    then each algorithm receives a fresh copy of those exact values. None seed
    means BASE_SEED + size; explicit integer seeds apply to every selected size.

    Create a new UTF-8 CSV plus <stem>.metadata.json, refusing to overwrite either
    existing file. Flush every validated row. On failure or KeyboardInterrupt,
    retain prior valid rows, record failure context in metadata, and re-raise.
    No retries, resume, parallel execution, or statistical aggregation occur.
    """
    selected_sizes = _validate_configuration(sizes, seed)
    output = Path(output_path)
    if output.suffix.lower() != ".csv":
        raise ValueError("output_path must have a .csv extension")
    metadata_path = output.with_suffix(".metadata.json")
    for path in (output, metadata_path):
        if path.exists():
            raise FileExistsError(f"Output already exists; choose a new path: {path}")

    metadata = {
        "status": "running",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "finished_at_utc": None,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported",
        "sizes": selected_sizes,
        "algorithms": list(ALGORITHMS),
        "dataset_types": list(DATASET_GENERATORS),
        "trial_count": 1,
        "effective_seeds": {
            str(size): BASE_SEED + size if seed is None else seed
            for size in selected_sizes
        },
        "required_sizes_selected": set(selected_sizes) == set(SIZES),
        "expected_rows": len(selected_sizes) * len(ALGORITHMS) * len(DATASET_GENERATORS),
        "completed_rows": 0,
        "timing_method": "time.perf_counter; sorting call only; seconds",
        "execution_order": "size, dataset type, algorithm; sequential; one trial",
        "csv_file": output.name,
    }
    rows = []
    scenario = {}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", newline="", encoding="utf-8") as csv_file, metadata_path.open(
        "x", encoding="utf-8"
    ) as metadata_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        csv_file.flush()
        _write_metadata(metadata_file, metadata)
        try:
            for size in selected_sizes:
                effective_seed = metadata["effective_seeds"][str(size)]
                for dataset_type, generate in DATASET_GENERATORS.items():
                    scenario = {"dataset_type": dataset_type, "size": size, "seed": effective_seed}
                    original = generate(size, seed=effective_seed)
                    expected = sorted(original)
                    for algorithm, sorter in ALGORITHMS.items():
                        scenario = {**scenario, "algorithm": algorithm}
                        working = original.copy()
                        context = f"{algorithm}, {dataset_type}, size={size}, seed={effective_seed}"
                        try:
                            result, elapsed = time_sort(sorter, working)
                        except Exception as error:
                            raise RuntimeError(f"Sorting failed ({context}): {error}") from error
                        if result is not working or result != expected:
                            raise ValueError(f"Invalid sorted output or list identity ({context})")
                        if not math.isfinite(elapsed) or elapsed < 0:
                            raise ValueError(f"Invalid elapsed time ({context}): {elapsed}")
                        row = {
                            "algorithm": algorithm, "dataset_type": dataset_type,
                            "size": size, "trial": 1, "seed": effective_seed,
                            "execution_time_seconds": elapsed, "valid": True,
                        }
                        writer.writerow(row)
                        csv_file.flush()
                        rows.append(row)
                        metadata["completed_rows"] = len(rows)
            metadata["status"] = "complete"
        except (Exception, KeyboardInterrupt) as error:
            metadata["status"] = "interrupted" if isinstance(error, KeyboardInterrupt) else "failed"
            metadata["error"] = f"{type(error).__name__}: {error}"
            metadata["failed_scenario"] = scenario.copy()
            raise
        finally:
            metadata["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
            _write_metadata(metadata_file, metadata)
    return rows
