from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\pdfs\middlegame_chapter")
paths = sorted((root / "diagrams").glob("*.png"))
thumb_w, thumb_h = 220, 245
cols = 6
rows = (len(paths) + cols - 1) // cols
sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), "white")
draw = ImageDraw.Draw(sheet)
for i, path in enumerate(paths):
    image = Image.open(path).convert("RGB")
    image.thumbnail((190, 205))
    x = (i % cols) * thumb_w + (thumb_w - image.width) // 2
    y = (i // cols) * thumb_h + 22
    sheet.paste(image, (x, y))
    draw.text(((i % cols) * thumb_w + 8, (i // cols) * thumb_h + 3), path.stem.replace("page-", "p"), fill="black")
sheet.save(root / "diagram_contact_sheet.png")
