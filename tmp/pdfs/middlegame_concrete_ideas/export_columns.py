import json
from pathlib import Path

root = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\pdfs\middlegame_concrete_ideas")
out = []
for page in range(11, 20):
    rows = json.loads((root / f"source-{page:03d}-ocr.json").read_text(encoding="utf-8"))
    out.append(f"===== PDF {page} / PRINTED {page - 2} =====")
    for column, selected in (
        ("LEFT", [r for r in rows if r["x"] < 900]),
        ("RIGHT", [r for r in rows if r["x"] >= 900]),
    ):
        out.append(f"--- {column} ---")
        for row in sorted(selected, key=lambda r: (r["y"], r["x"])):
            out.append(f'{row["y"]:7.1f} {row["text"]}')
(root / "ocr_columns.txt").write_text("\n".join(out), encoding="utf-8")
