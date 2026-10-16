import json
import re
import sys
from pathlib import Path

DEPS = Path(str(Path(__file__).resolve().parents[3] / 'tmp/translation_deps'))
sys.path.insert(0, str(DEPS))

import argostranslate.translate


ROOT = Path(str(Path(__file__).resolve().parents[3]))
TMP = ROOT / "tmp" / "pdfs" / "middlegame_chapters34"
TRANS = ROOT / "translations" / "chess_middlegame_planning"


def normalize_ocr(text):
    replacements = {
        "0verall": "overall", "upby": "up by", "seige": "siege",
        "ensuing": "ensuing", "Ral": "Ra1", "Rhl": "Rh1",
        "Qel": "Qe1", "Bgl": "Bg1", "Nxel": "Nxe1",
        "Rgl": "Rg1", "Rcl": "Rc1", "Bel": "Be1",
        "Kcl": "Kc1", "Qcl": "Qc1", "al,": "a1,",
        " a-fileto": " a-file to", "t the": "the", " a arises": " arises",
        "g on": " on", "0r ": "or ", "follow. ing": "following",
        "consi- derably": "considerably", "mi- stake": "mistake",
        "op- ponent": "opponent", "pre- requisite": "prerequisite",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("，", ",").replace("）", ")")
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_moves(text):
    text = normalize_ocr(text)
    text = re.sub(r"(?<!\d)(\d{1,2})\s*\.\s*\.\s*\.\s*", r"\1... ", text)
    text = re.sub(r"(?<!\d)(\d{1,2})\s*\.\s*(?=[KQRBNOa-h])", r"\1. ", text)
    text = re.sub(r"(?<!\d)(\d{1,2})\s+(?=[KQRBNO][a-h1-8O])", r"\1. ", text)
    text = re.sub(r"\b([01])-([01])\b", r"\1-\2", text)
    return text


def should_join(previous, current):
    if previous["kind"] == current["kind"] == "moves" and previous["page"] == current["page"] and previous["side"] == current["side"]:
        return True
    if previous["kind"] == current["kind"] == "body":
        if not re.search(r"[.!?。！？][\"'”’)]?$", previous["text"]):
            if current["text"] and current["text"][0].islower():
                return True
            if previous["side"] == "left" and current["side"] == "right" and previous["page"] == current["page"]:
                return True
            if previous["side"] == "right" and current["side"] == "left" and current["page"] == previous["page"] + 1:
                return True
    return False


def merge_segments(raw):
    merged = []
    for item in raw:
        item = dict(item)
        item["text"] = normalize_moves(item["text"]) if item["kind"] == "moves" else normalize_ocr(item["text"])
        if merged and should_join(merged[-1], item):
            merged[-1]["text"] = normalize_ocr(merged[-1]["text"] + " " + item["text"])
            merged[-1]["page_end"] = item["page"]
        else:
            item["page_end"] = item["page"]
            merged.append(item)
    return merged


MOVE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:\d{1,2}\.(?:\.\.)?\s*)?"
    r"(?:O-O-O|O-O|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)"
    r"(?![A-Za-z0-9])"
)


def protect_moves(text):
    protected = []
    def repl(match):
        token = f"MOVETOKEN{len(protected)}X"
        protected.append(match.group(0))
        return token
    return MOVE_PATTERN.sub(repl, text), protected


def restore_moves(text, protected):
    for index, value in enumerate(protected):
        text = text.replace(f"MOVETOKEN{index}X", value)
    return text


def chunks(text, limit=520):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    output = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= limit:
            current = (current + " " + sentence).strip()
            continue
        if current:
            output.append(current)
        if len(sentence) <= limit:
            current = sentence
            continue
        parts = re.split(r"(?<=[,;:])\s+", sentence)
        current = ""
        for part in parts:
            if len(current) + len(part) + 1 <= limit:
                current = (current + " " + part).strip()
            else:
                if current:
                    output.append(current)
                current = part
    if current:
        output.append(current)
    return output


NAME_MAP = {
    "Marco": "马尔科", "Muller": "穆勒", "Lasker": "拉斯克",
    "Showalter": "肖瓦尔特", "Treybal": "特雷巴尔",
    "Capablanca": "卡帕布兰卡", "Alekhine": "阿廖欣",
    "Evtifeev": "叶夫季费耶夫", "Danushevsky": "达努舍夫斯基",
    "Yudovich": "尤多维奇", "Alatortsev": "阿拉托尔采夫",
    "Pillsbury": "皮尔斯伯里", "Tarrasch": "塔拉什",
    "Schlechter": "施莱希特", "Nimzowitsch": "尼姆佐维奇",
    "Bogoljubow": "波戈留波夫", "Maroczy": "马洛契",
    "Chigorin": "齐果林", "Steinitz": "斯坦尼茨",
    "Rubinstein": "鲁宾斯坦", "Reti": "列蒂",
    "Spielmann": "斯皮尔曼", "Botvinnik": "鲍特维尼克",
    "Flohr": "弗洛尔", "Euwe": "尤伟", "Keres": "克列斯",
    "Smyslov": "斯梅斯洛夫", "Kotov": "科托夫",
}


def polish(text):
    replacements = {
        "怀特": "白方", "布莱克": "黑方", "白棋": "白方", "黑棋": "黑方",
        "国王的侧翼": "王翼", "国王侧翼": "王翼", "王的侧翼": "王翼",
        "女王的侧翼": "后翼", "女王侧翼": "后翼", "皇后侧翼": "后翼",
        "国王一侧": "王翼", "女王一侧": "后翼",
        "主教": "象", "骑士": "马", "女王": "后", "皇后": "后",
        "国王": "王", "典当": "兵", "卢克": "车", "鲁克": "车",
        "小件": "轻子", "小棋子": "轻子", "重件": "重子",
        "材料优势": "子力优势", "物质优势": "子力优势", "材料损失": "子力损失",
        "发展棋子": "出子", "棋子的发展": "出子", "棋子的开发": "出子",
        "发展这些棋子": "出子", "节奏": "先手",
        "检查配偶": "将杀", "伙伴": "将杀", "僵局": "逼和",
        "弱动作": "软着", "中间动作": "过渡着",
        "后续行动": "后续手段", "后续措施": "后续手段",
        "开放文件": "开放线", "打开文件": "打开线", "文件上的": "线上的",
        "中心舞台": "中局阶段", "中央阶段": "中局阶段",
        "棋手的行动": "棋手的行棋", "移动": "步",
        "反击": "反击", "牺牲交换": "弃半子", "交换牺牲": "弃半子",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    for letter in "abcdefgh":
        text = text.replace(f"{letter}-file", f"{letter}线")
        text = text.replace(f"{letter} file", f"{letter}线")
        text = text.replace(f"{letter}-pawn", f"{letter}兵")
        text = text.replace(f"{letter} pawn", f"{letter}兵")
    for old, new in NAME_MAP.items():
        text = text.replace(old, new)
    text = text.replace("Bird's Opening", "飞鸟开局")
    text = text.replace("English Opening", "英格兰开局")
    text = text.replace("Queen's Gambit", "后翼弃兵")
    text = text.replace("King's Indian Defence", "老印度防御")
    text = text.replace("Nimzo-Indian Defence", "尼姆佐维奇防御")
    text = text.replace("Slav Defence", "斯拉夫防御")
    text = text.replace("French Defence", "法兰西防御")
    text = text.replace("Sicilian Defence", "西西里防御")
    text = text.replace("Caro-Kann Defence", "卡罗-康防御")
    text = text.replace("Dutch Defence", "荷兰防御")
    text = text.replace("Grunfeld Defence", "格林菲尔德防御")
    text = re.sub(r"\b([a-h])线线\b", r"\1线", text)
    text = re.sub(r"\s+([，。；：！？,.!?;:])", r"\1", text)
    text = text.replace(",", "，").replace(";", "；").replace(":", "：")
    text = text.replace(".", "。").replace("?", "？").replace("!", "！")
    text = re.sub(r"([。！？]){2,}", r"\1", text)
    return text.strip()


MANUAL = {
    "Chapter Three": "第三章",
    "Play on the a-file": "a线上的战斗",
    "Chapter Four": "第四章",
    "The centre and its strategical significance": "中心及其战略意义",
    "The knight on e5 and d5 (e4 and d4). The pawn centre. Attack with the central \"hanging\" pawns.": "e5与d5（e4与d4）上的马。兵中心。以中央“悬兵”发动进攻",
    "Bird's Opening": "飞鸟开局",
    "English Opening": "英格兰开局",
}


def translate_text(text, kind):
    if kind == "moves":
        return text
    if text in MANUAL:
        return MANUAL[text]
    if kind == "metadata":
        return polish(text.replace("White", "白方").replace("Black", "黑方"))
    protected_text, protected = protect_moves(text)
    translated_parts = []
    for part in chunks(protected_text):
        translated_parts.append(argostranslate.translate.translate(part, "en", "zh"))
    translated = " ".join(translated_parts)
    translated = restore_moves(translated, protected)
    return polish(translated)


raw = json.loads((TMP / "segments.json").read_text(encoding="utf-8"))
segments = merge_segments(raw)

# Repair the decorative, cross-column Chapter Four title.
for item in segments:
    if item["page"] == 101 and item["text"] == "The centre and its Strategical":
        item["text"] = "The centre and its strategical significance"
        item["kind"] = "title"
    elif item["page"] == 101 and item["text"] == "Significance against Tarrasch and Schlechter. These proceeded identically up to the 11th move:":
        item["text"] = "Against Tarrasch and Schlechter, the games proceeded identically up to the 11th move:"
    elif item["page"] == 101 and item["text"] == "The knight on e5 and d5 (e4 and d4). The pawn centre.":
        item["text"] = "The knight on e5 and d5 (e4 and d4). The pawn centre. Attack with the central \"hanging\" pawns."
        item["kind"] = "title"
    elif item["page"] == 101 and item["text"].startswith("Attack with the central pawns."):
        item["text"] = "The part of the board which includes the squares e4, d4, e5 and d5 is called the centre. These squares are called central."

for item in segments:
    item["zh"] = translate_text(item["text"], item["kind"])

(TMP / "translated_segments.json").write_text(
    json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8"
)

for chapter, start, end, prefix, title in (
    (3, 89, 100, "13_chapter_three_a_file", "第三章：a线上的战斗"),
    (4, 101, 144, "14_chapter_four_centre", "第四章：中心及其战略意义"),
):
    selected = [item for item in segments if start <= item["page"] <= end]
    en_lines = [f"# {title}（英文 OCR 校对稿）", ""]
    zh_lines = [f"# {title}（中文初译）", ""]
    counter = 0
    for item in selected:
        if item["kind"] == "chapter":
            continue
        counter += 1
        segment_id = f"CH{chapter}-{counter}"
        en_lines.extend([f"## {segment_id}", "", item["text"], ""])
        zh_lines.extend([f"## {segment_id}", "", item["zh"], ""])
    (TRANS / f"{prefix}_en_ocr.md").write_text("\n".join(en_lines), encoding="utf-8")
    (TRANS / f"{prefix}_zh.md").write_text("\n".join(zh_lines), encoding="utf-8")
    print(f"chapter{chapter}_segments={counter}")
