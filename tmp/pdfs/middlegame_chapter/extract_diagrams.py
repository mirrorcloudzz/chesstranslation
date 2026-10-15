from pathlib import Path

import numpy as np
from PIL import Image, ImageOps


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\pdfs\middlegame_chapter")
SOURCE = ROOT / "source"
OUT = ROOT / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)


def dark_runs(row, threshold=95, min_length=260, gap=4):
    dark = np.flatnonzero(row < threshold)
    if not len(dark):
        return []
    runs = []
    start = prev = int(dark[0])
    for value in dark[1:]:
        value = int(value)
        if value - prev <= gap:
            prev = value
            continue
        if prev - start + 1 >= min_length:
            runs.append((start, prev))
        start = prev = value
    if prev - start + 1 >= min_length:
        runs.append((start, prev))
    return runs


def group_lines(lines):
    groups = []
    for y, x1, x2 in lines:
        matched = False
        for group in groups:
            gy, gx1, gx2 = group[-1]
            if y - gy <= 8 and abs(x1 - gx1) <= 25 and abs(x2 - gx2) <= 25:
                group.append((y, x1, x2))
                matched = True
                break
        if not matched:
            groups.append([(y, x1, x2)])
    return [
        (
            round(sum(v[0] for v in group) / len(group)),
            round(sum(v[1] for v in group) / len(group)),
            round(sum(v[2] for v in group) / len(group)),
        )
        for group in groups
    ]


manifest = []
for page in range(8, 62):
    path = SOURCE / f"page-{page:03d}.png"
    image = Image.open(path).convert("L")
    array = np.asarray(image)
    lines = []
    for y in range(array.shape[0]):
        for x1, x2 in dark_runs(array[y]):
            if 300 <= x2 - x1 + 1 <= 650:
                lines.append((y, x1, x2))
    grouped = group_lines(lines)
    candidates = []
    for i, top in enumerate(grouped):
        ty, tx1, tx2 = top
        tw = tx2 - tx1 + 1
        for bottom in grouped[i + 1:]:
            by, bx1, bx2 = bottom
            bw = bx2 - bx1 + 1
            height = by - ty
            if height < 300:
                continue
            if height > 650:
                break
            if abs(tx1 - bx1) <= 35 and abs(tx2 - bx2) <= 35 and abs(height - (tw + bw) / 2) <= 45:
                x1 = min(tx1, bx1)
                x2 = max(tx2, bx2)
                candidates.append((x1, ty, x2, by))
                break
    # Remove near-duplicates caused by thick borders.
    unique = []
    for box in candidates:
        if any(sum(abs(a - b) for a, b in zip(box, old)) < 45 for old in unique):
            continue
        unique.append(box)
    for index, (x1, y1, x2, y2) in enumerate(unique, 1):
        margin = 8
        crop = image.crop((max(0, x1 - margin), max(0, y1 - margin), min(image.width, x2 + margin + 1), min(image.height, y2 + margin + 1)))
        crop = ImageOps.autocontrast(crop)
        name = f"page-{page:03d}-diagram-{index}.png"
        crop.save(OUT / name)
        manifest.append(f"{page}\t{index}\t{x1},{y1},{x2},{y2}\t{name}")

# The lower-right board on source page 59 has a slightly broken scanned
# border, so the automatic border detector does not recognize it reliably.
# Crop it explicitly from the original page at the verified board bounds.
manual_crops = {
    "page-059-diagram-2.png": (893, 1397, 1382, 1881),
}
for name, box in manual_crops.items():
    page = int(name[5:8])
    image = Image.open(SOURCE / f"page-{page:03d}.png").convert("L")
    crop = ImageOps.autocontrast(image.crop(box))
    crop.save(OUT / name)
    manifest.append(f"{page}\tmanual\t{','.join(map(str, box))}\t{name}")

(ROOT / "diagram_manifest.tsv").write_text("\n".join(manifest), encoding="utf-8")
print(f"Extracted {len(manifest)} diagrams")
