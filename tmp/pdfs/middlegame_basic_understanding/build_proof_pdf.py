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
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(str(Path(__file__).resolve().parents[3]))
WORK = ROOT / "tmp" / "pdfs" / "middlegame_basic_understanding"
OUTPUT = ROOT / "output" / "pdf" / "chess_middlegame_planning_basic_understanding_zh_proof_v4.pdf"
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
cover_title = ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="DengBold", fontSize=25, leading=35, textColor=NAVY, alignment=TA_CENTER, spaceAfter=12, wordWrap="CJK")
cover_subtitle = ParagraphStyle("CoverSubtitle", parent=styles["Normal"], fontName="Deng", fontSize=14, leading=22, textColor=TEAL, alignment=TA_CENTER, wordWrap="CJK")
section_title = ParagraphStyle("SectionTitle", parent=styles["Heading1"], fontName="DengBold", fontSize=18, leading=24, textColor=NAVY, spaceAfter=10, wordWrap="CJK")
section_note = ParagraphStyle("SectionNote", parent=styles["Normal"], fontName="Deng", fontSize=9, leading=14, textColor=MUTED, spaceAfter=10, wordWrap="CJK")
table_head = ParagraphStyle("TableHead", parent=styles["Normal"], fontName="DengBold", fontSize=10, leading=14, textColor=colors.white, alignment=TA_CENTER, wordWrap="CJK")
eng_style = ParagraphStyle("English", parent=styles["BodyText"], fontName="Times-Roman", fontSize=8.7, leading=12.2, textColor=TEXT, alignment=TA_LEFT)
zh_style = ParagraphStyle("Chinese", parent=styles["BodyText"], fontName="Deng", fontSize=9.5, leading=15.1, textColor=TEXT, alignment=TA_LEFT, wordWrap="CJK")
label_style = ParagraphStyle("Label", parent=styles["Normal"], fontName="DengBold", fontSize=8, leading=10, textColor=TEAL, wordWrap="CJK")
info_style = ParagraphStyle("Info", parent=styles["BodyText"], fontName="Deng", fontSize=10, leading=16.5, textColor=TEXT, wordWrap="CJK")
diagram_caption = ParagraphStyle("DiagramCaption", parent=styles["Normal"], fontName="DengBold", fontSize=10, leading=14, textColor=NAVY, alignment=TA_CENTER, spaceAfter=7, wordWrap="CJK")


ROWS = {
    "BU-1": (
        "One can, without exaggeration, say that the formation and carrying out of a plan of action is the main task in the course of the process of the chess struggle.",
        "毫不夸张地说，在国际象棋斗争过程中，制定并执行行动计划是主要任务。",
    ),
    "BU-2": (
        "A skilfully conceived and purposefully executed plan serves as a true token of success.",
        "构思精巧并有目的地贯彻执行的计划，是成功的可靠保证。",
    ),
    "BU-3": (
        "A skilfully conceived plan - first and foremost this means a correctly mapped out objective which the chessplayer must direct his thoughts towards achieving. This problem is far from simple, and many difficulties arise on the way to solving it. However, a correctly mapped out objective is only half the matter. It is not enough to contemplate a plan, it is also necessary to solve another, no less serious problem - to carry it out. Of course, it is necessary to look at ways of achieving the objective with an outline of the objective itself. And what is more, the choice of the objective to some extent must be determined by the possibility of achieving it. This possibility, however, has to be assessed in highly relative terms, since one chessplayer's striving for an objective will run across the will and intentions of the opponent. It might also happen that the counter-action of the opponent forces a change of plan and even a transfer to defence. And yet, despite the above-mentioned relativity, it is not possible to conduct a game without drawing up a plan and without directing one's operations in accordance with it.",
        "所谓构思精巧的计划，首先是指正确确定一个目标，棋手必须把自己的思考引向如何实现这一目标。要解决这个问题远非易事，途中会遇到许多困难。然而，正确确定目标只完成了事情的一半。仅仅设想一个计划并不够，还必须解决另一个同样重大的问题：把计划执行出来。当然，在勾勒目标本身的同时，就要考虑实现目标的途径。不仅如此，目标的选择在一定程度上还必须取决于实现它的可能性。不过，这种可能性必须从很强的相对性来衡量，因为一方棋手对某个目标的追求，会受到对手意志和意图的阻碍。对手的反击也可能迫使棋手改变计划，甚至转入防御。尽管存在上述相对性，没有计划，或不按计划指导自己的行动，就不可能把一盘棋下得有章法。",
    ),
    "BU-4": (
        "In order to give very simple examples of how to formulate an idea of a plan, we look at two elementary positions from the endgame.",
        "为了用非常简单的例子说明如何形成计划构想，我们来看两个基础残局局面。",
    ),
    "BU-5": (
        "White to move.\n\nHis position is better since he will easily win the h4 pawn. Is this sufficient for victory? Indeed, it is sufficient, but only if White correctly maps out an idea and a method of realising it. His plan ought to consist of the following:\n\n- the first stage consists of the win of the h4 pawn;\n- in the second stage, White makes his way with the king to the a6 pawn and, exploiting the fact that the enemy king will be diverted from the queen's flank by his own passed pawn on the h-file, also wins this pawn;\n- finally, he promotes the a-pawn into a queen and finishes off the opponent's lone king.",
        "白方走。\n\n白方局面较好，因为他可以轻易吃掉h4兵。但这足以取胜吗？确实足够，不过前提是白方正确确定构想，并找到实现它的方法。其计划应包括以下内容：\n\n- 第一阶段，吃掉h4兵；\n- 第二阶段，白王向a6兵靠近；同时利用黑王被白方自己的h线通路兵从后翼引开的机会，再吃掉这个兵；\n- 最后，使a线兵升变为后，将死对方的孤王。",
    ),
    "BU-6": (
        "And so: 1 Kf4\n\nThere are two possible plans of defence for Black:\n\n- one - to make his way with the king to the a5 pawn, capture it and try to queen his passed pawn on the a-file;\n- the other - to attack the White pawn on the king's flank at that moment when the king has set off for the queen's flank to the a6 pawn.",
        "因此：1. Kf4\n\n黑方有两种可能的防守计划：\n\n- 第一种，黑王向a5兵靠近，吃掉它，然后设法使自己的a线通路兵升变；\n- 第二种，等白王动身前往后翼吃a6兵时，攻击白方王翼的兵。",
    ),
    "BU-7": (
        "The first plan must be discarded at once, since a simple calculation shows that the White pawn reaches h8 far quicker (8 moves are necessary for this - Kg4, Kxh4, Kg5, and h4-h5-h6-h7-h8Q) than Black's does to a1 (this operation requires 10 moves - Kd5, Kc4, Kb5, Kxa5, Kb4 and five moves with the pawn). There remains the second plan.\n\n1 ... Kf6 2 Kg4 Kg6 3 Kxh4 Kh6 4 Kg4 Kg6 5 Kf4 Kh5 6 Ke4 Kh4 7 Kd5 Kxh3 8 Kc5 Kg4 9 Kb6 Kf5 10 Kxa6 Ke6 11 Kb7, and the unhindered pawn reaches the queening square.",
        "第一种计划必须立即排除，因为简单计算便可看出，白兵到达h8的速度远快于黑兵到达a1。白方需要8步：Kg4、Kxh4、Kg5，然后h4-h5-h6-h7-h8Q；黑方则需要10步：Kd5、Kc4、Kb5、Kxa5、Kb4，再走5步兵。于是只剩第二种计划。\n\n1... Kf6 2. Kg4 Kg6 3. Kxh4 Kh6 4. Kg4 Kg6 5. Kf4 Kh5 6. Ke4 Kh4 7. Kd5 Kxh3 8. Kc5 Kg4 9. Kb6 Kf5 10. Kxa6 Ke6 11. Kb7\n\n此后，这个不受阻挡的兵将到达升变格。",
    ),
    "BU-8": (
        "In this example, White's position looks even more favourable. He already has an extra passed pawn and the plan of play seems obvious: at the cost of the passed pawn, to penetrate with the king to g7 so as to do away with the h7 pawn. However, there is a well-known type of position from endgame theory in which the weaker side shadows the enemy king and achieves a draw. It turns out that the present position is one of these.",
        "在这个例子中，白方的局面看起来更为有利。他已经多了一个通路兵，行棋计划似乎显而易见：弃掉这个通路兵，让白王侵入g7，从而吃掉h7兵。然而，残局理论中有一种广为人知的局面类型：弱方的王紧跟对方的王，最终可以取得和棋。当前局面正属于这一类型。",
    ),
    "BU-9": (
        "1 e5 Ke7 2 Kd5 Kd7 3 e6+ Ke8 4 Ke5 Ke7\n\nBlack tries to prevent the king getting to f6, but White still has the possibility of achieving this.\n\n5 Kd5 Ke8 6 Kd4 Kd8 7 Ke4 Ke8 8 Kd5 Ke7\n\nIf 8 ... Kd8, then 9 Kd6 and the e-pawn goes on to queen.\n\n9 Ke5 Ke8 10 Kf6\n\nThe first stage of the plan - penetrating with the king to the f6 square - is completed.\n\n10 ... Kf8 11 e7+ Ke8 12 Kg7\n\nIt seems that also the second problem of the plan has been solved, but ...\n\n12 ... Kxe7 13 Kxh7 Kf7 14 Kh8 Kf8 15 h7 Kf7 stalemate.\n\nWhite did not achieve his objective thanks to fine resistance by Black, whose defence revealed an interesting drawing resource.",
        "1. e5 Ke7 2. Kd5 Kd7 3. e6+ Ke8 4. Ke5 Ke7\n\n黑方设法阻止白王到达f6，但白方仍有办法实现这一目标。\n\n5. Kd5 Ke8 6. Kd4 Kd8 7. Ke4 Ke8 8. Kd5 Ke7\n\n如果8... Kd8，那么9. Kd6，随后e兵升变。\n\n9. Ke5 Ke8 10. Kf6\n\n计划的第一阶段，也就是让王侵入f6格，已经完成。\n\n10... Kf8 11. e7+ Ke8 12. Kg7\n\n计划的第二项任务似乎也已经完成，然而……\n\n12... Kxe7 13. Kxh7 Kf7 14. Kh8 Kf8 15. h7 Kf7，逼和。\n\n由于黑方顽强而精确的抵抗，白方未能实现目标；黑方的防守揭示了一种有趣的和棋手段。",
    ),
    "BU-10": (
        "In positions where there are considerable forces operating (a characteristic of the central stage), the essence of the plan remains the same, but, of course, on the whole the game is complicated immeasurably. The defending side will have available far more possibilities of resistance, indeed also the attacking side has in prospect to make a choice between many objectives and ways to achieve them. The ability to choose the best and most correct from these is usually determined by the correctness of the evaluation of the position.",
        "在大量子力参与战斗的局面中，也就是典型的中局局面，计划的本质仍然相同；但总体而言，棋局会复杂得多。防守方拥有更多抵抗的可能，进攻方也要在众多目标及其实现途径之间作出选择。能否从中选出最好、最正确的一项，通常取决于对局面评价得是否准确。",
    ),
    "BU-11": (
        "Consider the starting position of the chess game.",
        "现在考察国际象棋的初始局面。",
    ),
    "BU-12": (
        "Many inexperienced amateurs assume that in the starting position it is not possible to draw up a relatively real plan of action, since this is very complicated in that on each of White's moves, Black has the possibility of replying in various ways. To some extent this is of course true. And yet, nowadays, in a period of stormy growth of creative ideas in chess art, and hence a continuous enrichment of its theory, we know only too well that the opening position is unclear. Already after the first, second and third moves, variations are obtained out of which arise objectives, not only in the sphere of purely the opening, but also in the whole of the future struggle. In selecting his first move, be it 1 c4, 1 d4, 1 Nf3 or 1 e4, the modern chessplayer is already contemplating several positions which he wants to achieve in the opening and which, in their turn, will be for him the initial point for working out a general strategical plan, which he will realise mainly in the middlegame.",
        "许多经验不足的业余棋手认为，从初始局面不可能制定出比较切实可行的行动计划，因为白方每走一步，黑方都有多种应法，问题过于复杂。在一定程度上，这当然是事实。然而，如今国际象棋艺术中的创造性思想正迅速发展，其理论也随之不断丰富；我们十分清楚，初始局面的发展方向并不明朗。仅仅走过第一步、第二步和第三步，各种变化就会出现，并由此产生相应的目标；这些目标不仅属于纯粹的开局范畴，还会影响未来整个斗争过程。现代棋手在选择第一步时，无论是1 c4、1 d4、1 Nf3还是1 e4，都已经在设想若干自己希望在开局中达到的局面。这些局面又将成为他制定总体战略计划的出发点，而这一计划主要在中局实现。",
    ),
    "BU-13": (
        "The planned process of the chess struggle can be subdivided into three stages:\n\n- the preparation for the general battle;\n- the struggle for the advantage, and\n- the realisation of the advantage.\n\nThe success of the first stage, to a considerable extent, is decided in the opening. The main and most complicated stage is undoubtedly the second. The third stage is getting results.",
        "有计划的棋局斗争过程可以分为三个阶段：\n\n- 为全面战斗做准备；\n- 争取优势；\n- 兑现优势。\n\n第一阶段能否成功，在很大程度上取决于开局。主要而且最复杂的无疑是第二阶段。第三阶段则是取得成果。",
    ),
}


def para_with_label(label, text, style):
    body = escape(text).replace("\n", "<br/>")
    return Paragraph(f'<font name="DengBold" color="#28756B">{label}</font><br/>{body}', style)


def bilingual_table(labels):
    data = [[Paragraph("经校正的英文 OCR", table_head), Paragraph("中文译文", table_head)]]
    for label in labels:
        english, chinese = ROWS[label]
        data.append([para_with_label(label, english, eng_style), para_with_label(label, chinese, zh_style)])
    table = Table(data, colWidths=[86 * mm, 98 * mm], repeatRows=1, hAlign="CENTER")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BOX", (0, 0), (-1, -1), 0.7, MID),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, MID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
    ]
    for idx in range(1, len(data)):
        commands.append(("BACKGROUND", (0, idx), (-1, idx), colors.white if idx % 2 else PALE))
    table.setStyle(TableStyle(commands))
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(MID)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, A4[1] - 14 * mm, A4[0] - 18 * mm, A4[1] - 14 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Deng", 8)
        canvas.drawString(18 * mm, A4[1] - 11 * mm, "《国际象棋中局计划》｜计划 - 基本认识｜校对稿")
    canvas.setFillColor(MUTED)
    canvas.setFont("Deng", 8)
    canvas.drawCentredString(A4[0] / 2, 10 * mm, str(doc.page))
    canvas.restoreState()


def crop(source, target, box):
    with PILImage.open(source) as image:
        image.crop(box).save(target)


def scaled_image(path, max_width, max_height):
    with PILImage.open(path) as image:
        width, height = image.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


diagram1 = WORK / "diagram-1.png"
diagram2 = WORK / "diagram-2.png"
diagram3 = WORK / "diagram-3.png"
source8_crop = WORK / "source-08-section.png"
source11_crop = WORK / "source-11-section.png"
crop(WORK / "source-09.png", diagram1, (250, 450, 1380, 1500))
crop(WORK / "source-09.png", diagram2, (1780, 2400, 2900, 3520))
crop(WORK / "source-10.png", diagram3, (1760, 1020, 2920, 2020))
crop(WORK / "source-08.png", source8_crop, (0, 1600, 3123, 4400))
crop(WORK / "source-11.png", source11_crop, (0, 0, 1550, 2380))

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=13 * mm,
    leftMargin=13 * mm,
    topMargin=20 * mm,
    bottomMargin=17 * mm,
    title="Chess Middlegame Planning - Basic Understanding - Chinese Proof",
    author="OCR and Chinese translation proof",
    subject="Corrected English OCR and Chinese translation for proofreading",
)

story = [Spacer(1, 27 * mm), Paragraph("《国际象棋中局计划》", cover_title), Paragraph("计划 - 一般原则 - 基本认识", cover_title), Spacer(1, 4 * mm), Paragraph("英文 OCR 校正稿 + 中文翻译校对稿", cover_subtitle), Spacer(1, 14 * mm)]
cover_info = [
    [Paragraph("文档性质", label_style), Paragraph("初译校对稿，非最终出版版本", info_style)],
    [Paragraph("内容范围", label_style), Paragraph("原书印刷页 6 至第 9 页左栏；止于 2: Concrete Ideas 之前", info_style)],
    [Paragraph("图与棋谱", label_style), Paragraph("保留三个原书局面图；中文译文中的着法统一采用现代 SAN 格式，例如 1. Kf4、1... Kf6、2. Kg4 Kg6", info_style)],
    [Paragraph("术语处理", label_style), Paragraph("passed pawn 译为“通路兵”；queening square 译为“升变格”；stalemate 译为“逼和”", info_style)],
    [Paragraph("版本日期", label_style), Paragraph("2026-09-23", info_style)],
]
info_table = Table(cover_info, colWidths=[30 * mm, 125 * mm], hAlign="CENTER")
info_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE), ("BOX", (0, 0), (-1, -1), 0.7, MID), ("INNERGRID", (0, 0), (-1, -1), 0.35, MID), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
story.append(info_table)
story.append(Spacer(1, 11 * mm))
story.append(Paragraph("建议重点核对：Basic Understanding 的标题译法；“弱方的王紧跟对方的王”；“兑现优势”；以及两个残局示例中的着法和计划分段。", section_note))
story.append(PageBreak())

story.append(Paragraph("计划（Planning）", section_title))
story.append(Paragraph("A：一般原则｜1 基本认识（Basic Understanding）", section_note))
story.append(bilingual_table(["BU-1", "BU-2", "BU-3", "BU-4"]))
story.append(PageBreak())

story.append(Paragraph("残局示例一", section_title))
story.append(Paragraph("原书图示，白方走。最终出版时应重绘为矢量棋盘。", diagram_caption))
story.append(scaled_image(diagram1, 70 * mm, 70 * mm))
story.append(Spacer(1, 6 * mm))
story.append(bilingual_table(["BU-5", "BU-6", "BU-7"]))
story.append(PageBreak())

story.append(Paragraph("残局示例二", section_title))
story.append(Paragraph("原书图示。最终出版时应重绘为矢量棋盘。", diagram_caption))
story.append(scaled_image(diagram2, 70 * mm, 70 * mm))
story.append(Spacer(1, 6 * mm))
story.append(bilingual_table(["BU-8", "BU-9"]))
story.append(PageBreak())

story.append(Paragraph("从残局计划到中局计划", section_title))
story.append(bilingual_table(["BU-10", "BU-11"]))
story.append(Spacer(1, 7 * mm))
story.append(Paragraph("国际象棋初始局面（原书图示）", diagram_caption))
story.append(scaled_image(diagram3, 68 * mm, 68 * mm))
story.append(PageBreak())
story.append(bilingual_table(["BU-12", "BU-13"]))
story.append(PageBreak())

story.append(Paragraph("附录：原扫描页", section_title))
story.append(Paragraph("以下图像仅用于本次 OCR、棋谱与译文校对。", section_note))
story.append(Paragraph("原书印刷页 6：Basic Understanding 起始部分", diagram_caption))
story.append(scaled_image(source8_crop, 170 * mm, 215 * mm))
story.append(PageBreak())
story.append(Paragraph("原书印刷页 7", diagram_caption))
story.append(scaled_image(WORK / "source-09.png", 170 * mm, 238 * mm))
story.append(PageBreak())
story.append(Paragraph("原书印刷页 8", diagram_caption))
story.append(scaled_image(WORK / "source-10.png", 170 * mm, 238 * mm))
story.append(PageBreak())
story.append(Paragraph("原书印刷页 9 左栏：Basic Understanding 结尾", diagram_caption))
story.append(scaled_image(source11_crop, 105 * mm, 205 * mm))

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
