"""Demonstrate sorting and datasets; see the runner guide for benchmark runs."""

from algorithms import bubble_sort, insertion_sort, merge_sort, selection_sort
from data import (
    generate_partially_sorted,
    generate_random,
    generate_reverse_sorted,
    generate_sorted,
)


def main() -> None:
    """Show the assignment's sorting example and reproducible dataset types."""
    print("SortBench - Sorting Algorithm Performance Analyzer")
    print("Day 4: sorting, datasets, timing, and CSV benchmark export are ready.")
    original = [8, 3, 1, 6, 4]
    print(f"Input: {original}")
    for sort in (bubble_sort, selection_sort, insertion_sort, merge_sort):
        print(f"{sort.__name__}: {sort(original.copy())}")
    print("Dataset examples (20 values each, seed=0):")
    for generate in (
        generate_random,
        generate_sorted,
        generate_reverse_sorted,
        generate_partially_sorted,
    ):
        print(f"{generate.__name__}: {generate(20, seed=0)}")
    print("See docs/BENCHMARK_RUNNER.md to run a small or full benchmark.")
    print("Next: execute the full performance experiment on Day 5.")
    print("See docs/PROJECT_PLAN.md for the development checklist.")


if __name__ == "__main__":
    main()
