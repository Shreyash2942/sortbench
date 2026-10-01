"""Test timing boundaries, fair inputs, CSV persistence, and failure reporting."""

import csv
import json
import math
from itertools import product

import pytest

from benchmark import benchmark_runner as runner
from benchmark import timer
from data import SIZES


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def read_metadata(path):
    return json.loads(path.with_suffix(".metadata.json").read_text(encoding="utf-8"))


def sort_in_place(values):
    """Cheap controlled sorter for orchestration tests, not benchmark evidence."""
    values.sort()
    return values


def test_timer_preserves_result_and_brackets_sort_call(monkeypatch):
    events = []
    ticks = iter([100.0, 100.125])

    def clock():
        events.append("clock")
        return next(ticks)

    def sort(values):
        events.append("sort")
        return sort_in_place(values)

    monkeypatch.setattr(timer, "perf_counter", clock)
    values = [3, 1, 2]
    result, elapsed = timer.time_sort(sort, values)
    assert result is values
    assert result == [1, 2, 3]
    assert elapsed == 0.125
    assert events == ["clock", "sort", "clock"]


def test_timer_propagates_sorter_failure(monkeypatch):
    ticks = []
    monkeypatch.setattr(timer, "perf_counter", lambda: ticks.append(1) or 1.0)

    def fail(values):
        raise RuntimeError("sort failed")

    with pytest.raises(RuntimeError, match="sort failed"):
        timer.time_sort(fail, [2, 1])
    assert ticks == [1]


def test_small_real_run_exports_complete_cartesian_product(tmp_path):
    path = tmp_path / "nested" / "small.csv"
    rows = runner.run_benchmarks(path, sizes=[0, 1, 25])
    expected_keys = set(product([0, 1, 25], runner.DATASET_GENERATORS, runner.ALGORITHMS))
    assert {(row["size"], row["dataset_type"], row["algorithm"]) for row in rows} == expected_keys
    assert len(rows) == 48
    assert all(row["valid"] is True and row["trial"] == 1 for row in rows)
    assert all(math.isfinite(row["execution_time_seconds"]) and row["execution_time_seconds"] >= 0 for row in rows)
    assert all(row["seed"] == 506 + row["size"] for row in rows)
    disk_rows = read_rows(path)
    assert list(disk_rows[0]) == list(runner.CSV_FIELDS)
    assert len(disk_rows) == len(rows)
    for actual, expected in zip(disk_rows, rows):
        assert actual == {key: str(value) for key, value in expected.items()}
    metadata = read_metadata(path)
    assert metadata["status"] == "complete"
    assert metadata["expected_rows"] == metadata["completed_rows"] == 48
    assert metadata["required_sizes_selected"] is False
    assert metadata["effective_seeds"] == {"0": 506, "1": 507, "25": 531}
    assert metadata["python_version"] and metadata["platform"]
    assert metadata["finished_at_utc"] >= metadata["started_at_utc"]


def test_required_matrix_configuration_without_expensive_sorts(tmp_path, monkeypatch):
    # Keep real scenario names and sizes, but replace work with test doubles.
    # No such synthetic measurements leave pytest's temporary directory.
    generated = []

    def dataset(size, *, seed):
        generated.append((size, seed))
        return [2, 1]

    monkeypatch.setattr(runner, "ALGORITHMS", dict.fromkeys(runner.ALGORITHMS, sort_in_place))
    monkeypatch.setattr(runner, "DATASET_GENERATORS", dict.fromkeys(runner.DATASET_GENERATORS, dataset))
    rows = runner.run_benchmarks(tmp_path / "matrix.csv")
    assert len(rows) == 64
    assert [(r["size"], r["dataset_type"], r["algorithm"]) for r in rows] == list(
        product(SIZES, runner.DATASET_GENERATORS, runner.ALGORITHMS)
    )
    assert generated == [(size, 506 + size) for size in SIZES for _ in range(4)]
    assert read_metadata(tmp_path / "matrix.csv")["required_sizes_selected"] is True


def test_fresh_equivalent_inputs_for_every_algorithm(tmp_path, monkeypatch):
    originals = []
    inputs = []

    def dataset(size, *, seed):
        original = [3, 1, 2]
        originals.append(original)
        return original

    def sort(values):
        assert values == [3, 1, 2]
        inputs.append(values)  # Keep references so identity checks are meaningful.
        return sort_in_place(values)

    monkeypatch.setattr(runner, "DATASET_GENERATORS", {"controlled": dataset})
    monkeypatch.setattr(runner, "ALGORITHMS", {"first": sort, "second": sort})
    runner.run_benchmarks(tmp_path / "copies.csv", sizes=[3])
    assert originals == [[3, 1, 2]]
    assert inputs[0] is not inputs[1]
    assert all(values is not originals[0] for values in inputs)


def test_generation_copy_validation_and_csv_are_outside_timing(tmp_path, monkeypatch):
    events = []
    ticks = iter([1.0, 1.25])

    class WorkingList(list):
        def __ne__(self, other):
            events.append("validate")
            return list.__ne__(self, other)

    class OriginalList(list):
        def copy(self):
            events.append("copy")
            return WorkingList(self)

    def generate(size, *, seed):
        events.append("generate")
        return OriginalList([2, 1])

    def oracle(values):
        events.append("expected")
        return sorted(values)

    def clock():
        events.append("clock")
        return next(ticks)

    def sort(values):
        events.append("sort")
        return sort_in_place(values)

    writer_class = csv.DictWriter

    class RecordingWriter:
        def __init__(self, *args, **kwargs):
            self.writer = writer_class(*args, **kwargs)

        def writeheader(self):
            self.writer.writeheader()

        def writerow(self, row):
            events.append("csv")
            self.writer.writerow(row)

    monkeypatch.setattr(runner, "DATASET_GENERATORS", {"controlled": generate})
    monkeypatch.setattr(runner, "ALGORITHMS", {"controlled": sort})
    monkeypatch.setattr(runner, "sorted", oracle, raising=False)
    monkeypatch.setattr(timer, "perf_counter", clock)
    monkeypatch.setattr(runner.csv, "DictWriter", RecordingWriter)
    runner.run_benchmarks(tmp_path / "boundaries.csv", sizes=[2])
    assert events == ["generate", "expected", "copy", "clock", "sort", "clock", "validate", "csv"]


@pytest.mark.parametrize("seed", [0, -7, 123])
def test_custom_seed_is_recorded(tmp_path, seed):
    path = tmp_path / "seed.csv"
    rows = runner.run_benchmarks(path, sizes=[2, 3], seed=seed)
    assert {r["seed"] for r in rows} == {seed}
    assert read_metadata(path)["effective_seeds"] == {"2": seed, "3": seed}


@pytest.mark.parametrize("bad_sorter", [
    pytest.param(lambda values: values, id="unsorted"),
    pytest.param(lambda values: sorted(values), id="new-list"),
    pytest.param(lambda values: values.clear() or values, id="lost-values"),
    pytest.param(lambda values: values.__setitem__(slice(None), [1, 1]) or values, id="wrong-multiplicity"),
])
def test_reject_bad_output_and_keep_prior_valid_rows(tmp_path, monkeypatch, bad_sorter):
    path = tmp_path / "failed.csv"
    monkeypatch.setattr(runner, "DATASET_GENERATORS", {"controlled": lambda size, seed: [2, 1]})

    def fail_after_first(values):
        # Prior successful output must already be visible to another reader.
        assert len(read_rows(path)) == 1
        return bad_sorter(values)

    monkeypatch.setattr(runner, "ALGORITHMS", {"good": sort_in_place, "bad": fail_after_first})
    with pytest.raises(ValueError, match="bad, controlled, size=2"):
        runner.run_benchmarks(path, sizes=[2])
    rows = read_rows(path)
    assert len(rows) == 1 and rows[0]["algorithm"] == "good"
    metadata = read_metadata(path)
    assert metadata["status"] == "failed"
    assert metadata["completed_rows"] == 1
    assert metadata["failed_scenario"]["algorithm"] == "bad"
    assert metadata["finished_at_utc"]


@pytest.mark.parametrize("elapsed", [-1.0, float("nan"), float("inf")])
def test_reject_invalid_measurements(tmp_path, monkeypatch, elapsed):
    path = tmp_path / "invalid-time.csv"
    monkeypatch.setattr(runner, "time_sort", lambda sort, values: (sort(values), elapsed))
    with pytest.raises(ValueError, match="Invalid elapsed time"):
        runner.run_benchmarks(path, sizes=[2])
    assert read_rows(path) == []
    assert read_metadata(path)["status"] == "failed"


@pytest.mark.parametrize("error", [RuntimeError("sort failed"), KeyboardInterrupt()])
def test_exception_or_interrupt_is_recorded_and_raised(tmp_path, monkeypatch, error):
    def fail(values):
        raise error

    monkeypatch.setattr(runner, "ALGORITHMS", {"broken": fail})
    path = tmp_path / "exception.csv"
    with pytest.raises(type(error)):
        runner.run_benchmarks(path, sizes=[2])
    metadata = read_metadata(path)
    assert metadata["status"] == ("interrupted" if isinstance(error, KeyboardInterrupt) else "failed")
    assert metadata["completed_rows"] == 0
    assert metadata["failed_scenario"]["algorithm"] == "broken"
    assert read_rows(path) == []


def test_dataset_failure_is_recorded(tmp_path, monkeypatch):
    def fail(size, *, seed):
        raise RuntimeError("generation failed")

    monkeypatch.setattr(runner, "DATASET_GENERATORS", {"broken": fail})
    path = tmp_path / "dataset-failure.csv"
    with pytest.raises(RuntimeError, match="generation failed"):
        runner.run_benchmarks(path, sizes=[2])
    assert read_metadata(path)["failed_scenario"] == {"dataset_type": "broken", "size": 2, "seed": 508}


@pytest.mark.parametrize("existing", ["csv", "metadata"])
def test_existing_outputs_are_not_overwritten(tmp_path, existing):
    path = tmp_path / "existing.csv"
    existing_path = path if existing == "csv" else path.with_suffix(".metadata.json")
    existing_path.write_text("keep this", encoding="utf-8")
    with pytest.raises(FileExistsError):
        runner.run_benchmarks(path, sizes=[2])
    assert existing_path.read_text(encoding="utf-8") == "keep this"
    assert len(list(tmp_path.iterdir())) == 1


@pytest.mark.parametrize("sizes,exception", [
    ([], ValueError), ([2, 2], ValueError), ([-1], ValueError),
    ([True], TypeError), ([1.5], TypeError), (["2"], TypeError),
    ("1000", TypeError), (1000, TypeError),
])
def test_invalid_sizes_do_not_create_outputs(tmp_path, sizes, exception):
    with pytest.raises(exception):
        runner.run_benchmarks(tmp_path / "invalid.csv", sizes=sizes)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("seed", [True, "506", 1.5])
def test_invalid_seed_does_not_create_outputs(tmp_path, seed):
    with pytest.raises(TypeError, match="seed"):
        runner.run_benchmarks(tmp_path / "invalid.csv", sizes=[2], seed=seed)
    assert list(tmp_path.iterdir()) == []


def test_output_extension_is_validated_before_writing(tmp_path):
    with pytest.raises(ValueError, match=".csv"):
        runner.run_benchmarks(tmp_path / "invalid.json", sizes=[2])
    assert list(tmp_path.iterdir()) == []
