"""Render the APA-style project report with embedded figures.

Run from the repository root with:
    python scripts/render_apa_report.py

The Markdown file is the editable source. This renderer creates a submission-
friendly PDF with title page, APA-style headings, references, and chart figures.
It uses matplotlib, which is already part of the project requirements.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import textwrap

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from matplotlib.image import imread


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "APA_PROJECT_REPORT.pdf"


def _page(metadata_title: str = "SortBench APA Project Report") -> Figure:
    figure = Figure(figsize=(8.5, 11))
    figure.patch.set_facecolor("white")
    figure.text(0.5, 0.965, metadata_title, ha="center", va="top", fontsize=10, family="DejaVu Serif")
    return figure


def _footer(figure: Figure, page_number: int) -> None:
    figure.text(0.92, 0.035, str(page_number), ha="right", fontsize=10, family="DejaVu Serif")


def _paragraph(figure: Figure, text: str, y: float, width: int = 94, size: int = 11) -> float:
    for line in textwrap.wrap(text, width=width):
        figure.text(0.12, y, line, va="top", fontsize=size, family="DejaVu Serif")
        y -= 0.020
    return y - 0.016


def _heading(figure: Figure, text: str, y: float, centered: bool = False) -> float:
    x = 0.5 if centered else 0.12
    figure.text(x, y, text, ha="center" if centered else "left", va="top",
                fontsize=12, weight="bold", family="DejaVu Serif")
    return y - 0.035


def _table_50000(figure: Figure, y: float) -> float:
    rows = [
        ["Ordering", "Bubble", "Selection", "Insertion", "Merge"],
        ["Random", "61.1792", "23.6449", "27.0069", "0.0731"],
        ["Sorted", "0.0013", "29.2821", "0.0026", "0.0695"],
        ["Reverse", "79.5163", "28.0274", "52.9517", "0.0631"],
        ["Partial", "40.8929", "26.2688", "3.2475", "0.0819"],
    ]
    figure.text(0.12, y, "Table 1", va="top", fontsize=11, weight="bold", family="DejaVu Serif")
    y -= 0.024
    figure.text(0.12, y, "Execution Time for 50,000 Elements, in Seconds",
                va="top", fontsize=11, style="italic", family="DejaVu Serif")
    y -= 0.032
    axis = figure.add_axes([0.12, y - 0.145, 0.76, 0.145])
    axis.set_axis_off()
    table = axis.table(cellText=rows[1:], colLabels=rows[0], cellLoc="center", loc="center", bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    for (row, _column), cell in table.get_celld().items():
        cell.set_edgecolor("#b8c2cc")
        if row == 0:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#eef2f5")
    return y - 0.17


def _figure_page(pdf: PdfPages, page_number: int, title: str, image_names: list[tuple[str, str]]) -> None:
    figure = _page()
    _footer(figure, page_number)
    y = _heading(figure, title, 0.91, centered=True)
    for index, (caption, image_name) in enumerate(image_names):
        top = y - index * 0.39
        figure.text(0.12, top, caption.split("|", 1)[0], fontsize=11, weight="bold", family="DejaVu Serif")
        figure.text(0.12, top - 0.024, caption.split("|", 1)[1], fontsize=11, style="italic", family="DejaVu Serif")
        axis = figure.add_axes([0.12, top - 0.34, 0.76, 0.285])
        axis.imshow(imread(ROOT / "results" / "analysis" / "charts" / image_name))
        axis.set_axis_off()
    pdf.savefig(figure)


def render_apa_report() -> Path:
    timestamp = datetime(2026, 10, 5, tzinfo=timezone.utc)
    metadata = {
        "Title": "Sorting Algorithm Benchmarking in Python",
        "Author": "Shreyash",
        "Subject": "APA-style SortBench project report",
        "CreationDate": timestamp,
        "ModDate": timestamp,
    }
    with PdfPages(OUT, metadata=metadata) as pdf:
        figure = _page()
        _footer(figure, 1)
        figure.text(0.5, 0.68, "Sorting Algorithm Benchmarking in Python:\nEffects of Input Size and Ordering",
                    ha="center", va="center", fontsize=15, weight="bold", family="DejaVu Serif")
        figure.text(0.5, 0.54, "Shreyash\nCSC506: Design and Analysis of Algorithms\nColorado State University Global\nOctober 2026",
                    ha="center", va="center", fontsize=12, family="DejaVu Serif", linespacing=1.8)
        pdf.savefig(figure)

        figure = _page()
        _footer(figure, 2)
        y = _heading(figure, "Abstract", 0.90, centered=True)
        y = _paragraph(figure, "This project evaluated Bubble Sort, Selection Sort, Insertion Sort, and Merge Sort across random, sorted, reverse-sorted, and partially sorted integer lists with 1,000, 5,000, 10,000, and 50,000 elements. Each scenario was measured once in Python 3.14.4 on Windows 11 using time.perf_counter(), and every result was validated against Python's independently computed sorted(original) output.", y)
        y = _paragraph(figure, "The results supported the expected algorithmic patterns: Merge Sort scaled best on random, reverse-sorted, and partially sorted inputs, while adaptive quadratic algorithms were strongest on already sorted inputs. Because the benchmark used one recorded trial per scenario, the findings should be read as transparent project evidence rather than statistically generalizable performance claims.", y)
        y = _heading(figure, "Introduction", y)
        y = _paragraph(figure, "Sorting algorithms connect theoretical complexity with observed runtime behavior. Cormen et al. (2022) present sorting as a core topic in algorithm analysis because different strategies solve the same problem with different time and space costs.", y)
        _paragraph(figure, "SortBench compared four manually implemented algorithms under controlled project conditions. Bubble Sort and Insertion Sort can exploit already ordered data, Selection Sort performs predictable quadratic scans, and Merge Sort uses divide and conquer to provide O(n log n) behavior at the cost of auxiliary storage.", y)
        pdf.savefig(figure)

        figure = _page()
        _footer(figure, 3)
        y = _heading(figure, "Method", 0.90, centered=True)
        y = _paragraph(figure, "The benchmark used four dataset types and four sizes, producing 64 scenarios. Each size used deterministic seeds, and all orderings for that size shared the same multiset of values. The timer measured only the sorting call; generation, copying, validation, and CSV output were excluded.", y)
        y = _paragraph(figure, "Python's time.perf_counter() was selected because the official documentation describes it as a high-resolution performance counter for measuring short durations (Python Software Foundation, 2026a). Python's sorted function was used only as a correctness oracle, not as a benchmark target.", y)
        y = _heading(figure, "Results", y)
        y = _paragraph(figure, "Merge Sort was fastest in all random, reverse-sorted, and partially sorted groups. Sorted input changed the ranking: Bubble Sort won at 1,000, 5,000, and 50,000 elements, while Insertion Sort won at 10,000 elements. Selection Sort remained slow on sorted input because it continued scanning each unsorted suffix.", y)
        _table_50000(figure, y)
        pdf.savefig(figure)

        _figure_page(pdf, 4, "Analysis Figures", [
            ("Figure 1|Execution time by dataset size.", "time_vs_size.png"),
            ("Figure 2|Algorithm comparison by dataset ordering.", "dataset_comparison.png"),
        ])
        _figure_page(pdf, 5, "Dataset Figures", [
            ("Figure 3|Random dataset performance.", "random.png"),
            ("Figure 4|Sorted dataset performance.", "sorted.png"),
        ])
        _figure_page(pdf, 6, "Dataset Figures", [
            ("Figure 5|Reverse-sorted dataset performance.", "reverse_sorted.png"),
            ("Figure 6|Partially sorted dataset performance.", "partially_sorted.png"),
        ])

        figure = _page()
        _footer(figure, 7)
        y = _heading(figure, "Discussion", 0.90, centered=True)
        y = _paragraph(figure, "The measured growth rates were consistent with the distinction between O(n log n) and O(n^2). On random input, increasing the size from 1,000 to 50,000 elements increased Merge Sort runtime by about 75.5 times, while the quadratic algorithms increased by roughly 2,606 to 3,047 times.", y)
        y = _paragraph(figure, "Input ordering mattered most for Bubble Sort and Insertion Sort. On sorted input, both algorithms behaved like adaptive algorithms and avoided the large costs seen on random or reverse-sorted data. Python's Sorting HOWTO similarly notes that Python's Timsort can take advantage of existing order, although SortBench measured the course algorithms rather than Python's built-in sort (Python Software Foundation, 2026b).", y)
        y = _heading(figure, "Recommendations and Limitations", y)
        y = _paragraph(figure, "For random, reverse-sorted, or partially sorted integer lists in the tested size range, Merge Sort is the best time-based choice when O(n) extra memory is acceptable. For already sorted data, Bubble Sort or Insertion Sort is more appropriate. The main limitation is that each scenario has one recorded trial, so future work should add repeated trials, randomized execution order, multiple seeds, and memory profiling.", y)
        y = _heading(figure, "References", y)
        refs = [
            "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). Introduction to algorithms (4th ed.). The MIT Press. https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/",
            "Knuth, D. E. (1998). The art of computer programming: Volume 3: Sorting and searching (2nd ed.). Addison-Wesley.",
            "Python Software Foundation. (2026a). time - Time access and conversions. Python 3.14 documentation. https://docs.python.org/3/library/time.html",
            "Python Software Foundation. (2026b). Sorting techniques. Python 3.14 documentation. https://docs.python.org/3/howto/sorting.html",
        ]
        for ref in refs:
            y = _paragraph(figure, ref, y, width=92, size=9)
        pdf.savefig(figure)
    return OUT


if __name__ == "__main__":
    print(f"Wrote APA project report: {render_apa_report()}")
