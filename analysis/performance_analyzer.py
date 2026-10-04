"""Summarize the audited, single-trial benchmark without rerunning sorts."""

import hashlib
import json
from pathlib import Path

import pandas as pd

from benchmark.benchmark_runner import ALGORITHMS, DATASET_GENERATORS
from benchmark.result_validation import validate_results
from data import SIZES

ROOT = Path(__file__).resolve().parents[1]
PRIMARY_CSV = ROOT / "results" / "benchmark_results.csv"
TIME = "execution_time_seconds"


def load_results(csv_path: str | Path = PRIMARY_CSV) -> pd.DataFrame:
    """Audit the complete CSV and adjacent metadata before constructing a frame."""
    return pd.DataFrame(validate_results(csv_path))


def comparison_table(results: pd.DataFrame) -> pd.DataFrame:
    """Pivot audited records to 16 scenarios by four algorithms, in seconds.

    Consumers pass the unchanged output of load_results. No aggregation,
    interpolation, or averaging of separate runs is performed.
    """
    index = pd.MultiIndex.from_product(
        [DATASET_GENERATORS, SIZES], names=["dataset_type", "size"]
    )
    return results.pivot(
        index=["dataset_type", "size"], columns="algorithm", values=TIME
    ).reindex(index=index, columns=list(ALGORITHMS))


def observed_winners(results: pd.DataFrame) -> pd.DataFrame:
    """Return every exact minimum, including ties, with its raw recorded time."""
    minimum = results.groupby(["dataset_type", "size"])[TIME].transform("min")
    return results.loc[results[TIME].eq(minimum),
                       ["dataset_type", "size", "algorithm", TIME]].reset_index(drop=True)


def growth_table(results: pd.DataFrame) -> pd.DataFrame:
    """Compare 50k to 1k timings; a zero baseline has an undefined (NaN) ratio."""
    table = results.pivot(index=["dataset_type", "algorithm"], columns="size", values=TIME)
    output = table[[1000, 50000]].rename(columns={1000: "seconds_1000", 50000: "seconds_50000"})
    output["size_ratio"] = 50
    output["time_ratio"] = output["seconds_50000"].div(
        output["seconds_1000"].where(output["seconds_1000"].ne(0))
    )
    return output.reset_index()


def generate_analysis(csv_path: str | Path = PRIMARY_CSV,
                      output_dir: str | Path = ROOT / "results" / "analysis") -> Path:
    """Regenerate derived tables, recommendations, six PNG charts and provenance.

    Only derived files in output_dir are replaced. Primary/initial/diagnostic
    measurements are never modified. Invalid input fails before output creation.
    """
    from analysis.recommendation import recommend
    from visualization.charts import save_charts

    path, destination = Path(csv_path), Path(output_dir)
    results = load_results(path)
    table_names = ("comparison.csv", "observed_winners.csv", "growth.csv", "recommendations.json")
    if path.resolve() in {(destination / name).resolve() for name in table_names}:
        raise ValueError("The output directory would overwrite the input CSV")
    destination.mkdir(parents=True, exist_ok=True)
    comparison_table(results).to_csv(destination / "comparison.csv")
    observed_winners(results).to_csv(destination / "observed_winners.csv", index=False)
    growth_table(results).to_csv(destination / "growth.csv", index=False)
    recommendations = [recommend(results, kind, size)
                       for kind in DATASET_GENERATORS for size in SIZES]
    (destination / "recommendations.json").write_text(
        json.dumps(recommendations, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    chart_paths = save_charts(results, destination / "charts")
    import matplotlib
    source_files = [path, path.with_suffix(".metadata.json")]
    generated_files = sorted([*(destination / name for name in table_names), *chart_paths])
    provenance = {
        "source_files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
        "row_count": len(results), "trial_count_per_scenario": 1,
        "method": "Exact recorded times; no averaging, interpolation, or statistical inference",
        "pandas_version": pd.__version__, "matplotlib_version": matplotlib.__version__,
        "generated_files": {p.relative_to(destination).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in generated_files},
    }
    (destination / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    return destination


if __name__ == "__main__":
    print(f"Generated analysis: {generate_analysis()}")
