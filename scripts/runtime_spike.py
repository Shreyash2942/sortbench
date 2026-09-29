"""Measure a bounded quadratic comparison loop for Day 1 feasibility planning.

This is not a sorting implementation or part of the final 64-scenario dataset.
Run from the repository root: python scripts/runtime_spike.py
"""

import csv
import platform
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from time import perf_counter


def scan_suffix_minima(values: list[int]) -> int:
    """Scan unsorted suffixes without swapping; return a consumed checksum."""
    checksum = 0
    for start in range(len(values) - 1):
        smallest = values[start]
        for index in range(start + 1, len(values)):
            if values[index] < smallest:
                smallest = values[index]
        checksum += smallest
    return checksum


def main() -> None:
    """Write measured small-input times and an explicitly labeled projection."""
    root = Path(__file__).resolve().parents[1]
    rows = []
    summaries = []
    for size in (1000, 2000, 4000):
        rng = random.Random(506 + size)
        values = [rng.randint(0, 10 * size) for _ in range(size)]
        times = []
        for trial in range(1, 4):
            start = perf_counter()
            checksum = scan_suffix_minima(values)
            elapsed = perf_counter() - start
            times.append(elapsed)
            rows.append({"size": size, "trial": trial,
                         "comparisons": size * (size - 1) // 2,
                         "execution_time_seconds": elapsed,
                         "checksum": checksum})
        summaries.append((size, median(times)))

    result_path = root / "results" / "runtime_spike.csv"
    with result_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    size, measured = summaries[-1]
    target = 50000
    ratio = (target * (target - 1)) / (size * (size - 1))
    projection = measured * ratio
    table = "\n".join(
        f"| {n:,} | {n * (n - 1) // 2:,} | {seconds:.6f} |"
        for n, seconds in summaries
    )
    report = f"""# Day 1 runtime feasibility spike

Measured at {datetime.now(timezone.utc).isoformat()}.

- Python: {sys.version.splitlines()[0]}
- Platform: {platform.platform()}
- Processor: {platform.processor() or 'not reported'}
- Input: seeded random integers; seed = 506 + size.
- Method: three trials per size, median elapsed seconds, `perf_counter()`.
- Operation: suffix-minimum scanning with no swaps; **not a full sort**.
- Dataset construction and file output are outside timing.

| Size | Comparisons per trial | Measured median seconds |
|---:|---:|---:|
{table}

## Projection, not a measurement

At 50,000 elements the loop would make {target * (target - 1) // 2:,}
comparisons. Scaling the measured {size:,}-element median by the exact
comparison-count ratio ({ratio:.3f}) gives **{projection:.3f} seconds**.
The 50,000-element case was not executed in this spike.

This estimate assumes the same per-comparison cost. Full algorithms also have
swaps, shifts, recursion, allocation, and input-order effects. These numbers
cannot establish which sorting algorithm is fastest. Background system load
was not controlled, and three short runs do not establish statistical precision.

## Day 1 decision

Retain all required sizes, including 50,000, in the final benchmark. Expect
quadratic cases to take substantially longer than these small cases. Run full
experiments sequentially, save validated results as they finish, and document
any incomplete scenario. Do not substitute this projection for measured data.

Raw measurements: [runtime_spike.csv](../results/runtime_spike.csv).
Reproduce from the repository root with `python scripts/runtime_spike.py`.
"""
    (root / "docs" / "RUNTIME_SPIKE.md").write_text(report, encoding="utf-8")
    print(table)
    print(f"50,000-element projection (not measured): {projection:.3f} seconds")
    print("Wrote results/runtime_spike.csv and docs/RUNTIME_SPIKE.md")


if __name__ == "__main__":
    main()
