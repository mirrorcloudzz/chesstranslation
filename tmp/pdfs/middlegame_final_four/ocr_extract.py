import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\12059\Documents\Codex\chess\tmp\ocrdeps")

from rapidocr_onnxruntime import RapidOCR


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"
engine = RapidOCR()

for page in range(145, 233):
    image_path = SOURCE / f"page-{page:03d}.png"
    output = SOURCE / f"page-{page:03d}-ocr.json"
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
    print(f"{page}: {len(rows)} lines", flush=True)
