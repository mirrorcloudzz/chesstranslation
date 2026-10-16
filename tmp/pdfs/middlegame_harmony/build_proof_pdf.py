import re
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import CondPageBreak, Image, LongTable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(str(Path(__file__).resolve().parents[3]))
WORK = ROOT / "tmp" / "pdfs" / "middlegame_harmony"
EN_MD = ROOT / "translations" / "chess_middlegame_planning" / "05_planning_harmony_en_ocr.md"
ZH_MD = ROOT / "translations" / "chess_middlegame_planning" / "05_planning_harmony_zh.md"
OUTPUT = ROOT / "output" / "pdf" / "chess_middlegame_planning_harmony_zh_proof_v2.pdf"
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
cover_title = ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="DengBold", fontSize=24, leading=33, textColor=NAVY, alignment=TA_CENTER, spaceAfter=12, wordWrap="CJK")
cover_subtitle = ParagraphStyle("CoverSubtitle", parent=styles["Normal"], fontName="Deng", fontSize=14, leading=22, textColor=TEAL, alignment=TA_CENTER, wordWrap="CJK")
section_title = ParagraphStyle("SectionTitle", parent=styles["Heading1"], fontName="DengBold", fontSize=18, leading=24, textColor=NAVY, spaceAfter=10, wordWrap="CJK")
section_note = ParagraphStyle("SectionNote", parent=styles["Normal"], fontName="Deng", fontSize=9, leading=14, textColor=MUTED, spaceAfter=10, wordWrap="CJK")
table_head = ParagraphStyle("TableHead", parent=styles["Normal"], fontName="DengBold", fontSize=10, leading=14, textColor=colors.white, alignment=TA_CENTER, wordWrap="CJK")
eng_style = ParagraphStyle("English", parent=styles["BodyText"], fontName="Times-Roman", fontSize=8.15, leading=11.45, textColor=TEXT, alignment=TA_LEFT)
zh_style = ParagraphStyle("Chinese", parent=styles["BodyText"], fontName="Deng", fontSize=8.95, leading=14.1, textColor=TEXT, alignment=TA_LEFT, wordWrap="CJK")
label_style = ParagraphStyle("Label", parent=styles["Normal"], fontName="DengBold", fontSize=8, leading=10, textColor=TEAL, wordWrap="CJK")
info_style = ParagraphStyle("Info", parent=styles["BodyText"], fontName="Deng", fontSize=10, leading=16.5, textColor=TEXT, wordWrap="CJK")
scan_caption = ParagraphStyle("ScanCaption", parent=styles["Normal"], fontName="DengBold", fontSize=10, leading=14, textColor=NAVY, alignment=TA_CENTER, spaceAfter=7, wordWrap="CJK")


def parse_sections(path):
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## (HA-\d+)\s*$", text, flags=re.MULTILINE))
    result = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[match.end():end].strip()
    return result


def rich_text(text, style, chinese=False):
    value = escape(text)
    if chinese:
        value = re.sub(r"`([^`]+)`", r'<font name="Courier" color="#15324A">\1</font>', value)
        value = re.sub(r"^### (.+)$", r'<font name="DengBold" size="12" color="#15324A">\1</font>', value, flags=re.MULTILINE)
    else:
        value = re.sub(r"^### (.+)$", r'<font name="Times-Bold" size="11" color="#15324A">\1</font>', value, flags=re.MULTILINE)
    value = value.replace("  \n", "<br/>")
    value = value.replace("\n\n", "<br/><br/>").replace("\n", "<br/>")
    return Paragraph(value, style)


def labelled(label, text, style, chinese=False):
    return Paragraph(f'<font name="DengBold" color="#28756B">{label}</font><br/>{rich_text(text, style, chinese).text}', style)


def bilingual_table(labels, english_sections, chinese_sections):
    data = [[Paragraph("经校正的英文 OCR", table_head), Paragraph("中文译文", table_head)]]
    for label in labels:
        data.append([labelled(label, english_sections[label], eng_style), labelled(label, chinese_sections[label], zh_style, True)])
    table = LongTable(data, colWidths=[86 * mm, 98 * mm], repeatRows=1, hAlign="CENTER", splitByRow=1, splitInRow=1)
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
    for index in range(1, len(data)):
        commands.append(("BACKGROUND", (0, index), (-1, index), colors.white if index % 2 else PALE))
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
        canvas.drawString(18 * mm, A4[1] - 11 * mm, "《国际象棋中局计划》｜计划 - 协调性｜校对稿")
    canvas.setFillColor(MUTED)
    canvas.setFont("Deng", 8)
    canvas.drawCentredString(A4[0] / 2, 10 * mm, str(doc.page))
    canvas.restoreState()


def scaled_image(path, max_width, max_height):
    from PIL import Image as PILImage

    with PILImage.open(path) as image:
        width, height = image.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


english_sections = parse_sections(EN_MD)
chinese_sections = parse_sections(ZH_MD)
expected = {f"HA-{number}" for number in range(1, 16)}
if set(english_sections) != expected or set(chinese_sections) != expected:
    raise ValueError(f"Section mismatch: English={sorted(english_sections)}, Chinese={sorted(chinese_sections)}")

doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4, rightMargin=13 * mm, leftMargin=13 * mm, topMargin=20 * mm, bottomMargin=17 * mm,
    title="Chess Middlegame Planning - Harmony - Chinese Proof", author="OCR and Chinese translation proof",
    subject="Corrected English OCR and Chinese translation for proofreading",
)

story = [
    Spacer(1, 27 * mm),
    Paragraph("《国际象棋中局计划》", cover_title),
    Paragraph("计划 - 一般原则 - 协调性", cover_title),
    Spacer(1, 4 * mm),
    Paragraph("英文 OCR 校正稿 + 中文翻译校对稿", cover_subtitle),
    Spacer(1, 14 * mm),
]
cover_info = [
    [Paragraph("文档性质", label_style), Paragraph("初译校对稿，非最终出版版本", info_style)],
    [Paragraph("内容范围", label_style), Paragraph("原书印刷页 26 至第 36 页；止于 B: Squares / 1: Weak Points 之前", info_style)],
    [Paragraph("棋谱规范", label_style), Paragraph("中文译文采用现代 SAN；黑方单独着法使用省略号；将杀使用 #", info_style)],
    [Paragraph("术语延续", label_style), Paragraph("material 依棋理语境译为“子力”；mate in N moves 译为“N步杀”；sacrifice 译为“弃子”", info_style)],
    [Paragraph("版本日期", label_style), Paragraph("2026-09-23", info_style)],
]
info_table = Table(cover_info, colWidths=[30 * mm, 125 * mm], hAlign="CENTER")
info_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE), ("BOX", (0, 0), (-1, -1), 0.7, MID),
    ("INNERGRID", (0, 0), (-1, -1), 0.35, MID), ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(info_table)
story.append(Spacer(1, 10 * mm))
story.append(Paragraph("建议重点核对：Harmony 的标题译法；协调性与子力经济原则的术语；棋手姓名；以及五个实例中的全部实战和分析变例。", section_note))
story.append(PageBreak())

story.append(Paragraph("4 协调性（Harmony）", section_title))
story.append(Paragraph("原则说明与三个残局片段", section_note))
story.append(bilingual_table(["HA-1", "HA-2", "HA-3", "HA-4", "HA-5"], english_sections, chinese_sections))

story.append(CondPageBreak(38 * mm))
story.append(Spacer(1, 7 * mm))
story.append(Paragraph("例局一：阿廖欣 - 尤伟", section_title))
story.append(bilingual_table(["HA-6", "HA-7", "HA-8", "HA-9"], english_sections, chinese_sections))

story.append(CondPageBreak(38 * mm))
story.append(Spacer(1, 7 * mm))
story.append(Paragraph("例局二：戈特希尔夫 - 罗曼诺夫斯基", section_title))
story.append(bilingual_table(["HA-10", "HA-11", "HA-12", "HA-13", "HA-14"], english_sections, chinese_sections))

story.append(CondPageBreak(38 * mm))
story.append(Spacer(1, 7 * mm))
story.append(Paragraph("本节总结", section_title))
story.append(bilingual_table(["HA-15"], english_sections, chinese_sections))
story.append(PageBreak())

story.append(Paragraph("附录：原扫描页", section_title))
story.append(Paragraph("以下图像保留原书棋盘图、版面和旧式记谱，用于核对 OCR、棋谱与译文。印刷页 26 的上半页属于上一节；印刷页 36 的后半页已经进入下一章。", section_note))
story.append(PageBreak())
for page in range(28, 39):
    printed = page - 2
    story.append(Paragraph(f"原书印刷页 {printed}", scan_caption))
    story.append(scaled_image(WORK / f"source-{page:03d}.png", 170 * mm, 238 * mm))
    if page != 38:
        story.append(PageBreak())

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
