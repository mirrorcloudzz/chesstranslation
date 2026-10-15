from pathlib import Path
from PIL import Image, ImageDraw

root = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\pdfs\qa")
for folder_name in ("planning_v2", "planning_v3", "planning_v3_verified", "planning_v4", "planning_v5", "planning_v5_verified", "planning_v6", "planning_v7", "chapter1", "chapter_one_v2", "chapter2", "chapter_one_full_v3", "chapter_two_full_v2"):
    folder = root / folder_name
    files = sorted(folder.glob("p-*.jpg"))
    thumb_w, thumb_h = 238, 337
    per_sheet = 20
    for sheet_no, start in enumerate(range(0, len(files), per_sheet), 1):
        chosen = files[start:start + per_sheet]
        canvas = Image.new("RGB", (5 * (thumb_w + 14), 4 * (thumb_h + 28)), "#dfe5e1")
        draw = ImageDraw.Draw(canvas)
        for i, path in enumerate(chosen):
            with Image.open(path) as source:
                image = source.convert("RGB")
                image.thumbnail((thumb_w, thumb_h))
                x = (i % 5) * (thumb_w + 14) + 7
                y = (i // 5) * (thumb_h + 28) + 20
                canvas.paste(image, (x, y))
                draw.text((x, 3 + (i // 5) * (thumb_h + 28)), path.stem, fill="#1f2933")
        canvas.save(root / f"{folder_name}-contact-{sheet_no}.jpg", quality=88)
