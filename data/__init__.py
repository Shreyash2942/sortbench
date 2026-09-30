"""Reproducible benchmark inputs and the assignment's required sizes."""

from .data_generator import (
    BASE_SEED,
    SIZES,
    generate_partially_sorted,
    generate_random,
    generate_reverse_sorted,
    generate_sorted,
)

__all__ = [
    "BASE_SEED",
    "SIZES",
    "generate_random",
    "generate_sorted",
    "generate_reverse_sorted",
    "generate_partially_sorted",
]
