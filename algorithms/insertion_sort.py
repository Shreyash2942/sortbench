"""Insertion Sort by shifting values within a sorted prefix."""


def insertion_sort(values: list[int]) -> list[int]:
    """Sort integers in ascending order and return the supplied list.

    Insert each value into the already sorted prefix, shifting larger values
    right. Time is O(n) for sorted input and O(n^2) on average and in the worst
    case. Extra space is O(1). Equal values are not shifted past one another,
    making this sort stable.
    """
    for index in range(1, len(values)):
        current = values[index]
        position = index - 1
        while position >= 0 and values[position] > current:
            values[position + 1] = values[position]
            position -= 1
        values[position + 1] = current
    return values
