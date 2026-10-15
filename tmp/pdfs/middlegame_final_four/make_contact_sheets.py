from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\pdfs\middlegame_final_four")
for chapter in (5, 6, 7, 8):
    src = root / f"qa_ch{chapter}"
    files = sorted(src.glob("page-*.png"))
    out = root / f"contacts_ch{chapter}"
    out.mkdir(exist_ok=True)
    cols, rows = 4, 5
    tw, th, label = 210, 297, 24
    gap = 10
    for sheet_no, start in enumerate(range(0, len(files), cols * rows), 1):
        batch = files[start:start + cols * rows]
        canvas = Image.new("RGB", (cols * (tw + gap) + gap, rows * (th + label + gap) + gap), "#d7d7d7")
        draw = ImageDraw.Draw(canvas)
        for i, path in enumerate(batch):
            r, c = divmod(i, cols)
            im = Image.open(path).convert("RGB")
            im.thumbnail((tw, th))
            x = gap + c * (tw + gap) + (tw - im.width) // 2
            y = gap + r * (th + label + gap)
            canvas.paste(im, (x, y))
            draw.text((gap + c * (tw + gap), y + th + 2), f"p{start + i + 1}", fill="black")
        canvas.save(out / f"contact-{sheet_no:02d}.png")
        print(out / f"contact-{sheet_no:02d}.png")
