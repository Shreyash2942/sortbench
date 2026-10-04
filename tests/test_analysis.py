"""Check measured summaries, conservative recommendations and chart data."""

import hashlib
import json

import pandas as pd
import pytest

from analysis.performance_analyzer import (
    PRIMARY_CSV, comparison_table, generate_analysis, growth_table,
    load_results, observed_winners,
)
from analysis.recommendation import recommend
from benchmark.benchmark_runner import ALGORITHMS, DATASET_GENERATORS
from data import SIZES
from visualization.charts import dataset_comparison, time_vs_size


@pytest.fixture
def measured():
    """Hand-computable synthetic records; never saved as benchmark evidence."""
    return pd.DataFrame([
        {"dataset_type": kind, "size": size, "algorithm": algorithm,
         "execution_time_seconds": float((index + 1) * size / 1000)}
        for kind in DATASET_GENERATORS for size in SIZES
        for index, algorithm in enumerate(ALGORITHMS)
    ])


def test_comparison_preserves_times_and_scenario_order(measured):
    table = comparison_table(measured.sample(frac=1, random_state=1))
    assert table.shape == (16, 4)
    assert list(table.columns) == list(ALGORITHMS)
    assert table.loc[("random", 5000)].tolist() == [5, 10, 15, 20]


def test_winners_keep_exact_ties(measured):
    measured.loc[1, "execution_time_seconds"] = 1
    winners = observed_winners(measured)
    assert len(winners) == 17
    group = winners.loc[(winners.dataset_type == "random") & (winners["size"] == 1000)]
    assert group.algorithm.tolist() == ["Bubble Sort", "Selection Sort"]


def test_growth_and_zero_baseline(measured):
    table = growth_table(measured)
    assert table.time_ratio.eq(50).all()
    measured.loc[0, "execution_time_seconds"] = 0
    table = growth_table(measured).set_index(["dataset_type", "algorithm"])
    assert pd.isna(table.loc[("random", "Bubble Sort"), "time_ratio"])


def test_recommendation_observed_winner_and_warning(measured):
    result = recommend(measured, "sorted", 10000)
    assert result["algorithms"] == ["Bubble Sort"]
    assert result["execution_time_seconds"] == 10
    assert result["tied"] is False
    assert "One trial" in result["limitation"]
    assert "diagnostic" in result["limitation"]


def test_recommendation_tie_and_zero_time(measured):
    measured.loc[[0, 1], "execution_time_seconds"] = 0
    result = recommend(measured, "random", 1000)
    assert result["algorithms"] == ["Bubble Sort", "Selection Sort"]
    assert result["tied"] is True
    assert result["execution_time_seconds"] == 0


@pytest.mark.parametrize("kind,size", [("unknown", 1000), ("random", 2000),
                                      ("random", True), ("random", 1000.0)])
def test_no_untested_recommendations(measured, kind, size):
    with pytest.raises(ValueError):
        recommend(measured, kind, size)


@pytest.mark.parametrize("damage", ["missing", "duplicate", "nan", "negative", "infinite"])
def test_recommendation_rejects_bad_group(measured, damage):
    if damage == "missing":
        measured = measured.drop(0)
    elif damage == "duplicate":
        measured = pd.concat([measured, measured.iloc[[0]]])
    else:
        measured.loc[0, "execution_time_seconds"] = {"nan": float("nan"),
            "negative": -1, "infinite": float("inf")}[damage]
    with pytest.raises(ValueError):
        recommend(measured, "random", 1000)


def test_size_chart_uses_actual_sizes_seconds_and_labels(measured):
    figure = time_vs_size(measured, "random")
    axis = figure.axes[0]
    assert len(axis.lines) == 4
    assert axis.get_xscale() == axis.get_yscale() == "log"
    for index, line in enumerate(axis.lines):
        assert list(line.get_xdata()) == SIZES
        assert list(line.get_ydata()) == [(index + 1) * size / 1000 for size in SIZES]
        assert line.get_label() == list(ALGORITHMS)[index]
    assert "seconds" in axis.get_ylabel()
    figure.clear()


def test_zero_chart_uses_linear_scale_without_altering_values(measured):
    measured.loc[0, "execution_time_seconds"] = 0
    figure = time_vs_size(measured, "random")
    assert figure.axes[0].get_yscale() == "linear"
    assert figure.axes[0].lines[0].get_ydata()[0] == 0
    figure.clear()


def test_dataset_chart_preserves_type_order_and_values(measured):
    figure = dataset_comparison(measured)
    assert len(figure.axes) == 4
    for axis, size in zip(figure.axes, SIZES):
        assert [t.get_text() for t in axis.get_xticklabels()] == ["Random", "Sorted", "Reverse", "Partial"]
        for index, collection in enumerate(axis.collections):
            assert list(collection.get_offsets()[:, 1]) == [(index + 1) * size / 1000] * 4
    figure.clear()


def test_real_pipeline_exports_all_scenarios_without_changing_source(tmp_path):
    before = PRIMARY_CSV.read_bytes()
    destination = generate_analysis(output_dir=tmp_path / "derived")
    assert PRIMARY_CSV.read_bytes() == before
    results = load_results()
    winners = observed_winners(results)
    assert winners.algorithm.value_counts().to_dict() == {
        "Merge Sort": 12, "Bubble Sort": 3, "Insertion Sort": 1,
    }
    saved = pd.read_csv(destination / "comparison.csv", index_col=[0, 1])
    pd.testing.assert_frame_equal(saved, comparison_table(results), check_names=False,
                                  check_exact=False, rtol=1e-12)
    recommendations = json.loads((destination / "recommendations.json").read_text())
    assert len(recommendations) == 16
    for result in recommendations:
        group = results.loc[(results.dataset_type == result["dataset_type"]) &
                            (results["size"] == result["size"])]
        assert result["execution_time_seconds"] == group.execution_time_seconds.min()
    assert len(list((destination / "charts").glob("*.png"))) == 6
    provenance = json.loads((destination / "provenance.json").read_text())
    assert provenance["source_files"][PRIMARY_CSV.name] == hashlib.sha256(before).hexdigest()
    for filename, digest in provenance["generated_files"].items():
        assert hashlib.sha256((destination / filename).read_bytes()).hexdigest() == digest


def test_pipeline_rejects_incomplete_input_before_creating_outputs(tmp_path):
    path = tmp_path / "incomplete.csv"
    path.write_bytes(PRIMARY_CSV.read_bytes())
    metadata = json.loads(PRIMARY_CSV.with_suffix(".metadata.json").read_text())
    metadata["status"] = "interrupted"
    path.with_suffix(".metadata.json").write_text(json.dumps(metadata))
    with pytest.raises(ValueError, match="complete"):
        generate_analysis(path, tmp_path / "derived")
    assert not (tmp_path / "derived").exists()


@pytest.mark.parametrize("filename", ["comparison.csv", "observed_winners.csv", "growth.csv",
                                      "recommendations.json", "provenance.json", "charts/random.png"])
def test_pipeline_refuses_to_overwrite_input_with_derived_table(tmp_path, filename):
    path = tmp_path / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    before = PRIMARY_CSV.read_bytes()
    path.write_bytes(before)
    metadata = json.loads(PRIMARY_CSV.with_suffix(".metadata.json").read_text())
    metadata["csv_file"] = path.name
    path.with_suffix(".metadata.json").write_text(json.dumps(metadata))
    with pytest.raises(ValueError, match="overwrite"):
        generate_analysis(path, tmp_path)
    assert path.read_bytes() == before
