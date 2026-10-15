import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\12059\Documents\Codex\chess\tmp\ocrdeps")

from rapidocr_onnxruntime import RapidOCR


root = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\pdfs\middlegame_chapters12\source")
engine = RapidOCR()

for page in range(62, 90):
    image_path = root / f"page-{page:03d}.png"
    output = root / f"page-{page:03d}-ocr.json"
    result, _ = engine(str(image_path))
    rows = []
    for box, value, score in result or []:
        xs = [point[0] for point in box]
        ys = [point[1] for point in box]
        rows.append({
            "x": min(xs), "y": min(ys), "right": max(xs),
            "bottom": max(ys), "text": value, "score": score,
        })
    rows.sort(key=lambda row: (row["y"], row["x"]))
    output.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{image_path.name}: {len(rows)} lines")

