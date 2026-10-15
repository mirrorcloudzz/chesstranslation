import json
import re
from pathlib import Path


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess")
TMP = ROOT / "tmp" / "pdfs" / "middlegame_chapters34"
TRANS = ROOT / "translations" / "chess_middlegame_planning"

segments = json.loads((TMP / "translated_segments_final.json").read_text(encoding="utf-8"))

OVERRIDES = {
    "We have chosen as the basic theme the question of planning play along the a-file, when it occurs with castling king's side by both opponents. Namely these cases of play along the a-file assume a specific character, requiring an independent examination.":
        "我们选取双方均已短易位时围绕a线展开的计划性行棋作为基本主题。这类a线行动具有鲜明特点，值得单独研究。",
    "What features characterise play along the a-file, with king's side castling by both sides? Firstly, the a-file is as distant as can be from the king's flank, as a result of which the principal events, for the time being, do ) not affecthe castled positions. Even more important is the fact thathe side holding the initiative in play on the a-file must concentrate largescale forces, and in any case the rooks, on that file or near it. It means that such play is attended by the diversion of important pieces from the king's flank. But this could 1 prompthe opponent to direct his forces to an attack there, in the event of which it is very important to take care of the defence of the king's flank with a solid pawn chain and a minor piece covering C detachment.":
        "双方均在王翼易位时，a线行动具有哪些特点？首先，a线与王翼相距甚远，所以主要战事暂时不会直接影响易位后的王城。更重要的是，掌握a线主动权的一方必须在该线及其附近集中大量兵力，尤其是双车。这意味着重要棋子会被调离王翼，从而可能促使对手转而进攻王翼。因此，必须以稳固兵链和少量轻子妥善守护王翼。\n\n译注：从残局的观点来看，由于a线距离王城非常远，而轻子对于通路兵，尤其是边线通路兵的防守能力较弱，如果在此处的战斗发生大量重子兑换，后翼一旦出现通路兵将是决定性的。在围绕a线斗争的过程中执行兑换或者兵的突破时，必须时刻考虑到这一点。",
    "The technique of opening the a-file consists of the exchange of the a-pawn for the b-pawn. Such an exchange is difficult to achieve if the b-pawn stands on its original square. Therefore it is useful, as a pre-requisite to opening the a-file, to provoke the advance of the knight's pawn one or two squares. There is no need to mention thathe plan of opening the a-file and the future invasion on it must be carefully thought out, taking into account all the concrete positional conditions, to weigh up whether it is possible for the opponent to advantageously preventhe opening of the a-file or launch a successful counter-attack on the king's flank.":
        "打开a线的基本方法，是以a兵交换对方的b兵。如果b兵仍在初始格，这种交换便难以实现。因此，打开a线之前往往要先诱使对方的马前兵冲起一格或两格。显然，打开a线并随后沿线侵入的计划必须经过周密考虑：既要结合局面的具体条件，也要判断对手能否有利地阻止开线，或在王翼发动有效反击。",
    "In planning play on the a-file, it is of course necessary to secure the occupation of the opened line with his rooks. It means that an appropriate regrouping g of forces must take place even before the opening of the line.":
        "规划a线行动时，当然必须确保开线后能够以双车占据该线。这意味着适当的子力重组必须在a线打开之前便已完成。",
    "As an excellent example of the technique of invasion on the a-file might serve the ending of the game Marco-Muller, played as long ago as the end of the last century (1898) in the accessory tournament of the international congress in London.":
        "早在上世纪末的伦敦国际象棋大会附属赛（1898年）中，马尔科—穆勒一局的收尾便出色展示了沿a线侵入的技术。",
    "White has prepared the opening and occupation of the a-file.":
        "白方已经为打开并占据a线做好准备。",
    "The part of the board which includes the squares e4, d4, e5 and d5 is called the centre. These squares are called central.":
        "棋盘上由e4、d4、e5、d5四格构成的区域称为中心，这四个格子称为中心格。",
    "The arrangement of the pieces in the centre, from where they operate e in several directions, might serve as a basis for the construction of very active plans. Many different ideas and combinations have been carried out on this basis.":
        "棋子配置在中心后可以向多个方向发挥作用，这可成为制定积极计划的基础。许多不同的构想与组合都建立在这一基础上。",
    "Athe end of the last century the famous American chessplayer, Pillsbury, was able to win a number of interesting games where the basis of the initiative was the planting of a knight on e5. In the 20's and 30's of our century, a plan, where the whole object was the occupation of the d5 square (for Black - d4) with the knight, became increasingly pronounced. The centralised knight, supported by pawns, hampered the activity of the opponent, guaranteed a lasting initiative and frequently broughthe champions of such ideas success.":
        "十九世纪末，美国名将皮尔斯伯里赢下了多盘精彩对局；他取得主动的基础，正是把马安置在e5。到了二十世纪二三十年代，以马占据d5（黑方则为d4）为全部目标的计划愈发常见。得到兵支持的中心马能够限制对手棋子的活动，保证持久的主动权，并屡屡为这一构想的拥护者带来成功。",
    "We return, in the first instance, to Pillsbury's idea, introduced into international practice athe 1895 Hastings tournament in games Significance against Tarrasch and Schlechter. These proceeded identically up to the 11th move:":
        "我们先回到皮尔斯伯里的构想。1895年黑斯廷斯大赛上，他在对塔拉什和施莱希特的两盘棋中把这一构想带入国际赛场；两盘棋直到第11步都完全相同：",
    "The so-called Orthodox variation of the Queen's Gambit. This variation is also met in our day and consequently continues to be developed, buthe proportion of games with it, in comparison with the end of the 19th and the first two decades of the 20th century, was reduced owing to the opening systems which arose on the basis of the reply 1... Nf6. The fact should also be taken into account that methods of play have considerably improved for Black, and White does not succeed in easily obtaining a positional superiority as happened in Pillsbury's time.":
        "这是所谓的后翼弃兵正统变化。今天仍能见到这一变化，理论也在继续发展；不过，与十九世纪末和二十世纪最初二十年相比，其采用比例已经下降，因为以1... Nf6为基础的开局体系相继出现。此外，黑方的应对方法已经大为改进，白方不再能像皮尔斯伯里时代那样轻易取得局面优势。",
    "This was nearly always played in the old days. In itself, the plan with the development t of the bishop on b7 looks quite logical and does not arouse any objections on principle. But a principal - is a principal and concreteness - is concreteness. Pillsbury was the first to have doubts abouthe then generally accepted method of play for Black. In the course of time, more and more the shady side of the move... b6 followed by... Bb7 was revealed, and now there is a decided preference for 7... c6 with the aim of preparing an invasion of the Black knight on e4. (7... Ne4 at once is not possible, in view of 8":
        "过去这里几乎总是这样走。就其本身而言，先把象出到b7的计划看起来十分合乎逻辑，在原则上也无可非议。但原则归原则，具体局面归具体局面。皮尔斯伯里最先对当时公认的黑方下法产生怀疑。随着实践积累，...b6继而...Bb7的缺点逐渐显露出来；如今人们明显更倾向于7... c6，以准备黑马侵入e4。（7... Ne4不能立即走，因为8.",
    "Bxe7 Qxe7 9. cxd5 Nxc3 10. Rxc3 exd5 11. Rxc7.) Besides this, 7... c6 allows him, in the event of 8. Bd3, to bring about a favourable relaxation of tension in the centre by 8... dxc4 9. Bxc4 Nd5. Practice has shown that in this way Black succeeds in overcoming the difficulties with the development of his queen's flank. 8. cxd5 exd5 9. Bd3 Bb7 10. O-O c5":
        "Bxe7 Qxe7 9. cxd5 Nxc3 10. Rxc3 exd5 11. Rxc7。）此外，若白方走8. Bd3，7... c6还允许黑方以8... dxc4 9. Bxc4 Nd5有利地缓和中心的紧张。实践证明，黑方可以用这种方法克服后翼出子的困难。8. cxd5 exd5 9. Bd3 Bb7 10. O-O c5",
    "As distinct from the game with Tarrasch, where Pillsbury lost a tempo - 11. Re1, allowing Black to take over the initiative after 11...":
        "在对塔拉什的一局中，皮尔斯伯里以11. Re1浪费了一个先手，让黑方在11...",
    "c4 12. Bb1 a6 13. Ne5 b5 14. f4 Re8 15. Qf3 Nf8 16. Ne2? Ne4!, against Schlechter he continued 11. Bb1 Ne4 12. Bf4 Nxc3 13. Rxc3 c4 14. Ne5":
        "c4 12. Bb1 a6 13. Ne5 b5 14. f4 Re8 15. Qf3 Nf8 16. Ne2? Ne4!之后被黑方夺得主动。与此不同，在对施莱希特的一局中，他续走11. Bb1 Ne4 12. Bf4 Nxc3 13. Rxc3 c4 14. Ne5。",
}

EXACT = {
    "Queen's Gambit": "后翼弃兵",
    "English h Opening": "英格兰开局",
    "Sicilian Defence": "西西里防御",
    "the set-ups of the Sicilian Defence": "西西里防御的阵形",
    "Reti Opening": "列蒂开局",
    "Blumenfeld Gambit": "布卢门菲尔德弃兵",
    "King's Indian Defence": "老印度防御",
    "Queen's Pawn Opening": "后兵开局",
    "Four Knights Game": "四马开局",
    "Nimzo-Indian Defence": "尼姆佐维奇防御",
    "Queen's Indian Defence": "后印度防御",
}

PREFIX_OVERRIDES = {
    "Bxe7 Qxe7 9 cxd5":
        "Bxe7 Qxe7 9. cxd5 Nxc3 10. Rxc3 exd5 11. Rxc7。）此外，若白方走8. Bd3，7... c6还允许黑方以8... dxc4 9. Bxc4 Nd5有利地缓和中心的紧张。实践证明，黑方可以用这种方法克服后翼出子的困难。8. cxd5 exd5 9. Bd3 Bb7 10. O-O c5",
    "As distinct from the game with Tarrasch":
        "在对塔拉什的一局中，皮尔斯伯里以11. Re1浪费了一个先手，让黑方在11...",
    "c4 12. Bb1 a6 13. Ne5 b5":
        "c4 12. Bb1 a6 13. Ne5 b5 14. f4 Re8 15. Qf3 Nf8 16. Ne2? Ne4!之后被黑方夺得主动。与此不同，在对施莱希特的一局中，他续走11. Bb1 Ne4 12. Bf4 Nxc3 13. Rxc3 c4 14. Ne5。",
}

NAME_REPLACEMENTS = {
    "R.Charousek": "R.恰鲁塞克", "S.Alapin": "S.阿拉平",
    "E.Schiffers": "E.希弗斯", "V.Kirillov": "V.基里洛夫",
    "G.Lisitsin": "G.利西岑", "A.Lilienthal": "A.李林塔尔",
    "E.Geller": "E.盖勒", "V.Simagin": "V.西马金",
    "A.Alekhine": "A.阿廖欣", "A.Alekhin": "A.阿廖欣",
    "M.Taimanov": "M.泰马诺夫", "K.Bardeleben": "K.巴德莱本",
    "F.Dus Chotimirsky": "F.杜斯-霍季米尔斯基",
    "P.Romanovsky": "P.罗曼诺夫斯基", "O.Duras": "O.杜拉斯",
    "E.Zagorovsky": "E.扎戈罗夫斯基", "H.Kmoch": "H.克莫赫",
    "M.Euwe": "M.尤伟", "P.Evtifeev": "P.叶夫季费耶夫",
    "D.Danushevsky": "D.达努舍夫斯基", "M.Yudovich": "M.尤多维奇",
    "V.Alatortsev": "V.阿拉托尔采夫", "G.Maroczy": "G.马洛契",
    "M.Botvinnik": "M.鲍特维尼克", "G.Levenfish": "G.列文菲什",
}

REPLACEMENTS = {
    "怀特": "白方", "布莱克": "黑方", "肖沃尔特": "肖瓦尔特",
    "白：": "白方：", "黑：": "黑方：", "黑人：": "黑方：",
    "a字形": "a线", "A字形": "a线", "a-file": "a线", "A-file": "a线",
    "a 档": "a线", "a档": "a线", "a 列": "a线", "a列": "a线",
    "纵队": "线", "文件": "线", "档案": "线", "该列": "该线",
    "正方形": "格", "广场": "格", "方块": "格",
    "典当链": "兵链", "典当": "兵", "棋兵": "兵", "棋子中心": "兵中心",
    "b 棋子": "b兵", "e 棋子": "e兵", "d 棋子": "d兵",
    "马的棋子": "马前兵", "小棋子": "轻子", "重型棋子": "重子", "重棋": "重子",
    "王的侧翼": "王翼", "国王的侧翼": "王翼", "王一方": "王翼",
    "皇后侧翼": "后翼", "女王侧翼": "后翼",
    "女王": "后", "皇后": "后", "国王": "王", "骑士": "马", "主教": "象",
    "部件": "棋子", "球员": "棋手", "播放": "走", "玩": "走",
    "电子兵": "e兵", "电子典当": "e兵", "后移动": "动后",
    "开放系统": "开局体系", "开局的正统变体": "正统变化",
    "第七位": "第七横线", "第一和第二行": "第一横线和第二横线",
    "回归对局": "世界冠军回敬赛", "回敬赛": "世界冠军回敬赛",
    "牺牲的动机": "弃子的可能", "进一步计划": "后续计划",
    "位置优势": "局面优势", "位置弱点": "局面弱点",
    "步棋之后": "步之后", "棋步": "步", "与与 ": "与",
    "举动的阴暗面": "这步棋的缺点",
    "被演奏": "被采用", "进行演奏": "采用", "比赛方式": "行棋方式",
    "棋子的活动": "棋子的活动", "部队": "子力", "军队": "子力",
    "城堡位置": "易位后的王城", "城堡一侧": "易位一侧",
    "拿走棋子": "吃掉棋子", "抓住棋子": "吃掉棋子",
    "棋子的牺牲": "弃子", "牺牲棋子": "弃子",
    "不损失一个棋子": "不失兵", "损失一个棋子": "失子",
    "失去一个棋子": "失子", "赢得一个棋子": "得子", "赢得棋子": "得子",
    "牺牲一个棋子": "弃子", "重棋子": "重子", "吃掉a线棋子": "占据a线",
    "物质优势": "子力优势", "材料优势": "子力优势", "物质平衡": "子力平衡",
    "后翼发展的困难": "后翼出子的困难", "象在b7上的发展计划": "把象出到b7的计划",
    "为了不失兵，黑方被迫将车带离a8方格": "为了不丢兵，黑方被迫将a8车移开",
    "白方在第七横线翻倍": "白方在第七横线叠起重子",
    "方格": "格",
}


def normalize_notation(value: str) -> str:
    # Keep all prose and move notation in one font, but modernise the printed
    # notation: White's move number takes one dot and Black's takes three.
    value = re.sub(r"(?<![A-Za-z0-9.])(\d{1,3})\s*\.{2,}\s*(?=[KQRBNOa-h])", r"\1... ", value)
    value = re.sub(r"(?<![A-Za-z0-9.])(\d{1,3})\s+(?=[KQRBNOa-h][a-h1-8x=+#?!-]*)", r"\1. ", value)
    value = re.sub(r"(?<![A-Za-z0-9.])(\d{1,3})\.(?!\.)(?=[KQRBNOa-h])", r"\1. ", value)
    value = re.sub(r"\.{4,}", "……", value)
    return value


cleaned = []
skip = False
for index, item in enumerate(segments):
    if skip:
        skip = False
        continue
    item = dict(item)
    text = item["text"]
    if text == "Now an immediate capture on" and index + 1 < len(segments):
        following = segments[index + 1]
        if following["text"].startswith("b6 was also not bad."):
            item["text"] = text + " " + following["text"]
            item["page_end"] = following.get("page_end", following["page"])
            item["zh"] = "此时立即在b6交换也不坏。白方若走33. axb6 axb6 34. Qa1! Rxa4 35. Rxa4，便可掌握a线；结合b6兵和e6兵的弱点，这最终应当为白方带来胜利。不过，黑方以35... Rd7回应后仍可顽强防守。"
            skip = True
    if item["text"] in OVERRIDES:
        item["zh"] = OVERRIDES[item["text"]]
    if item["text"] in EXACT:
        item["zh"] = EXACT[item["text"]]
    for prefix, translated in PREFIX_OVERRIDES.items():
        if item["text"].startswith(prefix):
            item["zh"] = translated
            break
    for old, new in NAME_REPLACEMENTS.items():
        item["zh"] = item["zh"].replace(old, new)
    for old, new in REPLACEMENTS.items():
        item["zh"] = item["zh"].replace(old, new)
    item["text"] = normalize_notation(item["text"])
    item["zh"] = normalize_notation(item["zh"])
    item["zh"] = re.sub(r"\s+([，。；：！？）])", r"\1", item["zh"])
    item["zh"] = re.sub(r"（\s+", "（", item["zh"])
    item["zh"] = re.sub(r"[ \t\r\f\v]+", " ", item["zh"])
    item["zh"] = re.sub(r" *\n+ *", "\n\n", item["zh"]).strip()
    cleaned.append(item)

segments = cleaned
# The source-reviewed chapter supersedes the initial machine-translation pass.
# Keep reviewed content and stable legacy IDs when rebuilding downstream data.
reviewed_ch3 = TRANS / '13_chapter_three_reviewed.json'
if reviewed_ch3.exists():
    authoritative = json.loads(reviewed_ch3.read_text(encoding='utf-8'))
    segments = authoritative + [s for s in segments if not 89 <= s['page'] <= 100]
reviewed_ch4 = TRANS / '14_chapter_four_reviewed.json'
if reviewed_ch4.exists():
    authoritative = json.loads(reviewed_ch4.read_text(encoding='utf-8'))
    segments = [s for s in segments if not 101 <= s['page'] <= 144] + authoritative
(TMP / "translated_segments_clean.json").write_text(
    json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8"
)

for chapter, start, end, prefix, title in (
    (3, 89, 100, "13_chapter_three_a_file", "第三章：a线上的战斗"),
    (4, 101, 144, "14_chapter_four_centre", "第四章：中心及其战略意义"),
):
    selected = [item for item in segments if start <= item["page"] <= end]
    en_lines = [f"# {title}（英文 OCR 校对稿）", ""]
    status = '复核修订稿' if (chapter == 3 and reviewed_ch3.exists()) or (chapter == 4 and reviewed_ch4.exists()) else '中文初译'
    zh_lines = [f"# {title}（{status}）", ""]
    counter = 0
    for item in selected:
        if item["kind"] == "chapter":
            continue
        counter += 1
        segment_id = item.get('segment_id', f"CH{chapter}-{counter}")
        en_lines.extend([f"## {segment_id}", "", item["text"], ""])
        zh_lines.extend([f"## {segment_id}", "", item["zh"], ""])
    (TRANS / f"{prefix}_en_ocr.md").write_text("\n".join(en_lines), encoding="utf-8")
    (TRANS / f"{prefix}_zh.md").write_text("\n".join(zh_lines), encoding="utf-8")
    print(f"chapter{chapter}_segments={counter}")
