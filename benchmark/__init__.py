"""Sorting-only timing and validated sequential benchmark execution."""

from .benchmark_runner import run_benchmarks
from .timer import time_sort

__all__ = ["time_sort", "run_benchmarks"]
