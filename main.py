"""Demonstrate the four sorters; benchmark execution will be added on Day 4."""

from algorithms import bubble_sort, insertion_sort, merge_sort, selection_sort


def main() -> None:
    """Sort the assignment example with independent inputs for each algorithm."""
    print("SortBench - Sorting Algorithm Performance Analyzer")
    print("Day 2: all four sorting algorithms are implemented and tested.")
    original = [8, 3, 1, 6, 4]
    print(f"Input: {original}")
    for sort in (bubble_sort, selection_sort, insertion_sort, merge_sort):
        print(f"{sort.__name__}: {sort(original.copy())}")
    print("Next: implement the dataset generators on Day 3.")
    print("See docs/PROJECT_PLAN.md for the development checklist.")


if __name__ == "__main__":
    main()
