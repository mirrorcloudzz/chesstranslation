import json
import re
import sys
import time
from pathlib import Path

DEPS = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\translation_deps")
sys.path.insert(0, str(DEPS))

from translatepy.translators.google import GoogleTranslate


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess")
TMP = Path(__file__).resolve().parent
TRANS = ROOT / "translations" / "chess_middlegame_planning"
translator = GoogleTranslate()

OPENING_MAP = {
    "Bogolyubov-Indian Defence": "波戈印度防御",
    "Reti Opening": "列蒂开局",
    "King's Indian Defence": "老印度防御",
    "Spanish Game": "西班牙开局",
    "Queen's Gambit": "后翼弃兵",
    "Hungarian Defence": "匈牙利防御",
    "Sicilian Defence": "西西里防御",
    "English Opening": "英国式开局",
    "Caro-Kann Defence": "卡罗-康防御",
    "Nimzo-Indian Defence": "尼姆佐维奇防御",
    "Queen's Pawn Opening": "后兵开局",
    "Queen's Indian Defence": "后印度防御",
    "French Defence": "法兰西防御",
    "Slav Defence": "斯拉夫防御",
    "Dutch Defence": "荷兰防御",
    "Alekhine Defence": "阿廖欣防御",
}

NAME_MAP = {
    "Alatortsev": "阿拉托尔采夫", "Levenfish": "列文菲什",
    "Capablanca": "卡帕布兰卡", "Marshall": "马歇尔", "Kan": "卡恩",
    "Polugayevsky": "波卢加耶夫斯基", "Suetin": "苏埃京",
    "Teichmann": "泰希曼", "Rubinstein": "鲁宾斯坦",
    "Chigorin": "齐果林", "Zukertort": "祖凯尔托特",
    "Halprin": "哈尔普林", "Pillsbury": "皮尔斯伯里",
    "Alekhine": "阿廖欣", "Breyer": "布雷耶", "Kasparyan": "卡斯帕里扬",
    "Flohr": "弗洛尔", "Vajda": "瓦伊达", "Bogolyubov": "波戈留波夫",
    "Lasker": "拉斯克", "Janowski": "雅诺夫斯基", "Tarrasch": "塔拉什",
    "Tartakover": "塔塔科维", "Nimzovich": "尼姆佐维奇",
    "Makogonov": "马科戈诺夫", "Smyslov": "斯梅斯洛夫",
    "Romanovsky": "罗曼诺夫斯基", "Botvinnik": "鲍特维尼克",
    "Yates": "耶茨", "Averbakh": "阿韦尔巴赫", "Petrosian": "彼得罗相",
    "Khasin": "哈辛", "Boleslavsky": "博列斯拉夫斯基",
    "Stahlberg": "斯塔尔贝里", "Burn": "伯恩", "Alapin": "阿拉平",
    "Keres": "克列斯", "Euwe": "尤伟", "Ragozin": "拉戈津",
    "Bronstein": "布龙斯坦", "Kotov": "科托夫", "Panov": "帕诺夫",
    "Geller": "盖勒", "Taimanov": "泰曼诺夫", "Schlechter": "施莱希特",
    "Steinitz": "斯坦尼茨", "Maroczy": "马洛契", "Spielmann": "斯皮尔曼",
}

PLACE_MAP = {
    "Moscow": "莫斯科", "Carlsbad": "卡尔斯巴德", "Vienna": "维也纳",
    "Mannheim": "曼海姆", "Hastings": "哈斯廷斯", "Semmering": "塞默灵",
    "Budapest": "布达佩斯", "London": "伦敦", "Sverdlovsk": "斯维尔德洛夫斯克",
    "Petersburg": "彼得堡", "Nurnberg": "纽伦堡", "Nuremberg": "纽伦堡",
}

MOVE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:\d{1,2}\.(?:\.\.)?\s*)?"
    r"(?:O-O-O|O-O|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)"
    r"(?![A-Za-z0-9])"
)

TERM_PATTERNS = [
    (r"mate in (\w+) moves?", None),
    (r"castl(?:e|ing) (?:on )?the queen'?s side|queen'?s side castling", "长易位"),
    (r"castl(?:e|ing) (?:on )?the king'?s side|king'?s side castling", "短易位"),
    (r"king'?s flank pawn majority", "王翼多兵"),
    (r"queen'?s flank pawn majority", "后翼多兵"),
    (r"king'?s flank|king'?s wing", "王翼"),
    (r"queen'?s flank|queen'?s wing", "后翼"),
    (r"connected passed pawns?", "相连通兵"),
    (r"passed pawns?", "通兵"),
    (r"backward pawns?", "落后兵"),
    (r"isolated pawns?", "孤兵"),
    (r"doubled pawns?", "叠兵"),
    (r"pawn chain", "兵链"),
    (r"pawn centre|pawn center", "兵中心"),
    (r"pawn wedge", "兵楔"),
    (r"pawn nail", "钉子兵"),
    (r"pawn phalanx|phalanx of (?:the )?[a-h](?:-| )? and (?:the )?[a-h]-?pawns", "兵阵"),
    (r"pawn storm", "兵潮"),
    (r"pawn advance|advance of the [a-h]-pawn|advance of a pawn", "冲兵"),
    (r"pawn break|break with the [a-h]-pawn", "冲兵突破"),
    (r"handling pawns", "运用兵"),
    (r"development of (?:the )?pieces|develop (?:the )?pieces", "出子"),
    (r"material advantage", "子力优势"),
    (r"material loss", "子力损失"),
    (r"material superiority", "子力优势"),
    (r"material gains?", "子力收益"),
    (r"sacrifice of the exchange|exchange sacrifice", "弃半子"),
    (r"lose the exchange|loss of the exchange", "丢掉半子"),
    (r"win the exchange", "赢得半子"),
    (r"intermediate move", "过渡着"),
    (r"weak move", "一步软着"),
    (r"attacking moves?", "进攻着法"),
    (r"continuation", "后续手段"),
    (r"opening handbooks?", "开局谱"),
    (r"book reply", "常见谱招"),
    (r"eternal knight", "铁马"),
    (r"heavy pieces?", "重子"),
    (r"minor pieces?", "轻子"),
    (r"two bishops", "双象"),
    (r"manoeuvring|manoeuvering|maneuvering", "调动"),
    (r"manoeuvres?|manoeuvers?|maneuvers?", "运子"),
    (r"initiative", "主动权"),
    (r"tempo", "先手"),
    (r"stalemate", "逼和"),
    (r"sacrifice", "弃子"),
    (r"central squares?", "中心格"),
    (r"weak squares?", "弱格"),
    (r"open files?", "开放线"),
    (r"mating threats?", "将杀威胁"),
    (r"castling", "易位"),
    (r"(?:the )?([a-h])-file", None),
    (r"(?:the )?([a-h])-rank", None),
    (r"attacking force", "攻击力量"),
    (r"piece activity", "子力活动"),
    (r"positional play", "局面型下法"),
    (r"exchange variation", "兑换变例"),
    (r"exchange of pieces", "兑子"),
    (r"\brooks?\b", "车"),
    (r"\bbishops?\b", "象"),
    (r"\bknights?\b", "马"),
    (r"\bqueens?\b", "后"),
    (r"\bkings?\b", "王"),
    (r"\bpawns?\b", "兵"),
    (r"\bpieces?\b", "棋子"),
    (r"\bsquares?\b", "格"),
    (r"\bfiles?\b", "线"),
    (r"\branks?\b", "横线"),
]

NUMBER_MAP = {
    "one": "一", "two": "二", "three": "三", "four": "四", "five": "五",
    "six": "六", "seven": "七", "eight": "八", "nine": "九", "ten": "十",
}


def pure_moves(text):
    remainder = MOVE_PATTERN.sub(" ", text)
    remainder = re.sub(r"[\d\s.,;:()\-+/!?]+", " ", remainder)
    words = re.findall(r"[A-Za-z]{2,}", remainder)
    return len(words) <= 2 and all(word.lower() in {"etc", "or", "and"} for word in words)


def protect(text):
    values = []

    def add(value):
        key = f"T{len(values):04d}"
        values.append((key, value))
        return f"[[{key}]]"

    dictionary = {**OPENING_MAP, **NAME_MAP, **PLACE_MAP}
    for source, target in sorted(dictionary.items(), key=lambda pair: -len(pair[0])):
        if source in NAME_MAP:
            pattern = rf"(?<![A-Za-z])(?:[A-Z](?:m)?\.\s*)?{re.escape(source)}\b"
        else:
            pattern = rf"\b{re.escape(source)}\b"
        text = re.sub(pattern, lambda _m, t=target: add(t), text, flags=re.I)

    for pattern, fixed in TERM_PATTERNS:
        def repl(match, fixed=fixed, pattern=pattern):
            if fixed is not None:
                return add(fixed)
            if "file" in pattern:
                return add(f"{match.group(1).lower()}线")
            if "rank" in pattern:
                return add(f"{match.group(1).lower()}横线")
            number = match.group(1).lower()
            return add(f"{NUMBER_MAP.get(number, number)}步杀")
        text = re.sub(pattern, repl, text, flags=re.I)

    text = MOVE_PATTERN.sub(lambda match: add(match.group(0)), text)
    return text, values


def restore(text, values):
    for key, value in values:
        text = re.sub(rf"\[+\s*{key}\s*\]+", lambda _m, v=value: v, text, flags=re.I)
    return text


def polish(text):
    replacements = {
        "白棋": "白方", "黑棋": "黑方", "白色": "白方", "黑色": "黑方",
        "王后": "后", "皇后": "后", "国王": "王", "骑士": "马", "主教": "象",
        "兵卒": "兵", "重型棋子": "重子", "小棋子": "轻子", "次要棋子": "轻子",
        "物质优势": "子力优势", "物质损失": "子力损失", "物质收益": "子力收益",
        "棋子的发展": "出子", "发展棋子": "出子", "发展子力": "出子",
        "兵的推进": "冲兵", "兵推进": "冲兵", "推进兵": "冲兵",
        "交换牺牲": "弃半子", "牺牲交换": "弃半子", "牺牲一枚棋子": "弃子",
        "中间着法": "过渡着", "中间招法": "过渡着", "弱着": "一步软着",
        "获得一个棋子": "得子", "赢得一个棋子": "得子", "丢失一个棋子": "失子",
        "赢得皇后": "得后", "赢得后": "得后", "夺回一兵": "吃回一兵", "收回一兵": "吃回一兵",
        "后续行动": "后续手段", "后续措施": "后续手段", "节奏": "先手",
        "将死": "将杀", "棋步": "步", "这着棋": "这步棋", "一着棋": "一步棋",
        "下一着": "下一步", "这着": "这步", "一着": "一步", "王位": "王的位置",
        "游戏": "对局", "比赛": "对局", "移动皇后": "动后", "移动骑士": "动马",
        "移动车": "动车", "移动主教": "动象", "英国开局": "英国式开局",
        "中心广场": "中心格", "方格": "格", "文件": "线", "排名": "横线",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("。.", "。").replace("，，", "，")
    text = text.replace(".", "。").replace(",", "，").replace(";", "；")
    text = text.replace(":", "：").replace("?", "？").replace("!", "！")
    text = re.sub(r"\s+([，。；：！？])", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def metadata_translation(text):
    match = re.match(r"^(White|Black)\s*:\s*(.+)$", text)
    if match:
        side = "白方" if match.group(1) == "White" else "黑方"
        name = match.group(2).replace("1.Kan", "I.Kan")
        for source, target in sorted(NAME_MAP.items(), key=lambda pair: -len(pair[0])):
            name = re.sub(rf"\b{re.escape(source)}\b", target, name, flags=re.I)
        return f"{side}：{name}"
    return None


def translate_batch(items):
    payload = "\n".join(f"[S{index:04d}]\n{text}" for index, text in items)
    last_error = None
    for attempt in range(4):
        try:
            translated = str(translator.translate(payload, "Chinese"))
            matches = list(re.finditer(r"\[S(\d{4})\]", translated))
            found = {}
            for pos, match in enumerate(matches):
                start = match.end()
                end = matches[pos + 1].start() if pos + 1 < len(matches) else len(translated)
                found[int(match.group(1))] = translated[start:end].strip()
            if all(index in found for index, _ in items):
                return found
            last_error = RuntimeError(f"marker mismatch expected={len(items)} found={len(found)}")
        except Exception as exc:
            last_error = exc
        time.sleep(2 * (attempt + 1))
    if len(items) > 1:
        middle = len(items) // 2
        found = translate_batch(items[:middle])
        found.update(translate_batch(items[middle:]))
        return found
    raise last_error


segments = json.loads((TMP / "segments_ocr.json").read_text(encoding="utf-8"))
prepared = {}
pending = []

for index, item in enumerate(segments):
    if item.get("zh"):
        continue
    if item["kind"] == "heading" and item["text"] in OPENING_MAP:
        item["zh"] = OPENING_MAP[item["text"]]
        continue
    meta = metadata_translation(item["text"]) if item["kind"] == "metadata" else None
    if meta:
        item["zh"] = meta
        continue
    if pure_moves(item["text"]):
        item["zh"] = item["text"]
        continue
    protected, values = protect(item["text"])
    prepared[index] = values
    pending.append((index, protected))

batches = []
current = []
size = 0
for item in pending:
    addition = len(item[1]) + 12
    if current and size + addition > 3500:
        batches.append(current)
        current, size = [], 0
    current.append(item)
    size += addition
if current:
    batches.append(current)

for batch_number, batch in enumerate(batches, 1):
    translations = translate_batch(batch)
    for index, _text in batch:
        translated = polish(translations[index])
        translated = restore(translated, prepared[index])
        translated = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", translated)
        segments[index]["zh"] = translated
    print(f"batch {batch_number}/{len(batches)} segments={len(batch)}", flush=True)
    time.sleep(0.35)

(TMP / "translated_segments.json").write_text(
    json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8"
)

PREFIXES = {
    5: "15_chapter_five_active_pawns",
    6: "16_chapter_six_heavy_pieces",
    7: "17_chapter_seven_manoeuvring_initiative",
    8: "18_chapter_eight_two_bishops",
}
TITLES = {
    5: "第五章：进一步谈兵的积极行动",
    6: "第六章：重子斗争",
    7: "第七章：调动与主动权",
    8: "第八章：双象",
}
for chapter in range(5, 9):
    selected = [x for x in segments if x["chapter"] == chapter]
    en = [f"# {TITLES[chapter]}（英文 OCR 校对稿）", ""]
    zh = [f"# {TITLES[chapter]}（中文初译）", ""]
    for item in selected:
        en.extend([f"## {item['segment_id']}", "", item["text"], ""])
        zh.extend([f"## {item['segment_id']}", "", item["zh"], ""])
    (TRANS / f"{PREFIXES[chapter]}_en_ocr.md").write_text("\n".join(en), encoding="utf-8")
    (TRANS / f"{PREFIXES[chapter]}_zh.md").write_text("\n".join(zh), encoding="utf-8")
    (TRANS / f"{PREFIXES[chapter]}_draft.json").write_text(
        json.dumps(selected, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"chapter {chapter}: {len(selected)} segments", flush=True)
