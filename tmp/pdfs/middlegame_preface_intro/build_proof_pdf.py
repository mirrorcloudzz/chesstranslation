from html import escape
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess")
WORK = ROOT / "tmp" / "pdfs" / "middlegame_preface_intro"
OUTPUT = ROOT / "output" / "pdf" / "chess_middlegame_planning_preface_introduction_zh_proof_v3.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Deng", r"C:\Windows\Fonts\Deng.ttf"))
pdfmetrics.registerFont(TTFont("DengBold", r"C:\Windows\Fonts\Dengb.ttf"))

NAVY = colors.HexColor("#15324A")
TEAL = colors.HexColor("#28756B")
PALE = colors.HexColor("#F2F6F5")
PALE_BLUE = colors.HexColor("#EFF4F8")
MID = colors.HexColor("#B9C7CF")
TEXT = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#5B6770")

styles = getSampleStyleSheet()
cover_title = ParagraphStyle(
    "CoverTitle",
    parent=styles["Title"],
    fontName="DengBold",
    fontSize=26,
    leading=36,
    textColor=NAVY,
    alignment=TA_CENTER,
    spaceAfter=14,
    wordWrap="CJK",
)
cover_subtitle = ParagraphStyle(
    "CoverSubtitle",
    parent=styles["Normal"],
    fontName="Deng",
    fontSize=14,
    leading=22,
    textColor=TEAL,
    alignment=TA_CENTER,
    wordWrap="CJK",
)
section_title = ParagraphStyle(
    "SectionTitle",
    parent=styles["Heading1"],
    fontName="DengBold",
    fontSize=18,
    leading=24,
    textColor=NAVY,
    spaceBefore=2,
    spaceAfter=10,
    wordWrap="CJK",
)
section_note = ParagraphStyle(
    "SectionNote",
    parent=styles["Normal"],
    fontName="Deng",
    fontSize=9,
    leading=14,
    textColor=MUTED,
    spaceAfter=10,
    wordWrap="CJK",
)
table_head = ParagraphStyle(
    "TableHead",
    parent=styles["Normal"],
    fontName="DengBold",
    fontSize=10,
    leading=14,
    textColor=colors.white,
    alignment=TA_CENTER,
    wordWrap="CJK",
)
eng_style = ParagraphStyle(
    "English",
    parent=styles["BodyText"],
    fontName="Times-Roman",
    fontSize=8.8,
    leading=12.4,
    textColor=TEXT,
    alignment=TA_LEFT,
    spaceAfter=0,
)
zh_style = ParagraphStyle(
    "Chinese",
    parent=styles["BodyText"],
    fontName="Deng",
    fontSize=9.6,
    leading=15.2,
    textColor=TEXT,
    alignment=TA_LEFT,
    wordWrap="CJK",
    spaceAfter=0,
)
label_style = ParagraphStyle(
    "Label",
    parent=styles["Normal"],
    fontName="DengBold",
    fontSize=8,
    leading=10,
    textColor=TEAL,
    wordWrap="CJK",
)
info_style = ParagraphStyle(
    "Info",
    parent=styles["BodyText"],
    fontName="Deng",
    fontSize=10.2,
    leading=17,
    textColor=TEXT,
    wordWrap="CJK",
)
appendix_caption = ParagraphStyle(
    "AppendixCaption",
    parent=styles["Normal"],
    fontName="DengBold",
    fontSize=11,
    leading=15,
    textColor=NAVY,
    alignment=TA_CENTER,
    spaceAfter=8,
    wordWrap="CJK",
)


PREFACE = [
    (
        "PF-1",
        "In the prolific world of chess literature, books on the middlegame are comparatively rare - and those on planning even rarer. When the author happens to be a Soviet champion and honoured trainer, then the publication of such a work as Chess Middlegame Planning arouses even greater interest. Peter Romanovsky (1892-1964) served his chess apprenticeship in pre-Revolutionary Russia during the same period as his personal friend Alexander Alekhine, to whom he was runner-up in the very first Soviet championship of 1920. After Alekhine's subsequent defection to the West, Romanovsky himself twice won the Soviet title and achieved fine results ahead of famous grandmasters in the few international tournaments which were held in the USSR during the 20s and 30s. He also became closely acquainted with those other great world champions, Lasker and Capablanca, who both spent a fair amount of time in Russia.",
        "在浩如烟海的国际象棋文献中，论述中局的著作相对少见，专门讨论计划的则更为罕见。如果作者恰好又是一位苏联冠军和功勋教练，那么《国际象棋中局计划》这样的作品问世，自然会引起更大的兴趣。彼得·罗曼诺夫斯基（1892-1964）在十月革命前的俄国接受了棋艺磨炼，与他处于同一时期的还有其私交甚笃的亚历山大·阿廖欣；在1920年首届苏联锦标赛中，他位居阿廖欣之后，获得亚军。阿廖欣后来出走西方，罗曼诺夫斯基本人则两度夺得苏联冠军，并在20世纪20年代和30年代苏联举办的为数不多的国际比赛中取得佳绩，名次超过多位著名特级大师。他还与另外两位伟大的世界冠军拉斯克和卡帕布兰卡相熟；两人都曾在俄国居住过相当长的时间。",
    ),
    (
        "PF-2",
        "After the Second World War, Romanovsky retired from competitive play and assumed a major role as a trainer, writer and populariser of chess. He lectured on the game from 1947-57 at Moscow University, was on the editorial board of the official Chess in the USSR magazine from its inception, and wrote 16 books. After his death, many unpublished manuscripts were discovered amongst his archives - regrettably most of these treasures still remain unpublished to this day.",
        "第二次世界大战后，罗曼诺夫斯基退出竞技赛场，转而在国际象棋教练、作家和普及者的岗位上发挥重要作用。1947年至1957年，他在莫斯科大学讲授国际象棋；从官方杂志《苏联国际象棋》创刊之日起，他便担任该刊编委；此外，他还撰写了16部著作。他去世后，人们在其档案中发现了许多未刊手稿。令人遗憾的是，这些珍贵文稿中的大部分至今仍未出版。",
    ),
    (
        "PF-3",
        "A cultured man with varied interests, in particular music and literature, he smiled when once asked why he did not put more effort into becoming a grandmaster - \"Oh, because in life there are many attractions which I did not want to pass by....\"",
        "他学养深厚，兴趣广泛，尤其喜爱音乐和文学。有人曾问他，为何不投入更多精力去成为特级大师。他笑着答道：\"哦，因为生活中有许多吸引人的事物，我不愿与它们擦肩而过……\"",
    ),
    (
        "PF-4",
        "In the Soviet School of Chess, Kotov and Yudovich write \"Romanovsky is an artist and seeker. He strives, in his games, to prove or refute one or another strategic idea, to create interesting and beautiful combinations. His Middlegame is one of the best books in the world's chess literature; it has served as a guide for many Soviet masters .... By his day-to-day penetrating analyses of his own games and the games of others, in which he seeks out unnoticed possibilities, Romanovsky sets the youth an example of how to work on self-improvement. He teaches young players not only the fine points of modern technique but the evolution of chess ideas and the history of the game.\"",
        "科托夫和尤多维奇在《苏联国际象棋学派》中写道：\"罗曼诺夫斯基是一位艺术家，也是一位探索者。他努力在自己的对局中证实或驳倒某种战略思想，创造有趣而优美的战术组合。他的《中局》是世界国际象棋文献中最优秀的著作之一，曾经成为许多苏联大师的指南……他日复一日深入分析自己和他人的对局，从中寻找那些未被察觉的可能性，以此为年轻人树立了如何努力实现自我提高的榜样。他教给年轻棋手的，不只是现代技术的精微之处，还有国际象棋思想的演变和这项运动的历史。\"",
    ),
    (
        "PF-5",
        "Chess Middlegame Planning was published in Moscow 1960. Its originality and practical value, allied to a colourful literary style, made it an immediate classic. It is now offered to readers for the first time in the English language.\n\nJimmy Adams\nLondon 1990",
        "《国际象棋中局计划》于1960年在莫斯科出版。它构思新颖、实用价值突出，再加上生动多彩的文学风格，一经问世便成为经典。如今，本书首次以英文呈献给读者。\n\n吉米·亚当斯\n伦敦，1990年",
    ),
]

INTRODUCTION = [
    (
        "IN-1",
        "The central stage of the chess game is called the middlegame. It is characterised by a comparatively large number of active forces of both fighting sides. Also characteristic for this segment of the chess game is the passive position of the king and the emergence of continuous threats in that area of the struggle where it is placed. The consistently arising threats, associated with a single idea, represent an attack, of which the object in the middlegame frequently becomes the king's position. The middlegame is thereby distinguished from the endgame, where a comparatively small number of forces are operating, where an attack on the king is rare, where, finally, the king assumes an active role. It is precisely this abrupt contrast in the role of the king which is the main sign distinguishing the endgame stage from the middlegame.",
        "棋局的中间阶段称为中局。其特征是交战双方都有相当数量的子力积极投入战斗。这个阶段的另一个特点，是王通常处于被动地位，而王所在的区域会不断出现威胁。一次进攻，就是围绕同一构想连续制造威胁；在中局，进攻的目标往往正是王的阵地。中局由此区别于残局：残局中参与行动的子力相对较少，对王的进攻并不常见，而且王最终会转而发挥积极作用。王的作用发生这种鲜明而突然的变化，正是区分残局阶段与中局阶段的主要标志。",
    ),
    (
        "IN-2",
        "It goes without saying that the scantiness of forces operating in the endgame will appreciably narrow the range of creative ideas, the diversity of which, on the other hand, forms the distinguishing feature of the middlegame. The theory of many endings bears a finished character, and a knowledge of technique, that is the application of theoretical laws and principles in practice, naturally is sharply increased in the endgame. The middlegame struggle most fully and vividly reflects the creative substance of chess art. The most important creative factor of the chess struggle - the combination - is displayed chiefly in the central stage. In the middlegame, there is the strongest stimulation for imagination and creative thought by a chessplayer, and the most distinct expression both of purely human traits of his nature (temperament, boldness, inventiveness etc.) and features of his chess style, creative outlook and the ideological tendency to which he belongs. It is no coincidence that middlegame material, if looked at in a historical connection, allows us to very clearly trace the evolution of chess ideas.",
        "不言而喻，残局中参与行动的子力较少，这会明显限制创造性构想的范围；而构想的丰富多样，恰恰构成中局的显著特征。许多残局理论已经相当完备；在残局中，对技术的掌握，也就是在实战中运用理论规律和原则的能力，其重要性自然大为提高。中局斗争最充分、最生动地体现了国际象棋艺术的创造性本质。国际象棋斗争中最重要的创造性因素 - 战术组合 - 主要展现在中局阶段。中局最能激发棋手的想象力和创造性思维，也最鲜明地展现他的个人天性，例如气质、勇气和创造才能等，以及他的棋风、创作观念和所属的思想流派。从历史脉络考察中局素材，可以十分清楚地追踪国际象棋思想的演变，这绝非偶然。",
    ),
    (
        "IN-3",
        "Besides the middlegame and the endgame, there is also the opening - the initial stage of the game, the theory of which discusses the question of the expedient development of pieces. At the beginning of the opening stage, within the first 3-5 moves, the maximum number of forces are operating and in the majority of cases they remain very numerous right up to the approach of the middlegame. In this respect, the characters of the game in the opening and central stage are close to one another. However there is one substantial difference: the opening ideas are concentrated around the full mobilisation of forces whereas in the middlegame the plan arises from the possibility of an operation by already mobilised pieces, which immeasurably broadens the creative horizon of ideas.",
        "除中局和残局之外，还有开局，也就是一盘棋的初始阶段；开局理论研究的是如何合理出子。在开局开始后的最初3至5回合内，盘面上的子力数量最多；而且在大多数情况下，直到即将进入中局时，子力仍然十分众多。从这一点看，开局与中局阶段的棋局特征彼此接近。不过，两者之间存在一个实质性差别：开局构想集中于充分调动全部子力，而中局计划则产生于运用已经动员起来的子力展开行动的各种可能性，这使创造性构想的视野得到极大的拓展。",
    ),
    (
        "IN-4",
        "Of course there must exist a very close connection between the opening and the middlegame. In the opening one should not simply develop the pieces, but place them in such a way that they are able to fulfil the role intended for them at the first stage of the central phase. In other words, the middlegame scheme must logically continue the opening line of play, blending with it into a single systematic plan of action.",
        "当然，开局与中局之间必然存在非常紧密的联系。在开局中，棋手不应只是出子，还应把子力部署到适当的位置，使其能够在中局第一阶段承担预定的任务。换言之，中局构想必须在逻辑上延续开局的行棋路线，并与之融为一个完整而系统的行动计划。",
    ),
]


def para_with_label(label, text, style):
    body = escape(text).replace("\n", "<br/>")
    return Paragraph(f'<font name="DengBold" color="#28756B">{label}</font><br/>{body}', style)


def bilingual_table(rows):
    data = [
        [
            Paragraph("经校正的英文 OCR", table_head),
            Paragraph("中文译文", table_head),
        ]
    ]
    for label, english, chinese in rows:
        data.append(
            [
                para_with_label(label, english, eng_style),
                para_with_label(label, chinese, zh_style),
            ]
        )
    table = Table(data, colWidths=[86 * mm, 98 * mm], repeatRows=1, hAlign="CENTER")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BOX", (0, 0), (-1, -1), 0.7, MID),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, MID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
    ]
    for row_index in range(1, len(data)):
        style.append(
            (
                "BACKGROUND",
                (0, row_index),
                (-1, row_index),
                colors.white if row_index % 2 else PALE,
            )
        )
    table.setStyle(TableStyle(style))
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(MID)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, A4[1] - 14 * mm, A4[0] - 18 * mm, A4[1] - 14 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Deng", 8)
        canvas.drawString(18 * mm, A4[1] - 11 * mm, "《国际象棋中局计划》｜英译者序与导言｜校对稿")
    canvas.setFillColor(MUTED)
    canvas.setFont("Deng", 8)
    canvas.drawCentredString(A4[0] / 2, 10 * mm, str(doc.page))
    canvas.restoreState()


def source_image(path, max_width=170 * mm, max_height=210 * mm):
    with PILImage.open(path) as image:
        width, height = image.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


crop_path = WORK / "source-08-introduction-only.png"
with PILImage.open(WORK / "source-08.png") as image:
    image.crop((0, 0, image.width, 1550)).save(crop_path)

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=13 * mm,
    leftMargin=13 * mm,
    topMargin=20 * mm,
    bottomMargin=17 * mm,
    title="Chess Middlegame Planning - Preface and Introduction - Chinese Proof",
    author="OCR and Chinese translation proof",
    subject="Corrected English OCR and Chinese translation for proofreading",
)

story = []
story.append(Spacer(1, 32 * mm))
story.append(Paragraph("《国际象棋中局计划》", cover_title))
story.append(Paragraph("英译者序与导言", cover_title))
story.append(Spacer(1, 5 * mm))
story.append(Paragraph("英文 OCR 校正稿 + 中文翻译校对稿", cover_subtitle))
story.append(Spacer(1, 16 * mm))

cover_info = [
    [Paragraph("文档性质", label_style), Paragraph("内部校对稿，非最终出版版本", info_style)],
    [Paragraph("内容范围", label_style), Paragraph("原书印刷页 4-6；第 6 页仅收录 Planning 标题以前的导言结尾", info_style)],
    [Paragraph("对照方式", label_style), Paragraph("左栏为经扫描原页校正的英文 OCR，右栏为中文译文；段落编号一一对应", info_style)],
    [Paragraph("处理原则", label_style), Paragraph("仅合并原扫描中的断行与行末断词，不改写英文原文；中文以准确、通顺和国际象棋术语一致为目标", info_style)],
    [Paragraph("版本日期", label_style), Paragraph("2026-09-23", info_style)],
]
info_table = Table(cover_info, colWidths=[30 * mm, 125 * mm], hAlign="CENTER")
info_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
            ("BOX", (0, 0), (-1, -1), 0.7, MID),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, MID),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]
    )
)
story.append(info_table)
story.append(Spacer(1, 13 * mm))
story.append(
    Paragraph(
        "建议重点核对：人名与书名译法；combination 译为“战术组合”；central stage 按语境译为“中局阶段”；以及英译原文本身较生硬处的中文处理。",
        section_note,
    )
)
story.append(PageBreak())

story.append(Paragraph("一、英译者序（Translator's Preface）", section_title))
story.append(
    Paragraph(
        "原书印刷页 4。标题加“英译”二字，是为了避免与未来中文译者序混淆；英文 OCR 保留原题。",
        section_note,
    )
)
story.append(bilingual_table(PREFACE))
story.append(PageBreak())

story.append(Paragraph("二、导言（Introduction）", section_title))
story.append(
    Paragraph(
        "原书印刷页 5 至第 6 页上半部；止于 Planning 标题之前。",
        section_note,
    )
)
story.append(bilingual_table(INTRODUCTION))
story.append(PageBreak())

story.append(Paragraph("附录：原扫描页", section_title))
story.append(
    Paragraph(
        "以下图像仅用于本次 OCR 与译文校对。第三幅已裁去 Planning 及其后续正文。",
        section_note,
    )
)
story.append(Paragraph("原书印刷页 4：Translator's Preface", appendix_caption))
story.append(source_image(WORK / "source-06.png"))
story.append(PageBreak())
story.append(Paragraph("原书印刷页 5：Introduction", appendix_caption))
story.append(source_image(WORK / "source-07.png"))
story.append(PageBreak())
story.append(Paragraph("原书印刷页 6 上半部：Introduction 结尾", appendix_caption))
story.append(source_image(crop_path, max_height=105 * mm))

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
