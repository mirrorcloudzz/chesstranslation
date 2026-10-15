from pathlib import Path
import re
import pdfplumber

root = Path(r"C:\Users\12059\Documents\Codex\chess")
old = root / "output" / "pdf" / "chess_middlegame_planning_chapter_four_centre_illustrated_proof_v3.pdf"
new = root / "output" / "pdf" / "chess_middlegame_planning_chapter_four_centre_illustrated_proof_v4.pdf"

def inspect(path):
    with pdfplumber.open(path) as pdf:
        texts = [p.extract_text() or "" for p in pdf.pages]
        image_count = sum(len(p.images) for p in pdf.pages)
        oob = []
        for n, page in enumerate(pdf.pages, 1):
            for ch in page.chars:
                if ch["x0"] < -0.5 or ch["x1"] > page.width + 0.5 or ch["top"] < -0.5 or ch["bottom"] > page.height + 0.5:
                    oob.append((n, ch.get("text", "")))
        return texts, image_count, oob

old_text, old_images, old_oob = inspect(old)
new_text, new_images, new_oob = inspect(new)
norm = lambda s: re.sub(r"版本\s*[34]", "版本 X", s)
different = [i + 1 for i, (a, b) in enumerate(zip(old_text, new_text)) if norm(a) != norm(b)]
print(f"old_pages={len(old_text)} new_pages={len(new_text)} old_images={old_images} new_images={new_images}")
print(f"text_different_pages={different} old_oob={len(old_oob)} new_oob={len(new_oob)}")
print("page40 caption present=", "黑方走完26... c4后的局面" in new_text[39])
print("v4 size=", new.stat().st_size)
