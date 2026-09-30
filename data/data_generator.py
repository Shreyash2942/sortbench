"""Reproducible integer datasets sharing the same multiset for each size/seed.

Generation and built-in sorting here are setup work, outside benchmark timing.
The four handwritten sorting algorithms remain the subjects of the experiment.
"""

import random


BASE_SEED = 506
SIZES = [1000, 5000, 10000, 50000]


def _resolve_seed(size: int, seed: int | None) -> int:
    """Validate inputs and choose the documented deterministic default seed."""
    if isinstance(size, bool) or not isinstance(size, int):
        raise TypeError("size must be a nonnegative integer")
    if size < 0:
        raise ValueError("size must be nonnegative")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise TypeError("seed must be an integer or None")
    return BASE_SEED + size if seed is None else seed


def generate_random(size: int, *, seed: int | None = None) -> list[int]:
    """Return size random integers drawn inclusively from [0, 10 * size].

    Repeated calls with the same size/seed reproduce the values in a fresh
    list. None selects BASE_SEED + size; an explicit integer overrides that
    seed (including zero and negative integers). Global random state is unused.
    Invalid sizes/seeds raise TypeError; negative sizes raise ValueError.
    """
    rng = random.Random(_resolve_seed(size, seed))
    return [rng.randint(0, 10 * size) for _ in range(size)]


def generate_sorted(size: int, *, seed: int | None = None) -> list[int]:
    """Return the seeded base values in nondecreasing order in a fresh list.

    The size/seed rules and exceptions are the same as generate_random().
    """
    return sorted(generate_random(size, seed=seed))


def generate_reverse_sorted(size: int, *, seed: int | None = None) -> list[int]:
    """Return the seeded base values in nonincreasing order in a fresh list.

    The size/seed rules and exceptions are the same as generate_random().
    """
    return sorted(generate_random(size, seed=seed), reverse=True)


def generate_partially_sorted(size: int, *, seed: int | None = None) -> list[int]:
    """Return sorted base values after size // 20 reproducible random swaps.

    Select two distinct indices per swap using a separate local generator
    seeded with effective_seed + 1. Swaps can revisit indices or exchange equal
    values, so they do not imply an exact percentage of displaced elements.
    Sizes below 20 remain sorted. Input validation matches generate_random().
    """
    effective_seed = _resolve_seed(size, seed)
    values = generate_sorted(size, seed=effective_seed)
    rng = random.Random(effective_seed + 1)
    for _ in range(size // 20):
        first, second = rng.sample(range(size), 2)
        values[first], values[second] = values[second], values[first]
    return values
