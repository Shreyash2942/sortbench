"""Bubble Sort with an early exit when a pass makes no swaps."""


def bubble_sort(values: list[int]) -> list[int]:
    """Sort integers in ascending order and return the supplied list.

    Adjacent out-of-order values are swapped, placing the largest remaining
    value at the end of each pass. Time is O(n) for already sorted input and
    O(n^2) on average and in the worst case. Extra space is O(1).
    Equal values are not swapped, so the sort is stable.
    """
    for end in range(len(values) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]
                swapped = True
        if not swapped:
            break
    return values
