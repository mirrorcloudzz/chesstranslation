import json
import re
import sys
import time
from pathlib import Path

DEPS = Path(r"C:\Users\12059\Documents\Codex\chess\tmp\translation_deps")
sys.path.insert(0, str(DEPS))

from translatepy.translators.google import GoogleTranslate


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess")
TMP = ROOT / "tmp" / "pdfs" / "middlegame_chapters34"
TRANS = ROOT / "translations" / "chess_middlegame_planning"
translator = GoogleTranslate()

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

MOVE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:\d{1,2}\.(?:\.\.)?\s*)?"
    r"(?:O-O-O|O-O|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)"
    r"(?![A-Za-z0-9])"
)


def clean_notation(text):
    text = re.sub(
        r"([KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)\.\s+(?=[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8])",
        r"\1 ", text,
    )
    text = re.sub(r"(\d{1,2})\.\.\.\s+", r"\1... ", text)
    return text


def pure_moves(text):
    remainder = MOVE_PATTERN.sub(" ", text)
    remainder = re.sub(r"[\d\s.,;:()\-+/!?]+", " ", remainder)
    words = re.findall(r"[A-Za-z]{2,}", remainder)
    return len(words) <= 2 and all(word.lower() in {"etc", "or", "and"} for word in words)


def protect_moves(text):
    values = []
    def repl(match):
        key = f"M{len(values):04d}"
        values.append((key, match.group(0)))
        return f"[{key}]"
    return MOVE_PATTERN.sub(repl, text), values


def restore_moves(text, values):
    for key, value in values:
        text = re.sub(rf"\[\s*{key}\s*\]", lambda _: value, text, flags=re.I)
    return text


def polish(text):
    for old, new in NAME_MAP.items():
        text = re.sub(re.escape(old), new, text, flags=re.I)
    replacements = {
        "白棋": "白方", "黑棋": "黑方", "白色": "白方", "黑色": "黑方",
        "王后": "后", "皇后": "后", "国王": "王", "骑士": "马", "主教": "象",
        "兵卒": "兵", "棋兵": "兵", "重型棋子": "重子", "小子": "轻子",
        "物质优势": "子力优势", "物质损失": "子力损失", "物质收益": "子力收益",
        "棋子的发展": "出子", "发展棋子": "出子", "发展子力": "出子",
        "棋子的开发": "出子", "发展阶段": "出子阶段",
        "兵的推进": "冲兵", "兵推进": "冲兵", "推进兵": "冲兵",
        "交换牺牲": "弃半子", "牺牲交换": "弃半子", "牺牲一子": "弃子",
        "中间着法": "过渡着", "中间招法": "过渡着",
        "弱着": "一步软着", "弱招": "一步软着",
        "获得一个棋子": "得子", "赢得一个棋子": "得子", "丢失一个棋子": "失子",
        "赢得后": "得后", "夺回一兵": "吃回一兵", "收回一兵": "吃回一兵",
        "后续行动": "后续手段", "后续措施": "后续手段",
        "节奏": "先手", "逼入僵局": "逼和", "僵局": "逼和",
        "将死": "将杀", "三招杀": "三步杀", "三步将杀": "三步杀",
        "王的位置": "王的位置", "王位": "王的位置",
        "走棋动作": "行棋", "游戏": "对局", "比赛": "对局",
        "棋步": "步", "这着棋": "这步棋", "一着棋": "一步棋",
        "下一着": "下一步", "这着": "这步", "一着": "一步",
        "a-文件": "a线", "A-文件": "a线", "a 文件": "a线", "A 文件": "a线",
        "a档": "a线", "A档": "a线", "a列": "a线", "A列": "a线",
    }
    for letter in "abcdefgh":
        replacements[f"{letter}-pawn"] = f"{letter}兵"
        replacements[f"{letter} pawn"] = f"{letter}兵"
        replacements[f"{letter}-兵"] = f"{letter}兵"
        replacements[f"{letter}兵兵"] = f"{letter}兵"
        replacements[f"{letter} 档"] = f"{letter}线"
        replacements[f"{letter}档"] = f"{letter}线"
        replacements[f"{letter} 列"] = f"{letter}线"
        replacements[f"{letter}列"] = f"{letter}线"
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("后翼弃兵接受", "后翼弃兵接受变化")
    text = text.replace("国王翼", "王翼").replace("皇后翼", "后翼")
    text = text.replace("王侧翼", "王翼").replace("后侧翼", "后翼")
    text = re.sub(r"\s+([，。；：！？])", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def translate_batch(items, depth=0):
    payload = "\n".join(f"[S{index:04d}]\n{text}" for index, text in items)
    last_error = None
    for attempt in range(3):
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
            last_error = RuntimeError(f"missing segment markers: expected={len(items)} found={len(found)}")
        except Exception as exc:
            last_error = exc
        time.sleep(1.5 * (attempt + 1))
    if len(items) > 1:
        middle = len(items) // 2
        left = translate_batch(items[:middle], depth + 1)
        right = translate_batch(items[middle:], depth + 1)
        left.update(right)
        return left
    raise last_error


segments = json.loads((TMP / "translated_segments.json").read_text(encoding="utf-8"))
prepared = {}
pending = []

for index, item in enumerate(segments):
    item["text"] = clean_notation(item["text"])
    if item["text"] in MANUAL:
        item["zh"] = MANUAL[item["text"]]
        continue
    if pure_moves(item["text"]):
        item["zh"] = item["text"]
        continue
    protected, values = protect_moves(item["text"])
    prepared[index] = values
    pending.append((index, protected))

batches = []
current = []
current_size = 0
for item in pending:
    addition = len(item[1]) + 12
    if current and current_size + addition > 3900:
        batches.append(current)
        current, current_size = [], 0
    current.append(item)
    current_size += addition
if current:
    batches.append(current)

for batch_number, batch in enumerate(batches, 1):
    translations = translate_batch(batch)
    for index, _ in batch:
        restored = restore_moves(translations[index], prepared[index])
        segments[index]["zh"] = polish(restored)
    print(f"batch={batch_number}/{len(batches)} segments={len(batch)}", flush=True)
    time.sleep(0.4)

(TMP / "translated_segments_final.json").write_text(
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
