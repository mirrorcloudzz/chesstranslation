from pathlib import Path

import numpy as np
from PIL import Image, ImageOps


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\pdfs\middlegame_chapters12")
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
        for group in groups:
            gy, gx1, gx2 = group[-1]
            if y - gy <= 8 and abs(x1 - gx1) <= 25 and abs(x2 - gx2) <= 25:
                group.append((y, x1, x2))
                break
        else:
            groups.append([(y, x1, x2)])
    return [
        (
            round(sum(value[0] for value in group) / len(group)),
            round(sum(value[1] for value in group) / len(group)),
            round(sum(value[2] for value in group) / len(group)),
        )
        for group in groups
    ]


manifest = []
for page in range(62, 89):
    path = SOURCE / f"page-{page:03d}.png"
    image = Image.open(path).convert("L")
    array = np.asarray(image)
    lines = []
    for y in range(array.shape[0]):
        for x1, x2 in dark_runs(array[y]):
            if 300 <= x2 - x1 + 1 <= 650:
                lines.append((y, x1, x2))
    candidates = []
    grouped = group_lines(lines)
    for index, top in enumerate(grouped):
        ty, tx1, tx2 = top
        top_width = tx2 - tx1 + 1
        for bottom in grouped[index + 1 :]:
            by, bx1, bx2 = bottom
            height = by - ty
            if height < 300:
                continue
            if height > 650:
                break
            bottom_width = bx2 - bx1 + 1
            if (
                abs(tx1 - bx1) <= 35
                and abs(tx2 - bx2) <= 35
                and abs(height - (top_width + bottom_width) / 2) <= 45
            ):
                candidates.append((min(tx1, bx1), ty, max(tx2, bx2), by))
                break
    unique = []
    for box in candidates:
        if any(sum(abs(a - b) for a, b in zip(box, old)) < 45 for old in unique):
            continue
        unique.append(box)
    for index, (x1, y1, x2, y2) in enumerate(unique, 1):
        margin = 8
        crop = image.crop(
            (
                max(0, x1 - margin),
                max(0, y1 - margin),
                min(image.width, x2 + margin + 1),
                min(image.height, y2 + margin + 1),
            )
        )
        crop = ImageOps.autocontrast(crop)
        name = f"page-{page:03d}-diagram-{index}.png"
        crop.save(OUT / name)
        manifest.append(f"{page}\t{index}\t{x1},{y1},{x2},{y2}\t{name}")

(ROOT / "diagram_manifest.tsv").write_text("\n".join(manifest), encoding="utf-8")
print(f"Extracted {len(manifest)} diagrams")
