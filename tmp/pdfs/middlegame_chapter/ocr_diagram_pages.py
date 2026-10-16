import json
import sys
from pathlib import Path

DEPS = Path(str(Path(__file__).resolve().parents[3] / 'tmp/ocrdeps'))
sys.path.insert(0, str(DEPS))

from rapidocr_onnxruntime import RapidOCR

root = Path(str(Path(__file__).resolve().parents[3] / 'tmp/pdfs/middlegame_chapter/source'))
pages = [9, 13, 15, 16, 17, 18, 19, 22, 24, 25, 26, 27, 28, 29, 31, 32, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 54, 55, 56, 57, 59, 60]
engine = RapidOCR()

for page in pages:
    image_path = root / f"page-{page:03d}.png"
    output_path = root / f"page-{page:03d}-ocr.json"
    if output_path.exists():
        print(f"page {page}: cached")
        continue
    result, _ = engine(str(image_path))
    rows = []
    for box, text, score in result or []:
        x = min(point[0] for point in box)
        y = min(point[1] for point in box)
        rows.append({"x": x, "y": y, "text": text, "score": score})
    output_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"page {page}: {len(rows)} lines")
