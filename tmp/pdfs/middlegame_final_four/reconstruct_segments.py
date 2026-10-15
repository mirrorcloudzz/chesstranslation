import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"

CHAPTERS = {
    5: (145, 176, "More about active play with pawns", "进一步谈兵的积极行动"),
    6: (177, 195, "The Struggle with Heavy Pieces", "重子斗争"),
    7: (196, 216, "Manoeuvring. About the Initiative", "调动与主动权"),
    8: (217, 227, "The Two Bishops", "双象"),
}

START_PAGES = {start for start, _end, _en, _zh in CHAPTERS.values()}


def merge_same_line(rows):
    lines = []
    for row in sorted(rows, key=lambda item: (item["y"], item["x"])):
        text = row["text"].strip()
        if not text or row.get("score", 1) < 0.72:
            continue
        if re.fullmatch(r"[^A-Za-z0-9]+", text):
            continue
        if lines and abs(row["y"] - lines[-1]["y"]) <= 12:
            lines[-1]["parts"].append((row["x"], text))
            lines[-1]["x"] = min(lines[-1]["x"], row["x"])
            lines[-1]["right"] = max(lines[-1]["right"], row["right"])
            lines[-1]["bottom"] = max(lines[-1]["bottom"], row["bottom"])
        else:
            lines.append({
                "x": row["x"], "right": row["right"], "y": row["y"],
                "bottom": row["bottom"], "parts": [(row["x"], text)],
            })
    for line in lines:
        line["text"] = " ".join(text for _, text in sorted(line["parts"]))
    return lines


def clean_line(text):
    text = text.replace("\ufffd", '"').replace("“", '"').replace("”", '"')
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("…", "...").replace(".. .", "...")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\b([01]):([01])\b", r"\1-\2", text)
    text = text.replace("1/2:1/2", "1/2-1/2")
    text = re.sub(r"\b0-0-0\b", "O-O-O", text)
    text = re.sub(r"\b0-0\b", "O-O", text)
    text = re.sub(r"\b(\d{1,2})\s*\.{2}\s+", r"\1... ", text)
    corrections = {
        "correspondinly": "correspondingly", "himseif": "himself", " 0r ": " or ",
        "difference e between": "difference between", "concrete p plan": "concrete plan",
        "tLasker": "Lasker", "iand ": "and ", "some other s sort": "some other sort",
        "manoeuvering g merited": "manoeuvering merited", "activity 1 of": "activity of",
        "interests sn about": "interests us about", " v whether": " whether",
    }
    for old, new in corrections.items():
        text = text.replace(old, new)
    return text


MOVE = r"(?:O-O-O|O-O|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)"
MOVE_RE = re.compile(rf"(?<![A-Za-z0-9])(?:\d{{1,2}}\s*\.(?:\.\.)?\s*)?{MOVE}(?![A-Za-z0-9])")


def line_kind(text):
    if re.fullmatch(r"\d{1,3}", text):
        return "page_number"
    if text.startswith("Chapter "):
        return "chapter"
    if re.search(r"(?:Opening|Defence|Defense|Gambit|Game|System|Variation)$", text) and len(text) < 72:
        return "heading"
    if re.match(r"^(White|Black)\s*:", text):
        return "metadata"
    if re.match(r"^\([^)]*(?:18|19|20)\d{2}[^)]*\)$", text):
        return "metadata"
    moves = MOVE_RE.findall(text)
    words = re.findall(r"[A-Za-z]{5,}", text)
    if moves and not words and (len(moves) >= 2 or re.match(r"^\d{1,2}\s*\.{0,3}\s*", text)):
        return "moves"
    return "body"


def join_text(left, right):
    if left.endswith("-") and right and right[0].islower():
        return left[:-1] + right
    return left + " " + right


def column_segments(rows, page, side):
    lines = merge_same_line(rows)
    base = 76 if side == "left" else 824
    segments = []
    current = None
    for line in lines:
        # Chapter headings span the page and are inserted manually below.
        if page in START_PAGES and line["y"] < (450 if page == 145 else 390):
            continue
        text = clean_line(line["text"])
        kind = line_kind(text)
        if kind == "page_number":
            continue
        indented = line["x"] >= base + 32
        explicit = kind in {"chapter", "heading", "metadata", "moves"}
        after_special = current and current["kind"] in {"chapter", "heading", "metadata", "moves"}
        if current is None or explicit or after_special or (indented and not current["text"].endswith("-")):
            if current:
                segments.append(current)
            current = {"page": page, "side": side, "kind": kind, "text": text}
        else:
            current["text"] = join_text(current["text"], text)
    if current:
        segments.append(current)
    return segments


def normalize_move_segment(text):
    text = re.sub(r"\b(\d{1,2})\s*\.{2}\s+", r"\1... ", text)
    text = re.sub(rf"(?<![.\d])(\d{{1,2}})\s+({MOVE})", r"\1. \2", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


all_segments = []
for chapter, (start, end, title_en, title_zh) in CHAPTERS.items():
    chapter_segments = [{
        "chapter": chapter, "page": start, "side": "full", "kind": "title",
        "text": title_en, "zh": title_zh,
    }]
    if chapter == 5:
        chapter_segments.append({
            "chapter": chapter, "page": start, "side": "full", "kind": "title",
            "text": "The pawn wedge and the reaction to it. The pawn nail. The phalanx of e- and f-pawns. Pawn storm.",
            "zh": "兵楔及其应对。钉子兵。e兵与f兵组成的兵阵。兵潮。",
        })
    for page in range(start, end + 1):
        rows = json.loads((SOURCE / f"page-{page:03d}-ocr.json").read_text(encoding="utf-8"))
        left = [row for row in rows if row["x"] < 790]
        right = [row for row in rows if row["x"] >= 790]
        chapter_segments.extend(column_segments(left, page, "left"))
        chapter_segments.extend(column_segments(right, page, "right"))

    cleaned = []
    for item in chapter_segments:
        item["chapter"] = chapter
        item["text"] = re.sub(r"\s+", " ", item["text"]).strip()
        if item["kind"] == "moves":
            item["text"] = normalize_move_segment(item["text"])
        # Drop obvious chessboard OCR fragments and empty debris.
        alpha = len(re.findall(r"[A-Za-z]", item["text"]))
        if item["kind"] == "body" and len(item["text"]) < 4 and alpha < 2:
            continue
        cleaned.append(item)

    coalesced = []
    continuations = re.compile(r"^(?:and|or|but|of|which|who|whose|that|an|a|the|for|to|on|in|with|by|from|as|than|while|since|because|pawns?\b)", re.I)
    for item in cleaned:
        if coalesced:
            previous = coalesced[-1]
            merge_moves = previous["kind"] == item["kind"] == "moves"
            merge_body = (
                previous["kind"] == item["kind"] == "body"
                and not re.search(r"[.!?][\"')\]]?$", previous["text"])
                and (item["text"][:1].islower() or continuations.match(item["text"]))
            )
            if merge_moves or merge_body:
                previous["text"] = join_text(previous["text"], item["text"])
                previous["page_end"] = item["page"]
                continue
        coalesced.append(item)

    for number, item in enumerate(coalesced, 1):
        item["segment_id"] = f"CH{chapter}-{number}"
    all_segments.extend(coalesced)

(ROOT / "segments_ocr.json").write_text(
    json.dumps(all_segments, ensure_ascii=False, indent=2), encoding="utf-8"
)

for chapter, (start, end, title_en, title_zh) in CHAPTERS.items():
    selected = [x for x in all_segments if x["chapter"] == chapter]
    lines = [f"# Chapter {chapter}: {title_en}", ""]
    for item in selected:
        lines.extend([f"## {item['segment_id']} (p. {item['page'] - 2})", "", item["text"], ""])
    (ROOT / f"chapter_{chapter}_english_ocr.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"chapter {chapter}: pages {start}-{end}, segments={len(selected)}")
