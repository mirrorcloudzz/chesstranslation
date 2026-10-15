from pathlib import Path
import json
import pdfplumber

root = Path(r"C:\Users\12059\Documents\Codex\chess")
pdf_dir = root / "output" / "pdf"
data = json.loads((root / "tmp" / "pdfs" / "middlegame_final_four" / "reviewed_segments.json").read_text(encoding="utf-8"))

pdfs = {
    5: pdf_dir / "chess_middlegame_planning_chapter_five_active_pawns_bilingual_proof_v1.pdf",
    6: pdf_dir / "chess_middlegame_planning_chapter_six_heavy_pieces_bilingual_proof_v1.pdf",
    7: pdf_dir / "chess_middlegame_planning_chapter_seven_manoeuvring_initiative_bilingual_proof_v1.pdf",
    8: pdf_dir / "chess_middlegame_planning_chapter_eight_two_bishops_bilingual_proof_v1.pdf",
}

for chapter, path in pdfs.items():
    expected = [r["segment_id"] for r in data if r["chapter"] == chapter]
    oob = []
    with pdfplumber.open(path) as pdf:
        texts = []
        for page_no, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            texts.append(text)
            for ch in page.chars:
                if ch["x0"] < -0.5 or ch["x1"] > page.width + 0.5 or ch["top"] < -0.5 or ch["bottom"] > page.height + 0.5:
                    oob.append((page_no, ch.get("text", ""), ch["x0"], ch["x1"], ch["top"], ch["bottom"]))
        joined = "\n".join(texts)
        missing = [seg_id for seg_id in expected if seg_id not in joined]
        print(path.name)
        print(f"  pages={len(pdf.pages)} bytes={path.stat().st_size} expected_ids={len(expected)} missing_ids={len(missing)} oob_chars={len(oob)}")
        print(f"  first_id={expected[0]} present={expected[0] in joined} last_id={expected[-1]} present={expected[-1] in joined}")
        if missing:
            print("  missing sample:", missing[:10])
        if oob:
            print("  oob sample:", oob[:5])

