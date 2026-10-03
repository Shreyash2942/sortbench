"""Reject corrupt or incomplete benchmark evidence without running expensive sorts."""

import csv
import json

import pytest

from benchmark.benchmark_runner import ALGORITHMS, CSV_FIELDS, DATASET_GENERATORS
from benchmark.result_validation import validate_results
from data import SIZES


@pytest.fixture
def saved_run(tmp_path):
    """Synthetic evidence stays in pytest's temporary directory only."""
    path = tmp_path / "synthetic.csv"
    rows = [
        {"algorithm": algorithm, "dataset_type": kind, "size": size,
         "trial": 1, "seed": 506 + size, "execution_time_seconds": 0.125, "valid": True}
        for size in SIZES for kind in DATASET_GENERATORS for algorithm in ALGORITHMS
    ]
    metadata = {
        "status": "complete", "trial_count": 1, "expected_rows": 64, "completed_rows": 64,
        "sizes": SIZES.copy(), "required_sizes_selected": True,
        "algorithms": list(ALGORITHMS), "dataset_types": list(DATASET_GENERATORS),
        "effective_seeds": {str(size): 506 + size for size in SIZES},
        "csv_file": path.name, "timing_method": "time.perf_counter; sorting call only; seconds",
        "python_version": "test version", "platform": "test platform", "processor": "test CPU",
        "execution_order": "size, dataset type, algorithm; sequential; one trial",
        "started_at_utc": "2026-10-02T12:00:00+00:00",
        "finished_at_utc": "2026-10-02T12:01:00+00:00",
    }
    return path, rows, metadata


def save(run):
    path, rows, metadata = run
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    path.with_suffix(".metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
    return path


def test_accepts_complete_required_matrix(saved_run):
    rows = validate_results(save(saved_run))
    assert rows == saved_run[1]
    assert len(rows) == 64


def test_accepts_consistent_seed_override(saved_run):
    path, rows, metadata = saved_run
    metadata["effective_seeds"] = {str(size): 0 for size in SIZES}
    for row in rows:
        row["seed"] = 0
    assert len(validate_results(save(saved_run))) == 64


@pytest.mark.parametrize("field,value,match", [
    ("status", "running", "complete"),
    ("status", "interrupted", "complete"),
    ("completed_rows", 63, "completed_rows"),
    ("expected_rows", 32, "expected_rows"),
    ("trial_count", True, "trial_count"),
    ("trial_count", 2, "trial_count"),
    ("sizes", [1000, 5000, 10000, 10000], "size"),
    ("required_sizes_selected", False, "required sizes"),
    ("algorithms", [], "algorithm"),
    ("dataset_types", [], "dataset"),
    ("effective_seeds", {}, "seed"),
    ("csv_file", "wrong.csv", "filename"),
    ("timing_method", "milliseconds", "timing"),
    ("execution_order", "parallel", "execution order"),
    ("python_version", "", "environment"),
    ("finished_at_utc", None, "timestamp"),
    ("finished_at_utc", "2026-10-01T00:00:00+00:00", "chronological"),
    ("started_at_utc", "2026-10-02T12:00:00", "timezone"),
])
def test_rejects_inconsistent_metadata(saved_run, field, value, match):
    saved_run[2][field] = value
    with pytest.raises(ValueError, match=match):
        validate_results(save(saved_run))


@pytest.mark.parametrize("field,value,match", [
    ("algorithm", "Unknown Sort", "Unexpected"),
    ("dataset_type", "missing", "Unexpected"),
    ("size", 10, "Unexpected"),
    ("size", "1000.5", "numeric"),
    ("trial", 2, "trial"),
    ("seed", 0, "Seed"),
    ("valid", False, "validated"),
    ("execution_time_seconds", "nan", "elapsed"),
    ("execution_time_seconds", "inf", "elapsed"),
    ("execution_time_seconds", -1, "elapsed"),
    ("execution_time_seconds", "invalid", "numeric"),
])
def test_rejects_invalid_rows(saved_run, field, value, match):
    saved_run[1][0][field] = value
    with pytest.raises(ValueError, match=match):
        validate_results(save(saved_run))


def test_rejects_missing_scenario(saved_run):
    saved_run[1].pop()
    with pytest.raises(ValueError, match="missing 1"):
        validate_results(save(saved_run))


def test_rejects_duplicate_even_when_count_is_64(saved_run):
    saved_run[1][-1] = saved_run[1][0].copy()
    with pytest.raises(ValueError, match="Duplicate"):
        validate_results(save(saved_run))


def test_rejects_mismatched_scenario_order(saved_run):
    saved_run[1].reverse()
    with pytest.raises(ValueError, match="order"):
        validate_results(save(saved_run))


def test_rejects_wrong_header(saved_run):
    path = save(saved_run)
    path.write_text("wrong,header\n", encoding="utf-8")
    with pytest.raises(ValueError, match="header"):
        validate_results(path)


@pytest.mark.parametrize("row", ["Bubble Sort,random\n", "Bubble Sort,random,1000,1,1506,0.1,True,extra\n"])
def test_rejects_malformed_row(saved_run, row):
    path = save(saved_run)
    path.write_text(",".join(CSV_FIELDS) + "\n" + row, encoding="utf-8")
    with pytest.raises(ValueError, match="Malformed"):
        validate_results(path)
