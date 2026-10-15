from pathlib import Path
from PIL import Image, ImageDraw

root = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\pdfs\middlegame_chapter\final_render")
paths = sorted(root.glob("page-*.png"))
cols = 5
cell_w, cell_h = 250, 360
rows = (len(paths) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "#dadada")
draw = ImageDraw.Draw(sheet)
for i, path in enumerate(paths):
    image = Image.open(path).convert("RGB")
    image.thumbnail((225, 320))
    x0 = (i % cols) * cell_w + (cell_w - image.width) // 2
    y0 = (i // cols) * cell_h + 25
    sheet.paste(image, (x0, y0))
    draw.text(((i % cols) * cell_w + 10, (i // cols) * cell_h + 6), f"PDF {i + 1}", fill="black")
sheet.save(root.parent / "final_contact_sheet.png")
