import json
from pathlib import Path

root = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\pdfs\middlegame_chapters12\source")
out_dir = root.parent / "plain"
out_dir.mkdir(exist_ok=True)

for page in range(62, 90):
    rows = json.loads((root / f"page-{page:03d}-ocr.json").read_text(encoding="utf-8"))
    parts = [f"PDF {page} / PRINTED {page - 2}"]
    for selected in (
        [row for row in rows if row["x"] < 820],
        [row for row in rows if row["x"] >= 820],
    ):
        parts.append("\n".join(row["text"] for row in sorted(selected, key=lambda item: (item["y"], item["x"]))))
    (out_dir / f"page-{page:03d}.txt").write_text("\n\n".join(parts), encoding="utf-8")
