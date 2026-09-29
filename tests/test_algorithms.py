"""Check every sorter against an independent oracle and its mutation contract."""

import random
from itertools import product

import pytest

from algorithms import bubble_sort, insertion_sort, merge_sort, selection_sort


SORTERS = [bubble_sort, selection_sort, insertion_sort, merge_sort]


@pytest.fixture(params=SORTERS, ids=lambda sorter: sorter.__name__)
def sorter(request):
    """Run the same behavioral checks for all four implementations."""
    return request.param


@pytest.mark.parametrize(
    "original",
    [
        pytest.param([], id="empty"),
        pytest.param([1], id="singleton"),
        pytest.param([2, 1], id="two-reversed"),
        pytest.param([1, 2], id="two-sorted"),
        pytest.param([1, 1, 1], id="all-equal"),
        pytest.param([-5, 3, 0, -2], id="mixed-signs"),
        pytest.param([-1, -9, -3, -9], id="negative-duplicates"),
        pytest.param([8, 3, 1, 6, 4], id="assignment-example"),
        pytest.param([4, 1, 4, 0, 1, 4], id="duplicates"),
        pytest.param(list(range(33)), id="sorted-odd-length"),
        pytest.param(list(range(32, -1, -1)), id="reversed-odd-length"),
        pytest.param([1, 2, 4, 3, 5, 6], id="nearly-sorted"),
        pytest.param([10**30, 0, -(10**30), 10**30], id="large-integers"),
    ],
)
def test_sorting_contract(sorter, original):
    working = original.copy()
    expected = sorted(original)

    result = sorter(working)

    assert result is working
    assert working == expected


def test_all_short_lists(sorter):
    """Exhaust small duplicate-heavy lists to expose boundary/merge mistakes."""
    for size in range(6):
        for items in product((-1, 0, 1), repeat=size):
            working = list(items)
            result = sorter(working)
            assert result is working
            assert result == sorted(items), items


@pytest.mark.parametrize("size", [3, 16, 31, 64, 127, 256, 1000])
def test_seeded_random_inputs(sorter, size):
    rng = random.Random(506 + size)
    working = [rng.randint(-size, size) for _ in range(size)]
    expected = sorted(working)

    result = sorter(working)

    assert result is working
    assert result == expected


def test_repeated_calls_are_independent(sorter):
    first = [9, -1, 4, 4]
    second = [2, 0, -3]
    assert sorter(first) is first
    assert sorter(second) is second
    assert sorter(first) is first
    assert first == [-1, 4, 4, 9]
    assert second == [-3, 0, 2]


class CountedInt(int):
    """Count comparisons without relying on noisy elapsed-time thresholds."""

    comparisons = 0

    def __gt__(self, other):
        type(self).comparisons += 1
        return int.__gt__(self, other)


@pytest.mark.parametrize("sort", [bubble_sort, insertion_sort])
def test_sorted_input_requires_one_linear_pass(sort):
    values = [CountedInt(value) for value in range(100)]
    CountedInt.comparisons = 0

    result = sort(values)

    assert result is values
    assert values == list(range(100))
    assert CountedInt.comparisons == len(values) - 1


@pytest.mark.parametrize("sort", [bubble_sort, insertion_sort, merge_sort])
def test_stable_sorts_preserve_equal_value_order(sort):
    # Distinct objects with equal numeric values reveal movement across ties.
    values = [CountedInt(value) for value in [2, 1, 2, 1, 2, 0, 1]]
    expected = sorted(values)

    result = sort(values)

    assert result is values
    assert [id(value) for value in result] == [id(value) for value in expected]
