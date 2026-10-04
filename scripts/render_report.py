"""Format the final Markdown analysis into three printable, text-based pages.

Run from the repository root with python scripts/render_report.py. This small
formatter supports the paragraphs, headings and tables used by this report;
it is not a general Markdown converter. It uses the existing matplotlib dependency.
"""

from datetime import datetime, timezone
from pathlib import Path
import re
import textwrap

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from matplotlib.image import imread

ROOT = Path(__file__).resolve().parents[1]


def _plain(text: str) -> str:
    """Keep link labels and inline code text in the printed narrative."""
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text).replace("`", "")


def render_report(preview_dir: Path | None = None) -> Path:
    """Write exactly three pages; fail if edited content exceeds the page area."""
    source = (ROOT / "docs/PERFORMANCE_ANALYSIS.md").read_text(encoding="utf-8")
    first, rest = source.split("## Algorithm behavior and complexity", 1)
    second, third = rest.split("Sorted input substantially changed the result.", 1)
    pages = [first, "## Algorithm behavior and complexity" + second,
             "## Ordering effects\n\nSorted input substantially changed the result." + third]
    destination = ROOT / "docs/PERFORMANCE_ANALYSIS.pdf"
    timestamp = datetime(2026, 10, 3, tzinfo=timezone.utc)
    metadata = {"Title": "SortBench: Performance Analysis", "Author": "SortBench",
                "Subject": "v1.0.0 measured results and limitations",
                "CreationDate": timestamp, "ModDate": timestamp}
    if preview_dir:
        preview_dir.mkdir(parents=True, exist_ok=True)
    with PdfPages(destination, metadata=metadata) as pdf:
        for number, content in enumerate(pages, start=1):
            figure = Figure(figsize=(8.5, 11))
            canvas = FigureCanvasAgg(figure)
            figure.text(0.075, 0.955, "SORTBENCH  /  PERFORMANCE ANALYSIS", fontsize=9,
                        color="#30556d", weight="bold")
            figure.text(0.925, 0.955, "v1.0.0", fontsize=9, ha="right", color="#30556d")
            figure.text(0.075, 0.04, "One trial per scenario | Primary full repeat | October 3, 2026",
                        fontsize=8, color="#555555")
            figure.text(0.925, 0.04, f"{number} / 3", fontsize=8, ha="right")
            y = 0.918
            body_artists = []
            for block in re.split(r"\n\s*\n", content.strip()):
                if block.startswith("|"):
                    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")]
                            for line in block.splitlines()]
                    rows = [row for row in rows if not all(re.fullmatch(r"[-:]+", cell) for cell in row)]
                    height = len(rows) * 0.022
                    axis = figure.add_axes([0.075, y - height, 0.85, height])
                    axis.set_axis_off()
                    table = axis.table(cellText=rows[1:], colLabels=rows[0],
                                       cellLoc="left", loc="center", bbox=[0, 0, 1, 1])
                    table.auto_set_font_size(False)
                    table.set_fontsize(8)
                    for (row, column), cell in table.get_celld().items():
                        cell.set_edgecolor("#d1d9df")
                        if row == 0:
                            cell.set_facecolor("#e6eef3")
                            cell.set_text_props(weight="bold")
                    y -= height + 0.022
                elif block.startswith("#"):
                    title = block.lstrip("# ")
                    size = 17 if block.startswith("# ") else 12
                    body_artists.append(figure.text(0.075, y, title, va="top", fontsize=size,
                                                     weight="bold", color="#1e394b"))
                    y -= 0.044 if size == 17 else 0.034
                else:
                    lines = textwrap.wrap(_plain(" ".join(block.splitlines())), width=96)
                    for line in lines:
                        body_artists.append(figure.text(0.075, y, line, va="top", fontsize=10,
                                                         color="#202830"))
                        y -= 13 / 792
                    y -= 0.015
            if number == 1:
                axis = figure.add_axes([0.075, 0.095, 0.85, min(y - 0.12, 0.36)])
                axis.imshow(imread(ROOT / "results/analysis/charts/random.png"))
                axis.set_axis_off()
            canvas.draw()
            renderer = canvas.get_renderer()
            for artist in body_artists:
                box = artist.get_window_extent(renderer).transformed(figure.transFigure.inverted())
                if box.x1 > 0.94 or box.y0 < 0.075:
                    raise ValueError(f"Report page {number} overflows at {box.bounds}: {artist.get_text()}")
            if y < 0.065:
                raise ValueError(f"Report page {number} is too long")
            pdf.savefig(figure)
            if preview_dir:
                figure.savefig(preview_dir / f"report-page-{number}.png", dpi=120)
            figure.clear()
    return destination


if __name__ == "__main__":
    print(f"Wrote three-page report: {render_report()}")
