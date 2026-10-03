# Day 3 dataset generation

The root assignment plan's four functions are available from `data` and from
`data.data_generator`. They accept a configurable size and an optional keyword
seed. Every call returns a fresh integer list.

```python
from data import (
    SIZES,
    generate_random,
    generate_sorted,
    generate_reverse_sorted,
    generate_partially_sorted,
)

for size in SIZES:  # [1000, 5000, 10000, 50000]
    original = generate_random(size)
    ascending = generate_sorted(size)
    descending = generate_reverse_sorted(size)
    partial = generate_partially_sorted(size)
    assert ascending == sorted(original)
    assert descending == ascending[::-1]
    assert sorted(partial) == ascending
```

## Input and seed contract

- `size` must be a nonnegative integer. Zero returns a fresh empty list.
- Booleans and other non-integer sizes raise `TypeError`; negative sizes raise
  `ValueError`. The required sizes are defaults for the experiment, not a limit
  on the generator API.
- Omitted `seed` or `seed=None` resolves to `BASE_SEED + size`, with BASE_SEED=506.
  None deliberately means the deterministic default, not system entropy.
- Explicit integer seeds, including zero and negatives, are accepted. Boolean
  and other non-integer seeds raise `TypeError`.
- All four functions accept the same keyword seed. For matching values across
  orderings, use equal sizes and equal effective seeds.
- Each call constructs a local `random.Random`; it does not seed or consume the
  module-level random generator. Mutating one returned list cannot affect later
  calls or another dataset.

Reproducibility means identical inputs in the same Python environment yield
identical outputs. Do not assume all Python versions produce identical results
for every random helper, or that every distinct integer seed must yield distinct
datasets. Record the Python version and effective seed with future benchmarks.

## Ordering definitions

| Function | Construction |
|---|---|
| `generate_random(size, *, seed=None)` | Draw `size` integers with `randint(0, 10 * size)`, inclusive at both ends. |
| `generate_sorted(size, *, seed=None)` | Sort that same seeded base list in nondecreasing order. |
| `generate_reverse_sorted(size, *, seed=None)` | Sort the seeded base list in nonincreasing order. |
| `generate_partially_sorted(size, *, seed=None)` | Start with the ascending base list, then perform `size // 20` swaps. |

Duplicates are allowed, so sorted order is not necessarily strictly increasing
or decreasing. A random sample can happen to be ordered, especially at small
sizes; the generator does not force disorder by changing the specified draws.

For partial ordering, use a separate local RNG seeded with `effective_seed + 1`.
For each swap, `sample(range(size), 2)` chooses two distinct indices. Different
swaps may reuse indices; swapped values may be equal. Therefore 5% as many
swaps as elements does not mean exactly 5% of elements are displaced. At most
`2 * (size // 20)` positions can differ from the sorted base. For sizes below
20 there are no swaps, and the output stays sorted.

## Benchmark integration and validation

Built-in sorting here constructs test inputs; it does not implement any of the
four algorithms being benchmarked. Dataset generation belongs outside the timed
sorting call. The Day 4 runner generates each scenario once, makes a fresh
copy per algorithm, and records the effective seed (`506 + size` by default).

Run `.venv/Scripts/python.exe -m pytest -q tests/test_data_generator.py` to run
the 175 dataset/integration cases. They include all required sizes, ordering and
multiset checks, exact seeded examples, invalid inputs, global-state isolation,
and all 16 algorithm/dataset combinations on small inputs. The complete suite,
including benchmark and result-audit tests, has 338 passing tests. No ranking is inferred
from these correctness checks.
