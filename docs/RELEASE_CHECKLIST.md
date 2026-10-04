# SortBench v1.0.0 release checklist

The implementation, evidence, report, and local release checks are complete.
GitHub Release publication requires an authenticated GitHub CLI session; the
SSH Git remote alone does not provide access to the Releases API.

## Deliverable review

| Requirement | Evidence | Result |
|---|---|---|
| Four manual sorting algorithms | `algorithms/`, 93 algorithm tests | Complete |
| Four reproducible dataset orderings and required sizes | `data/`, 175 dataset/integration tests | Complete |
| Sorting-only timer, independent copies, correctness validation | `benchmark/`, 33 runner/timer tests | Complete |
| All 64 required measurements and CSV table | [Primary CSV](../results/benchmark_results.csv), complete metadata | Complete |
| Independent persisted-result audit | 37 audit tests, [validation report](../results/validation_report.json) | Complete |
| Performance, size, and ordering comparisons | [Six charts](../results/analysis/charts/time_vs_size.png), comparison and growth CSVs | Complete |
| Measured recommendation logic and guide | [Guide](RECOMMENDATION_GUIDE.md), 25 analysis/chart tests | Complete |
| 2-3 page written analysis with complexity and trade-offs | [Three-page PDF](PERFORMANCE_ANALYSIS.pdf), [Markdown source](PERFORMANCE_ANALYSIS.md) | Complete |
| README, requirements, architecture and test plan | Linked from [README](../README.md) | Complete |
| Retrospective | [Project retrospective](RETROSPECTIVE.md) | Complete |
| Incremental Git history | Focused commits across Days 1-7; no rewritten history | Reviewed |
| Source, results, report and charts included in release | Versioned repository tree and annotated `v1.0.0` tag | Prepared |
| Stable GitHub Release page | Publish using the command below after CLI login | Pending authentication |

## Verification record

On October 3, 2026, the exact versions in `requirements-lock.txt` installed
successfully into a fresh virtual environment using Python 3.14.4 on Windows.
The complete suite passed: **363 tests**. `pip check` found no broken
requirements, and `main.py` produced the expected sorted example and datasets.
The machine-readable record is [release_validation.json](../results/release_validation.json).
The analysis integration test regenerates tables and all six charts in a
temporary directory and verifies input preservation and output provenance.

The primary CSV still has 64 unique valid scenarios. Primary and derived file
hashes match their recorded manifests. The PDF has exactly three pages; all
three page layouts were inspected for clipping and readability. Local Markdown
links resolve, and the original root `README(6).md` and its preserved assignment
copy remain byte-for-byte identical. No full timing experiment was rerun during
release QA, and no timings or observed rankings were changed.

## Reproduce the checks

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe scripts/render_report.py
```

The lock file records the verified environment; other platforms and Python
versions were not tested. The direct dependencies remain in `requirements.txt`.
The report formatter uses matplotlib and checks page bounds before finishing.

## Publish the prepared GitHub Release

Once `v1.0.0` is pushed and the CLI is authenticated as an account with access:

```powershell
gh release create v1.0.0 docs/PERFORMANCE_ANALYSIS.pdf --repo Shreyash2942/sortbench --verify-tag --title "SortBench v1.0.0" --notes-file docs/RELEASE_NOTES.md
gh release view v1.0.0 --repo Shreyash2942/sortbench
```

GitHub supplies source archives from the tagged commit; the PDF is also attached
for convenient download. Update publication status only after the API confirms
the release exists. A Git tag and a GitHub Release page are distinct artifacts.
