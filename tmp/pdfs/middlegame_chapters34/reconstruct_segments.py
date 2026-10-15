import json
import re
from pathlib import Path


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\pdfs\middlegame_chapters34")
SOURCE = ROOT / "source"


def merge_same_line(rows):
    lines = []
    for row in sorted(rows, key=lambda item: (item["y"], item["x"])):
        text = row["text"].strip()
        if not text or re.fullmatch(r"[^A-Za-z0-9]+", text):
            continue
        if lines and abs(row["y"] - lines[-1]["y"]) <= 10:
            lines[-1]["parts"].append((row["x"], text))
            lines[-1]["x"] = min(lines[-1]["x"], row["x"])
            lines[-1]["bottom"] = max(lines[-1]["bottom"], row["bottom"])
        else:
            lines.append({
                "x": row["x"], "y": row["y"], "bottom": row["bottom"],
                "parts": [(row["x"], text)],
            })
    for line in lines:
        line["text"] = " ".join(text for _, text in sorted(line["parts"]))
    return lines


def clean_line(text):
    text = text.replace("…", "...").replace(".. .", "...")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\b([01]):([01])\b", r"\1-\2", text)
    text = text.replace("1/2:1/2", "1/2-1/2")
    return text


def line_kind(text):
    if re.fullmatch(r"\d{1,3}", text):
        return "page_number"
    if text in {"Chapter Three", "Chapter Four"}:
        return "chapter"
    if text in {"Play on the a-file"}:
        return "title"
    if re.search(r"Opening$|Defence$|Gambit$|Game$", text) and len(text) < 55:
        return "heading"
    if re.match(r"^(White|Black)\s*:", text):
        return "metadata"
    if re.match(r"^\([^)]*(?:18|19)\d{2}[^)]*\)$", text):
        return "metadata"
    move_tokens = re.findall(r"(?:\d+\s*\.{0,3}\s*)?(?:[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?|[O0]-[O0](?:-[O0])?)", text)
    long_words = re.findall(r"[A-Za-z]{6,}", text)
    if move_tokens and not long_words and (len(move_tokens) >= 2 or re.match(r"^\d+\s*\.{0,3}\s*", text)):
        return "moves"
    return "body"


def join_text(left, right):
    if left.endswith("-") and right and right[0].islower():
        return left[:-1] + right
    return left + " " + right


def column_segments(rows, page, side):
    lines = merge_same_line(rows)
    if not lines:
        return []
    base = 80 if side == "left" else 827
    segments = []
    current = None
    for line in lines:
        text = clean_line(line["text"])
        kind = line_kind(text)
        if kind == "page_number":
            continue
        indented = line["x"] >= base + 34
        explicit = kind in {"chapter", "title", "heading", "metadata", "moves"}
        boundary_after_special = current and current["kind"] in {"chapter", "title", "heading", "metadata"}
        if current is None or explicit or boundary_after_special or (indented and not current["text"].endswith("-")):
            if current:
                segments.append(current)
            current = {"page": page, "side": side, "kind": kind, "text": text}
        else:
            current["text"] = join_text(current["text"], text)
            if current["kind"] == "metadata" and kind == "body":
                current["kind"] = "body"
    if current:
        segments.append(current)
    return segments


all_segments = []
for page in range(89, 145):
    rows = json.loads((SOURCE / f"page-{page:03d}-ocr.json").read_text(encoding="utf-8"))
    left = [row for row in rows if row["x"] < 820]
    right = [row for row in rows if row["x"] >= 820]
    all_segments.extend(column_segments(left, page, "left"))
    all_segments.extend(column_segments(right, page, "right"))

for segment in all_segments:
    text = segment["text"]
    text = re.sub(r"\b0-0-0\b", "O-O-O", text)
    text = re.sub(r"\b0-0\b", "O-O", text)
    text = re.sub(r"\s+", " ", text).strip()
    segment["text"] = text

(ROOT / "segments.json").write_text(
    json.dumps(all_segments, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"segments={len(all_segments)}")
print(f"chapter3={sum(1 for item in all_segments if 89 <= item['page'] <= 100)}")
print(f"chapter4={sum(1 for item in all_segments if 101 <= item['page'] <= 144)}")
