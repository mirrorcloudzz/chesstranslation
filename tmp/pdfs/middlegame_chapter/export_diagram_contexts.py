import json
from pathlib import Path

root = Path(str(Path(__file__).resolve().parents[3] / 'tmp/pdfs/middlegame_chapter/source'))
manifest = root.parent / "diagram_manifest.tsv"
out = []

for raw in manifest.read_text(encoding="utf-8").splitlines():
    page_text, index_text, box_text, name = raw.split("\t")
    page = int(page_text)
    x1, y1, x2, y2 = map(int, box_text.split(","))
    rows = json.loads((root / f"page-{page:03d}-ocr.json").read_text(encoding="utf-8"))
    # Capture text in the same column above the diagram, plus a small amount below it.
    column_rows = [
        row for row in rows
        if x1 - 120 <= row["x"] <= x2 + 120 and max(0, y1 - 650) <= row["y"] <= min(2200, y2 + 250)
    ]
    out.append(f"===== {name} | PDF {page} / PRINTED {page - 2} | box {box_text} =====")
    for row in sorted(column_rows, key=lambda item: (item["y"], item["x"])):
        marker = "[ABOVE]" if row["y"] < y1 else "[BELOW]" if row["y"] > y2 else "[DIAGRAM]"
        out.append(f'{marker} {row["y"]:7.1f} {row["text"]}')

(root.parent / "diagram_contexts.txt").write_text("\n".join(out), encoding="utf-8")
