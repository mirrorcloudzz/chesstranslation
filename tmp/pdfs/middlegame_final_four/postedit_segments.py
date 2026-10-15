import json
import re
from pathlib import Path


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess")
TMP = Path(__file__).resolve().parent
TRANS = ROOT / "translations" / "chess_middlegame_planning"

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

MANUAL_ZH = {
    "CH5-3": "由此我们已经认识到，兵的作用绝不只是施加局面压力、控制某种颜色的格，或为子力提供便利的据点；兵本身也是强大的进攻手段。子力发起的进攻若得不到兵的积极支援，往往会撞上敌兵构成的防御屏障而归于失败。因此，兵在进攻中的主要任务之一，就是清除计划攻击区域内对手的防御兵线。如果兵的攻击针对易位后的王翼阵地，它往往会对暴露的王直接形成将杀威胁。",
    "CH5-6": "应当指出，只有在楔入兵两侧相邻的对方兵仍停留在原始格c7或e7（对黑方而言为c2或e2）时，e4-d5-c4（黑方为e5-d4-c5）兵形才称为兵楔。这种兵楔动态潜力更强——白方可冲起c4-c5或e4-e5，黑方相应可走...c5-c4或...e5-e4——但也不那么稳固，因为对方可能用以下冲兵加以冲击：",
    "CH5-66": "黑方准备...e5，这完全符合兑象后的局面要求：这个兵所控制的正是中心黑格。另一项以...d5为核心的计划不够合乎逻辑，而且会妨碍黑方完成后翼出子。",
    "CH6-6": "例如，众所周知，拉斯克执白采用西班牙开局兑换变例（1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Bxc6），计划在4... dxc6之后利用残局中王翼多兵的优势。他在对雅诺夫斯基和塔拉什的对抗赛中成功执行了这一计划。不过，在1896年纽伦堡国际大赛上，他用同一变例甚至在进入残局之前就击败了塔拉什。更鲜明的例子是1914年彼得堡的拉斯克对卡帕布兰卡一局。卡帕布兰卡熟悉拉斯克转入残局的计划，于是在兑换变例中封锁e兵，准备用e线双车并由b7象支援来攻击它。战斗仍在中局展开，拉斯克毫不犹豫地冲起f5，使e4兵成为落后弱兵。在斗争的决定性时刻，他又弃掉这个兵，让马侵入第六横线、双车叠入第七横线，彻底击溃了这位强劲的对手。拉斯克在构思进攻时，对自己的前景作出了细致而深入的判断，完全没有受可能转入残局这一因素的束缚。",
    "CH6-56": "44. Kg3 Qg1+，黑方胜。不过，拉斯克急于攫取子力，尤其是因为当时看不出王会立即遭遇危险。",
    "CH6-177": "拒绝兑换是否正确，并不容易判断。黑方无疑有理由设法利用白王暴露的位置；但另一方面，他也必须承受艰难防守所带来的紧张，因为黑王的位置同样并非毫无危险。",
    "CH7-2": "在国际象棋著作与评注中，我们经常遇到“调动”一词。按照已故特级大师塔塔科维的用法，有时人们会用它替代“迂回”这一概念，尽管从语义上说，两者并不相同。",
    "CH7-3": "“调动”一词源自德语manöver，意为“运子”。",
    "CH7-4": "不过，不应混淆“运子”和“调动”两个概念。运子，是同一枚棋子连续走数步，通常带有某种具体目标；调动，则是不同棋子一系列运子的组合，持续时间较长，而且很少具有清晰明确的目标。",
    "CH7-246": "白方本可不封闭局面并自动转入调动，而是在中心采取积极的进攻计划：11. d4，随后走Be3、Rad1和f4。黑方很难接受11... 后的弃兵。",
    "CH8-3": "开放线上的车和象、占据弱格的马——这些因素都会增强子力的活性。铁马的威力往往很大，通常足以让对手即使多半子也难以发挥优势。业余棋手总爱问马和象谁更强，标准答案是：在某种局面中象更强，在另一种局面中马更强。这取决于棋盘上的兵力配置、兵形，以及力量相近的棋子首先占据了哪些位置；当然，其他棋子的位置也同样必须纳入考虑。",
}

MANUAL_EN = {
    "CH7-3": "Manoeuvering is a term coming from the German word manöver, which means manoeuvre.",
    "CH7-4": "However, one should not mix up the concepts of 'manoeuvre' and 'manoeuvering'. A manoeuvre is several moves of one piece, usually made with some concrete aim. Manoeuvering is a series of manoeuvres with different pieces, bearing a more or less prolonged character and rarely having a clearly outlined aim.",
}


def notation(text):
    text = text.replace("0-0-0", "O-O-O").replace("0-0", "O-O")
    text = re.sub(r"\b([01]):([01])\b", r"\1-\2", text)
    text = re.sub(r"\b(\d{1,2})\s*[。\.]{2,3}\s*", r"\1... ", text)
    text = re.sub(
        r"(?<![\d.])(\d{1,2})\s+((?:O-O-O|O-O|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*))",
        r"\1. \2", text,
    )
    text = re.sub(r"(?:。){2,}|…{2,}", "...", text)
    text = re.sub(r"\.{4,}", "...", text)
    return re.sub(r"\s+", " ", text).strip()


def common_zh(text, source):
    replacements = {
        "白方格": "白格", "黑方格": "黑格", "白方方块": "白格", "黑方方块": "黑格",
        "方格": "格", "王位": "王的位置", "王位置": "王的位置", "典当": "兵",
        "“永恒”马": "铁马", "永恒马": "铁马", "开幕阶段": "开局阶段",
        "在董事会": "在棋盘上", "板上的": "棋盘上的", "交换后后": "兑后之后",
        "一张通兵": "一个通兵", "兵弃子": "弃兵", "相反颜色的象": "异格象",
        "开放线路": "开放线", "第六个横线": "第六横线", "第七个横线": "第七横线",
        "额外的交换": "多半子", "白方王的空位": "白王暴露的位置",
        "职位的评估": "局面的评估", "位置的评估": "局面的评估",
        "怀特": "白方", "布莱克": "黑方", "白e-兵": "白方e兵", "黑e-兵": "黑方e兵",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    pawn_advance = "advance" in source.lower() and re.search(r"pawn|phalanx|\b[a-h][1-8]\b", source, re.I)
    if pawn_advance:
        text = text.replace("f-兵推进到f5", "冲起f5")
        text = text.replace("f4报复性推进", "冲起f4反击")
        text = text.replace("e-兵的积极推进", "积极冲起e兵")
        text = text.replace("白方e兵的推进", "冲起白方e兵")
        text = text.replace("兵小组的推进", "兵群前冲")
        text = text.replace("方阵进一步推进", "兵阵再次前冲")
        text = text.replace("方阵的推进", "兵阵向前冲击")
        text = text.replace("推进e-f方阵", "推动e、f兵阵前冲")
        text = text.replace("推进 f-兵", "冲起f兵")
    return notation(text)


segments = json.loads((TMP / "translated_segments.json").read_text(encoding="utf-8"))
for item in segments:
    item["text"] = notation(MANUAL_EN.get(item["segment_id"], item["text"]))
    item["zh"] = MANUAL_ZH.get(item["segment_id"], common_zh(item["zh"], item["text"]))
    item["zh"] = notation(item["zh"])

(TMP / "reviewed_segments.json").write_text(
    json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8"
)

for chapter in range(5, 9):
    selected = [x for x in segments if x["chapter"] == chapter]
    en = [f"# {TITLES[chapter]}（英文 OCR 校对稿）", ""]
    zh = [f"# {TITLES[chapter]}（中文初译）", ""]
    for item in selected:
        en.extend([f"## {item['segment_id']}", "", item["text"], ""])
        zh.extend([f"## {item['segment_id']}", "", item["zh"], ""])
    (TRANS / f"{PREFIXES[chapter]}_en_ocr.md").write_text("\n".join(en), encoding="utf-8")
    (TRANS / f"{PREFIXES[chapter]}_zh.md").write_text("\n".join(zh), encoding="utf-8")
    (TRANS / f"{PREFIXES[chapter]}_reviewed.json").write_text(
        json.dumps(selected, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"chapter {chapter}: {len(selected)} segments")
