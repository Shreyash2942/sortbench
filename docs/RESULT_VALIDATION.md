# Day 5 result audit

The runner checks actual sorting output during execution. The separate
`benchmark.result_validation.validate_results()` function audits persisted CSV
and metadata for the full, single-trial assignment matrix. It does not rerun
sorting and cannot independently prove a stored correctness flag is truthful.

From the repository root:

```powershell
.\.venv\Scripts\python.exe -c "from benchmark.result_validation import validate_results; rows = validate_results('results/benchmark_results.csv'); print(f'Validated {len(rows)} scenarios')"
```

The audit requires:

- The exact CSV columns defined by the runner.
- Every algorithm/type/required-size combination exactly once: 64 rows.
- Trial 1, `valid=True`, and finite nonnegative elapsed seconds on every row.
- Integer seeds matching the metadata for each size.
- Complete metadata with consistent scenario counts, required sizes, algorithm
  and dataset order, timing units/method, filename, and environment details.
- Timezone-aware, chronological start and finish timestamps.
- CSV row order matching the declared sequential execution order.

Missing, duplicate, unexpected, malformed, invalid, or inconsistent evidence
raises `ValueError`. Missing/unreadable files raise the underlying I/O exception.
A Day 4 smoke run intentionally fails this audit because it does not contain
the required sizes and 64 scenarios. Synthetic fixtures used in audit tests
remain inside pytest temporary directories and are never published as results.

The final [validation report](../results/validation_report.json) records SHA-256
hashes of the primary CSV and metadata. These identify the bytes that were
audited; they do not provide cryptographic proof that a benchmark was executed.
The [initial observations](DAY5_OBSERVATIONS.md) compare the measured values and
identify the fastest observed algorithm for each of the 16 size/type groups.

One trial per scenario supports descriptive comparisons, not confidence
intervals or robust estimates of timing noise. No average over repeated trials
is reported. Suspicious results should prompt a consistent comparison-set rerun
with a new filename and a documented method, retaining the original evidence.

During Day 5, the initial attempt completed all 64 scenarios but recorded
3,927.573 seconds for the 50,000-element reverse-sorted Bubble Sort case.
An observation shortly afterward showed only about 380 seconds of total process
CPU time. This supports an apparent long pause or scheduling gap; its precise
cause was not confirmed. The original CSV and metadata were moved unchanged to
`results/initial_run/`, and the entire matrix was repeated for the final dataset.
Results are not selected individually from whichever attempt was faster.
See [run_review.json](../results/run_review.json) for the attempt record.
