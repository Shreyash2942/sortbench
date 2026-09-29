"""Merge Sort using recursive index ranges and one reusable merge buffer."""


def merge_sort(values: list[int]) -> list[int]:
    """Sort integers in ascending order and return the supplied list.

    Recursively sort each half and merge the halves back into the input.
    Time is O(n log n) for best, average, and worst cases. Extra space is O(n)
    for the buffer plus O(log n) recursion depth. Choosing the left value on
    ties preserves stability. The input list's identity is preserved, but
    this algorithm does not use constant auxiliary space.
    """
    if len(values) < 2:
        return values

    buffer = [0] * len(values)

    def sort_range(start: int, stop: int) -> None:
        """Sort the half-open range [start, stop)."""
        if stop - start < 2:
            return
        middle = (start + stop) // 2
        sort_range(start, middle)
        sort_range(middle, stop)

        left, right = start, middle
        for destination in range(start, stop):
            # Take the left item on equal values to keep the merge stable.
            if left < middle and (right >= stop or values[left] <= values[right]):
                buffer[destination] = values[left]
                left += 1
            else:
                buffer[destination] = values[right]
                right += 1
        for index in range(start, stop):
            values[index] = buffer[index]

    sort_range(0, len(values))
    return values
