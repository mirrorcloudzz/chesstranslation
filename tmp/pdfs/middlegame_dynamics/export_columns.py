import json
from pathlib import Path

root = Path(str(Path(__file__).resolve().parents[3] / 'tmp/pdfs/middlegame_dynamics'))
out = []
for page in range(19, 29):
    rows = json.loads((root / f"source-{page:03d}-ocr.json").read_text(encoding="utf-8"))
    out.append(f"===== PDF {page} / PRINTED {page - 2} =====")
    for column, selected in (
        ("LEFT", [row for row in rows if row["x"] < 820]),
        ("RIGHT", [row for row in rows if row["x"] >= 820]),
    ):
        out.append(f"--- {column} ---")
        for row in sorted(selected, key=lambda item: (item["y"], item["x"])):
            out.append(f'{row["y"]:7.1f} {row["text"]}')

(root / "ocr_columns.txt").write_text("\n".join(out), encoding="utf-8")
