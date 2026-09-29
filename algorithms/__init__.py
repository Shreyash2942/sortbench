"""Sorting functions that modify and return the supplied integer list."""

from .bubble_sort import bubble_sort
from .insertion_sort import insertion_sort
from .merge_sort import merge_sort
from .selection_sort import selection_sort

__all__ = ["bubble_sort", "selection_sort", "insertion_sort", "merge_sort"]
