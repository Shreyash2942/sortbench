# Reproducing the Day 6 analysis

From the repository directory, using the environment installed from
`requirements.txt`:

```powershell
.\.venv\Scripts\python.exe -m analysis.performance_analyzer
```

This audits `results/benchmark_results.csv` and its adjacent metadata before
loading records into pandas. It writes derived artifacts under
`results/analysis/` and does not execute sorting benchmarks. Repeating the
command replaces these derived outputs; the original measurements are preserved.
Invalid or incomplete input raises an error before the destination is created.

| Artifact | Meaning |
|---|---|
| `comparison.csv` | All 16 ordering/size groups, with a seconds column per algorithm |
| `observed_winners.csv` | Each minimum recorded time; every exact tie is retained |
| `growth.csv` | 50,000/1,000 time ratios per algorithm and ordering; undefined zero-baseline ratios are blank |
| `recommendations.json` | All 16 measured recommendations with limitations |
| `provenance.json` | SHA-256 hashes of input CSV/metadata and generated files, dependency versions and method |
| `charts/time_vs_size.png` | Four panels comparing times against actual dataset sizes |
| `charts/random.png`, `sorted.png`, `reverse_sorted.png`, `partially_sorted.png` | Larger individual ordering charts |
| `charts/dataset_comparison.png` | Four panels comparing dataset orderings at each size |

The six PNGs are standalone, share consistent algorithm colors, and label
units and scales. Time and size use logarithmic axes in the line charts;
the ordering chart uses categorical positions and logarithmic time. Its small
horizontal offsets distinguish algorithms within each category. Panels have
independent time ranges, so compare their labeled values rather than apparent
heights across panels. For an audited input containing zero time, the affected
panel uses a labeled linear time axis instead of hiding or adjusting zero.
Lines connect observations; they are not fitted predictions.

## Python API

```python
from analysis.performance_analyzer import load_results, comparison_table, generate_analysis
from analysis.recommendation import recommend

results = load_results()  # Audits the complete primary CSV and metadata.
print(comparison_table(results))
print(recommend(results, "random", 50000))
# algorithms: ['Merge Sort']; recorded time: approximately 0.0731335 seconds

# Optional: analyze another complete, audited assignment matrix separately.
# generate_analysis("results/another_run.csv", "results/another_analysis")
```

Summary and chart functions accept the unchanged frame returned by
`load_results`; they are not general-purpose validators for arbitrary data.
Recommendations additionally reject unsupported scenarios, incomplete groups,
duplicate algorithms, and invalid times. A near-tie is not converted into an
exact tie with an arbitrary tolerance; each recommendation warns that a single
observed minimum does not establish statistical superiority.

Primary, archived initial, and diagnostic runs are never merged. Provenance
hashes identify the bytes used for derived artifacts and do not independently
prove sorting correctness. The runner checked correctness during execution.
Saved [Day 5 winners](../results/scenario_winners.csv) remain unchanged;
the Day 6 table derives winners again and supports tied minima.

Read the [performance analysis](PERFORMANCE_ANALYSIS.md) and
[recommendation guide](RECOMMENDATION_GUIDE.md) for interpretation. The final [three-page PDF](PERFORMANCE_ANALYSIS.pdf)
is reproduced with `python scripts/render_report.py`. See
[RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) for release verification.
