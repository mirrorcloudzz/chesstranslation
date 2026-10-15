import json
import re
import sys
from pathlib import Path

DEPS = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\translation_deps")
sys.path.insert(0, str(DEPS))

import ctranslate2
import sentencepiece as spm


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess")
TMP = ROOT / "tmp" / "pdfs" / "middlegame_chapters34"
TRANS = ROOT / "translations" / "chess_middlegame_planning"
MODEL = ROOT / "tmp" / "marian_en_zh_ct2"

src_sp = spm.SentencePieceProcessor(model_file=str(MODEL / "source.spm"))
tgt_sp = spm.SentencePieceProcessor(model_file=str(MODEL / "target.spm"))
translator = ctranslate2.Translator(
    str(MODEL), device="cpu", compute_type="int8", intra_threads=8, inter_threads=1
)


MANUAL = {
    "Chapter Three": "第三章",
    "Play on the a-file": "a线上的战斗",
    "Chapter Four": "第四章",
    "The centre and its strategical significance": "中心及其战略意义",
    "The knight on e5 and d5 (e4 and d4). The pawn centre. Attack with the central \"hanging\" pawns.": "e5与d5（e4与d4）上的马。兵中心。以中央“悬兵”发动进攻",
    "Bird's Opening": "飞鸟开局",
    "English Opening": "英格兰开局",
}

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
    "Bernstein": "伯恩斯坦", "Marshall": "马歇尔",
    "Janowski": "雅诺夫斯基", "Teichmann": "泰希曼",
    "Ragozin": "拉戈津", "Levenfish": "列文菲什",
}

OPENING_MAP = {
    "Bird's Opening": "飞鸟开局", "English Opening": "英格兰开局",
    "Queen's Gambit": "后翼弃兵", "King's Indian Defence": "老印度防御",
    "Nimzo-Indian Defence": "尼姆佐维奇防御", "Slav Defence": "斯拉夫防御",
    "French Defence": "法兰西防御", "Sicilian Defence": "西西里防御",
    "Caro-Kann Defence": "卡罗-康防御", "Dutch Defence": "荷兰防御",
    "Grunfeld Defence": "格林菲尔德防御", "Indian Defence": "印度防御",
}

MOVE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:\d{1,2}\.(?:\.\.)?\s*)?"
    r"(?:O-O-O|O-O|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)"
    r"(?![A-Za-z0-9])"
)

TERM_PATTERNS = [
    (r"castling (?:on )?the queen'?s side|castle queen'?s side", "长易位"),
    (r"castling (?:on )?the king'?s side|castle king'?s side|king'?s side castling", "短易位"),
    (r"king'?s flank|king'?s wing", "王翼"),
    (r"queen'?s flank|queen'?s wing", "后翼"),
    (r"connected passed pawns?", "相连通兵"),
    (r"passed pawns?", "通兵"),
    (r"pawn chain", "兵链"),
    (r"pawn centre|pawn center", "兵中心"),
    (r"pawn advance", "冲兵"),
    (r"minor pieces?", "轻子"),
    (r"heavy pieces?", "重子"),
    (r"sacrifice of the exchange|exchange sacrifice", "弃半子"),
    (r"intermediate move", "过渡着"),
    (r"weak move", "一步软着"),
    (r"opening handbooks?", "开局谱"),
    (r"book reply", "常见谱招"),
    (r"material advantage", "子力优势"),
    (r"material loss", "子力损失"),
    (r"development of (?:the )?pieces|develop (?:the )?pieces", "出子"),
    (r"knight'?s pawn", "马前兵"),
    (r"(?:the )?([a-h])-file", None),
    (r"(?:the )?([a-h])-pawn", None),
    (r"open file", "开放线"),
    (r"files?", "线"),
    (r"ranks?", "横线"),
    (r"central squares?", "中心格"),
    (r"weak squares?", "弱格"),
    (r"squares?", "格"),
    (r"rooks?", "车"),
    (r"bishops?", "象"),
    (r"knights?", "马"),
    (r"queens?", "后"),
    (r"kings?", "王"),
    (r"pawns?", "兵"),
    (r"pieces?", "棋子"),
    (r"tempo", "先手"),
    (r"stalemate", "逼和"),
    (r"sacrifice", "弃子"),
]


def label(index):
    value = index
    letters = ""
    while True:
        letters = chr(ord("A") + value % 26) + letters
        value = value // 26 - 1
        if value < 0:
            return letters


def protect(text):
    values = []
    def add(value):
        key = label(len(values))
        values.append((key, value))
        return f"[[{key}]]"

    # Names and opening names are protected before generic chess terms.
    for source, target in sorted({**OPENING_MAP, **NAME_MAP}.items(), key=lambda pair: -len(pair[0])):
        text = re.sub(re.escape(source), lambda _: add(target), text, flags=re.I)

    for pattern, fixed in TERM_PATTERNS:
        def term_repl(match, fixed=fixed):
            if fixed is not None:
                return add(fixed)
            letter = match.group(1).lower()
            if "file" in match.group(0).lower():
                return add(f"{letter}线")
            return add(f"{letter}兵")
        text = re.sub(pattern, term_repl, text, flags=re.I)

    text = MOVE_PATTERN.sub(lambda match: add(match.group(0)), text)
    return text, values


def restore(text, values):
    for key, value in values:
        text = re.sub(rf"\[+\s*{re.escape(key)}\s*\]+", lambda _: value, text, flags=re.I)
    return text


def pure_moves(text):
    remainder = MOVE_PATTERN.sub(" ", text)
    remainder = re.sub(r"[\d\s.,;:()\-+/!?]+", " ", remainder)
    words = re.findall(r"[A-Za-z]{2,}", remainder)
    return len(words) <= 2 and all(word.lower() in {"etc", "or", "and"} for word in words)


def split_chunks(text, limit=430):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    output, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= limit:
            current = (current + " " + sentence).strip()
        else:
            if current:
                output.append(current)
            current = sentence
    if current:
        output.append(current)
    return output


def polish(text):
    replacements = {
        "怀特": "白方", "布莱克": "黑方", "白色": "白方", "黑色": "黑方",
        "白种人": "白方", "黑种人": "黑方", "白人": "白方", "黑人": "黑方",
        "棋手的动作": "棋手的行棋", "动作计划": "行动计划",
        "移动": "步", "下一步行动": "下一步", "中央": "中心",
        "获得一兵": "得兵", "赢得一兵": "得兵", "失去一兵": "丢兵",
        "夺回一兵": "吃回一兵", "收回一兵": "吃回一兵",
        "获得一个棋子": "得子", "失去一个棋子": "失子",
        "赢得后": "得后", "决定性优势": "胜势",
        "检验": "将军", "将死": "将杀",
        "延续": "后续手段", "续集": "后续手段",
        "发展": "出子", "前进": "冲兵",
        "玩耍": "行棋", "玩白牌": "执白", "游戏": "对局",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace(".", "。").replace(",", "，").replace(";", "；")
    text = text.replace(":", "：").replace("?", "？").replace("!", "！")
    text = re.sub(r"\s+([，。；：！？])", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


segments = json.loads((TMP / "translated_segments.json").read_text(encoding="utf-8"))
tasks = []
pending = {}

for index, item in enumerate(segments):
    text = item["text"]
    if text in MANUAL:
        item["zh"] = MANUAL[text]
        continue
    if pure_moves(text):
        item["zh"] = text
        continue
    protected, values = protect(text)
    parts = split_chunks(protected)
    pending[index] = {"values": values, "count": len(parts), "results": [None] * len(parts)}
    for part_index, part in enumerate(parts):
        tasks.append((index, part_index, part))

for start in range(0, len(tasks), 64):
    batch = tasks[start:start + 64]
    sources = [src_sp.encode(part, out_type=str) + ["</s>"] for _, _, part in batch]
    results = translator.translate_batch(
        sources, beam_size=1, max_decoding_length=384,
        batch_type="tokens", max_batch_size=64,
    )
    for (item_index, part_index, _), result in zip(batch, results):
        pending[item_index]["results"][part_index] = tgt_sp.decode(result.hypotheses[0])
    print(f"translated={min(start + len(batch), len(tasks))}/{len(tasks)}", flush=True)

for index, data in pending.items():
    translated = " ".join(data["results"])
    translated = restore(translated, data["values"])
    segments[index]["zh"] = polish(translated)

(TMP / "translated_segments_v2.json").write_text(
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
