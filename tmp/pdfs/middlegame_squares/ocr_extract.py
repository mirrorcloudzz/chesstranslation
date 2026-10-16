import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tmp/ocrdeps'))

from rapidocr_onnxruntime import RapidOCR


root = Path(str(Path(__file__).resolve().parents[3] / 'tmp/pdfs/middlegame_squares/source'))
engine = RapidOCR()

for image_path in sorted(root.glob("page-*.png")):
    output = root / f"{image_path.stem}-ocr.json"
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
