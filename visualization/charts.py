"""Render measured times with consistent colors and explicit units and scales."""

from pathlib import Path

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd

from benchmark.benchmark_runner import ALGORITHMS, DATASET_GENERATORS
from data import SIZES

COLORS = ("#0072B2", "#D55E00", "#009E73", "#CC79A7")
KINDS = {kind: kind.replace("_", " ").title() for kind in DATASET_GENERATORS}
TIME = "execution_time_seconds"
NOTE = "Source: audited CSV | One trial per scenario | No error bars or significance claims"


def _figure(width: float, height: float) -> Figure:
    figure = Figure(figsize=(width, height), layout="constrained")
    FigureCanvasAgg(figure)
    return figure


def _style(axis, values: pd.Series) -> None:
    # Zero is valid audit input and cannot be represented on a log axis.
    scale = "log" if values.gt(0).all() else "linear"
    axis.set_yscale(scale)
    axis.set_ylabel(f"Execution time (seconds; {scale} scale)")
    axis.grid(axis="y", alpha=0.2, which="both")
    axis.set_axisbelow(True)


def time_vs_size(results: pd.DataFrame, dataset_type: str | None = None) -> Figure:
    """Plot audited times for one ordering or all four, using actual numeric sizes."""
    if dataset_type is not None and dataset_type not in KINDS:
        raise ValueError(f"Unsupported dataset type: {dataset_type}")
    kinds = [dataset_type] if dataset_type is not None else list(KINDS)
    figure = _figure(11.7, 8.3) if len(kinds) == 4 else _figure(9, 5.8)
    axes = figure.subplots(2, 2).flat if len(kinds) == 4 else [figure.subplots()]
    for axis, kind in zip(axes, kinds):
        group = results.loc[results["dataset_type"] == kind]
        for algorithm, color in zip(ALGORITHMS, COLORS):
            series = group.loc[group["algorithm"] == algorithm].sort_values("size")
            axis.plot(series["size"], series[TIME], marker="o", linewidth=1.8,
                      markersize=4, label=algorithm, color=color)
        _style(axis, group[TIME])
        axis.set_xscale("log")
        axis.set_xticks(SIZES)
        axis.xaxis.set_major_formatter(ScalarFormatter())
        axis.set_xlabel("Number of elements (log scale)")
        axis.set_title(KINDS[kind])
        axis.legend(fontsize=8)
    figure.suptitle("SortBench: execution time vs. dataset size\n" + NOTE, fontsize=10)
    return figure


def dataset_comparison(results: pd.DataFrame) -> Figure:
    """Compare orderings at each measured size; marker height is recorded seconds."""
    figure = _figure(11.7, 8.3)
    positions = np.arange(len(KINDS))
    for axis, size in zip(figure.subplots(2, 2).flat, SIZES):
        group = results.loc[results["size"] == size]
        for index, (algorithm, color) in enumerate(zip(ALGORITHMS, COLORS)):
            series = group.loc[group["algorithm"] == algorithm].set_index("dataset_type").reindex(KINDS)
            axis.scatter(positions + (index - 1.5) * 0.14, series[TIME],
                         label=algorithm, color=color, s=35)
        _style(axis, group[TIME])
        axis.set_xticks(positions, ["Random", "Sorted", "Reverse", "Partial"])
        axis.set_xlabel("Dataset ordering (offsets separate algorithms)")
        axis.set_title(f"{size:,} elements")
        axis.legend(fontsize=8)
    figure.suptitle("SortBench: dataset ordering comparison\n" + NOTE, fontsize=10)
    return figure


def save_charts(results: pd.DataFrame, output_dir: str | Path) -> list[Path]:
    """Write six PNGs from audited records, releasing each figure after saving."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, kind in [("time_vs_size", None), *[(kind, kind) for kind in KINDS]]:
        figure = time_vs_size(results, kind)
        path = destination / f"{name}.png"
        figure.savefig(path, dpi=160)
        figure.clear()
        paths.append(path)
    figure = dataset_comparison(results)
    path = destination / "dataset_comparison.png"
    figure.savefig(path, dpi=160)
    figure.clear()
    return [*paths, path]
