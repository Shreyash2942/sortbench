"""Audit a persisted, complete single-trial assignment benchmark.

This checks saved evidence and coverage. Sorting correctness is checked during
execution by the runner; auditing the CSV does not rerun the algorithms.
"""

import csv
import json
import math
from datetime import datetime
from pathlib import Path

from data import SIZES

from .benchmark_runner import ALGORITHMS, CSV_FIELDS, DATASET_GENERATORS


def validate_results(csv_path: str | Path) -> list[dict]:
    """Return typed records only if CSV and metadata describe all 64 scenarios.

    Require one valid row per algorithm/type/required-size combination, trial 1,
    finite nonnegative timings, and consistent complete-run metadata. Explicit
    seed overrides are allowed but must match metadata for each size. Raise
    ValueError for malformed or inconsistent contents; file I/O errors propagate.
    Small smoke runs and partial runs deliberately fail this full-matrix audit.
    """
    path = Path(csv_path)
    metadata = json.loads(path.with_suffix(".metadata.json").read_text(encoding="utf-8"))
    if not isinstance(metadata, dict) or metadata.get("status") != "complete":
        raise ValueError("Metadata must describe a complete run")
    for field, expected in (("trial_count", 1), ("expected_rows", 64), ("completed_rows", 64)):
        if type(metadata.get(field)) is not int or metadata[field] != expected:
            raise ValueError(f"Metadata {field} must be {expected}")
    sizes = metadata.get("sizes")
    if (
        not isinstance(sizes, list) or len(sizes) != len(SIZES)
        or any(type(size) is not int for size in sizes) or set(sizes) != set(SIZES)
    ):
        raise ValueError("Metadata must contain each required size exactly once")
    if metadata.get("required_sizes_selected") is not True:
        raise ValueError("Metadata must identify the required sizes")
    if metadata.get("algorithms") != list(ALGORITHMS):
        raise ValueError("Metadata algorithm order does not match the experiment")
    if metadata.get("dataset_types") != list(DATASET_GENERATORS):
        raise ValueError("Metadata dataset order does not match the experiment")
    seeds = metadata.get("effective_seeds")
    if (
        not isinstance(seeds, dict) or set(seeds) != {str(size) for size in SIZES}
        or any(type(seed) is not int for seed in seeds.values())
    ):
        raise ValueError("Metadata must record one integer seed for each required size")
    if metadata.get("csv_file") != path.name:
        raise ValueError("Metadata CSV filename does not match")
    if metadata.get("timing_method") != "time.perf_counter; sorting call only; seconds":
        raise ValueError("Unexpected timing method or units")
    if metadata.get("execution_order") != "size, dataset type, algorithm; sequential; one trial":
        raise ValueError("Unexpected execution order in metadata")
    for field in ("python_version", "platform", "processor", "execution_order"):
        if not isinstance(metadata.get(field), str) or not metadata[field].strip():
            raise ValueError(f"Missing environment/method detail: {field}")
    try:
        start = datetime.fromisoformat(metadata["started_at_utc"])
        finish = datetime.fromisoformat(metadata["finished_at_utc"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Invalid run timestamps") from error
    if start.tzinfo is None or finish.tzinfo is None or finish < start:
        raise ValueError("Run timestamps must be timezone-aware and chronological")

    required = {
        (algorithm, dataset_type, size)
        for algorithm in ALGORITHMS
        for dataset_type in DATASET_GENERATORS
        for size in SIZES
    }
    seen = set()
    rows = []
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(CSV_FIELDS):
            raise ValueError("CSV header does not match the benchmark schema")
        for line, raw in enumerate(reader, start=2):
            if set(raw) != set(CSV_FIELDS) or any(value is None for value in raw.values()):
                raise ValueError(f"Malformed CSV row at line {line}")
            try:
                size, trial, seed = (int(raw[field]) for field in ("size", "trial", "seed"))
                elapsed = float(raw["execution_time_seconds"])
            except (TypeError, ValueError) as error:
                raise ValueError(f"Invalid numeric field at line {line}") from error
            key = (raw["algorithm"], raw["dataset_type"], size)
            if key not in required:
                raise ValueError(f"Unexpected scenario at line {line}: {key}")
            if key in seen:
                raise ValueError(f"Duplicate scenario at line {line}: {key}")
            if trial != 1 or raw["valid"] != "True":
                raise ValueError(f"Expected trial 1 and validated output at line {line}")
            if seed != seeds[str(size)]:
                raise ValueError(f"Seed mismatch at line {line}")
            if not math.isfinite(elapsed) or elapsed < 0:
                raise ValueError(f"Invalid elapsed time at line {line}")
            seen.add(key)
            rows.append({
                "algorithm": key[0], "dataset_type": key[1], "size": size,
                "trial": trial, "seed": seed, "execution_time_seconds": elapsed,
                "valid": True,
            })
    if seen != required:
        raise ValueError(f"Incomplete benchmark: missing {len(required - seen)} of 64 scenarios")
    expected_order = [
        (algorithm, dataset_type, size)
        for size in sizes for dataset_type in DATASET_GENERATORS for algorithm in ALGORITHMS
    ]
    if [(r["algorithm"], r["dataset_type"], r["size"]) for r in rows] != expected_order:
        raise ValueError("CSV scenario order does not match the documented execution order")
    return rows
