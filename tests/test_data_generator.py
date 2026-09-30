"""Verify dataset contracts independently of sorting benchmark execution."""

import random
from collections import Counter

import pytest

from algorithms import bubble_sort, insertion_sort, merge_sort, selection_sort
from data import (
    BASE_SEED,
    SIZES,
    generate_partially_sorted,
    generate_random,
    generate_reverse_sorted,
    generate_sorted,
)


GENERATORS = [
    generate_random,
    generate_sorted,
    generate_reverse_sorted,
    generate_partially_sorted,
]


@pytest.fixture(params=GENERATORS, ids=lambda function: function.__name__)
def generator(request):
    return request.param


@pytest.mark.parametrize("size", [0, 1, 2, 19, 20, 21, *SIZES])
def test_sizes_and_value_bounds(generator, size):
    values = generator(size)
    assert isinstance(values, list)
    assert len(values) == size
    assert all(type(value) is int and 0 <= value <= 10 * size for value in values)


@pytest.mark.parametrize("size", [True, False, 1.5, "10", None, []])
def test_invalid_size_types(generator, size):
    with pytest.raises(TypeError, match="size"):
        generator(size)


@pytest.mark.parametrize("size", [-1, -100])
def test_negative_sizes(generator, size):
    with pytest.raises(ValueError, match="size"):
        generator(size)


@pytest.mark.parametrize("seed", [True, False, 1.5, "506", [], {}])
def test_invalid_seed_types(generator, seed):
    with pytest.raises(TypeError, match="seed"):
        generator(20, seed=seed)


@pytest.mark.parametrize("seed", [None, 0, -7, 12345])
def test_reproducible_seeds(generator, seed):
    assert generator(100, seed=seed) == generator(100, seed=seed)


def test_default_seed_matches_documented_rule(generator):
    assert generator(100) == generator(100, seed=BASE_SEED + 100)


def test_different_seeds_change_dataset(generator):
    assert generator(100, seed=10) != generator(100, seed=11)


def test_each_call_returns_independent_storage(generator):
    first = generator(100)
    second = generator(100)
    expected = second.copy()
    assert first is not second
    first[0] = -1
    assert second == expected
    assert generator(100) == expected
    assert generator(0) is not generator(0)


def test_global_random_state_is_unchanged(generator):
    before = random.getstate()
    generator(100)
    generator(100, seed=0)
    assert random.getstate() == before


@pytest.mark.parametrize("size", [0, 1, 19, 20, *SIZES])
@pytest.mark.parametrize("seed", [None, 0, -7])
def test_orderings_share_the_same_multiset(size, seed):
    original = generate_random(size, seed=seed)
    expected = sorted(original)
    ascending = generate_sorted(size, seed=seed)
    descending = generate_reverse_sorted(size, seed=seed)
    partial = generate_partially_sorted(size, seed=seed)

    assert ascending == expected
    assert descending == expected[::-1]
    assert Counter(partial) == Counter(original)
    # Each swap can affect at most two positions; some affect fewer.
    displaced = sum(left != right for left, right in zip(partial, ascending))
    assert displaced <= 2 * (size // 20)


@pytest.mark.parametrize("size", [0, 1, 2, 19])
def test_partial_small_inputs_remain_sorted(size):
    assert generate_partially_sorted(size, seed=0) == generate_sorted(size, seed=0)


def test_partial_one_swap_uses_the_documented_seed():
    # Random(1).sample(range(20), 2) selects positions 4 and 18.
    expected = generate_sorted(20, seed=0)
    expected[4], expected[18] = expected[18], expected[4]
    assert generate_partially_sorted(20, seed=0) == expected


def test_partial_repeated_swaps_have_expected_order():
    # Random(1) selects (17,72), (97,8), (32,15), (63,97), (57,60).
    expected = generate_sorted(100, seed=0)
    for first, second in [(17, 72), (97, 8), (32, 15), (63, 97), (57, 60)]:
        expected[first], expected[second] = expected[second], expected[first]
    actual = generate_partially_sorted(100, seed=0)
    assert actual == expected
    assert actual != sorted(actual)


def test_random_draws_match_seeded_inclusive_range():
    # First five randint(0, 50) draws from Random(0).
    assert generate_random(5, seed=0) == [24, 48, 26, 2, 16]


@pytest.mark.parametrize("sorter", [bubble_sort, selection_sort, insertion_sort, merge_sort])
def test_generated_inputs_work_with_each_sorter(generator, sorter):
    original = generator(100, seed=7)
    snapshot = original.copy()
    working = original.copy()
    assert sorter(working) is working
    assert working == sorted(snapshot)
    assert original == snapshot
