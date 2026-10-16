from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(str(Path(__file__).resolve().parents[3] / 'tmp/pdfs/middlegame_chapters12'))


def make(files, stem, columns, rows, thumb_size):
    thumb_w, thumb_h = thumb_size
    per_sheet = columns * rows
    for sheet_number, start in enumerate(range(0, len(files), per_sheet), 1):
        chosen = files[start : start + per_sheet]
        canvas = Image.new(
            "RGB",
            (columns * (thumb_w + 18), rows * (thumb_h + 34)),
            "#dde3df",
        )
        draw = ImageDraw.Draw(canvas)
        for index, path in enumerate(chosen):
            with Image.open(path) as source:
                image = source.convert("RGB")
                image.thumbnail((thumb_w, thumb_h))
            x = (index % columns) * (thumb_w + 18) + 9
            y = (index // columns) * (thumb_h + 34) + 25
            canvas.paste(image, (x, y))
            draw.text((x, y - 19), path.stem, fill="#1f2933")
        canvas.save(ROOT / f"{stem}-{sheet_number}.jpg", quality=90)


pages = [ROOT / "source" / f"page-{page:03d}.png" for page in range(62, 89)]
diagrams = sorted((ROOT / "diagrams").glob("*.png"))
make(pages, "source-contact", 5, 3, (235, 345))
make(diagrams, "diagram-contact", 6, 3, (190, 190))
