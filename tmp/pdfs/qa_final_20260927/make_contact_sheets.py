from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONT = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)

for chapter in ("ch2", "ch3", "ch4"):
    images = sorted((ROOT / chapter).glob("page-*.jpg"))
    for batch, start in enumerate(range(0, len(images), 20), 1):
        subset = images[start:start + 20]
        thumbs = []
        for path in subset:
            with Image.open(path) as source:
                image = source.convert("RGB")
                image.thumbnail((310, 440))
                tile = Image.new("RGB", (330, 480), "white")
                x = (330 - image.width) // 2
                tile.paste(image, (x, 28))
                draw = ImageDraw.Draw(tile)
                draw.text((10, 4), path.stem, fill="black", font=FONT)
                thumbs.append(tile)
        rows = (len(thumbs) + 3) // 4
        sheet = Image.new("RGB", (4 * 330, rows * 480), "#D9DEE2")
        for index, tile in enumerate(thumbs):
            sheet.paste(tile, ((index % 4) * 330, (index // 4) * 480))
        sheet.save(ROOT / f"{chapter}-contact-{batch}.jpg", quality=88)
