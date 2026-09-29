"""Selection Sort using minimum-element selection."""


def selection_sort(values: list[int]) -> list[int]:
    """Sort integers in ascending order and return the supplied list.

    Select the minimum of each unsorted suffix and swap it into position.
    Time is O(n^2) for best, average, and worst cases, with at most n - 1
    swaps and O(1) extra space. Nonadjacent swaps make this sort unstable.
    """
    for start in range(len(values) - 1):
        minimum = start
        for index in range(start + 1, len(values)):
            if values[index] < values[minimum]:
                minimum = index
        if minimum != start:
            values[start], values[minimum] = values[minimum], values[start]
    return values
