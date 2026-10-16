import re
import sys
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, LongTable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(str(Path(__file__).resolve().parents[3]))
TRANS = ROOT / "translations" / "chess_middlegame_planning"
SOURCE = ROOT / "tmp" / "pdfs" / "middlegame_squares" / "source"
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

CONFIGS = [
    {
        "slug": "squares_1_weak_points", "stem": "06_squares_weak_points",
        "title": "B：格子 - 1：弱点", "header": "格子 - 弱点",
        "range": "原书印刷页 36-38", "labels": ["WP-1", "WP-2", "WP-3"],
        "scans": range(38, 41),
        "note": "重点核对 weak point 与 weak square 的概念区分、两个例局片段及棋手译名。",
    },
    {
        "slug": "squares_2_eternal_knight", "stem": "07_squares_eternal_knight",
        "title": "B：格子 - 2：铁马", "header": "格子 - 铁马",
        "range": "原书印刷页 38-43", "labels": [f"EK-{i}" for i in range(1, 6)],
        "scans": range(40, 46),
        "note": "重点核对“铁马”的术语、五组例局或片段、棋手译名和全部分析变例。",
    },
    {
        "slug": "squares_3_weak_sixth_rank", "stem": "08_squares_weak_sixth_rank",
        "title": "B：格子 - 3：第六（第三）横线上的弱格", "header": "格子 - 第六（第三）横线上的弱格",
        "range": "原书印刷页 43-51", "labels": [f"WS-{i}" for i in range(1, 8)],
        "scans": range(45, 54),
        "note": "重点核对第六（第三）横线的表述、六个主要实例、开局名称、棋手译名和棋谱。",
    },
    {
        "slug": "squares_4_some_conclusions", "stem": "09_squares_some_conclusions",
        "title": "B：格子 - 4：若干结论", "header": "格子 - 若干结论",
        "range": "原书印刷页 51-52", "labels": ["SC-1", "SC-2"],
        "scans": range(53, 55),
        "note": "重点核对结构性弱格、局面性原因、据点和象的侧翼出子等概念表述。",
    },
]

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
cover_title = ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="DengBold", fontSize=23, leading=32, textColor=NAVY, alignment=TA_CENTER, spaceAfter=12, wordWrap="CJK")
cover_subtitle = ParagraphStyle("CoverSubtitle", parent=styles["Normal"], fontName="Deng", fontSize=14, leading=22, textColor=TEAL, alignment=TA_CENTER, wordWrap="CJK")
section_title = ParagraphStyle("SectionTitle", parent=styles["Heading1"], fontName="DengBold", fontSize=18, leading=24, textColor=NAVY, spaceAfter=10, wordWrap="CJK")
section_note = ParagraphStyle("SectionNote", parent=styles["Normal"], fontName="Deng", fontSize=9, leading=14, textColor=MUTED, spaceAfter=10, wordWrap="CJK")
table_head = ParagraphStyle("TableHead", parent=styles["Normal"], fontName="DengBold", fontSize=10, leading=14, textColor=colors.white, alignment=TA_CENTER, wordWrap="CJK")
eng_style = ParagraphStyle("English", parent=styles["BodyText"], fontName="Times-Roman", fontSize=8.0, leading=11.25, textColor=TEXT, alignment=TA_LEFT)
zh_style = ParagraphStyle("Chinese", parent=styles["BodyText"], fontName="Deng", fontSize=8.8, leading=13.8, textColor=TEXT, alignment=TA_LEFT, wordWrap="CJK")
label_style = ParagraphStyle("Label", parent=styles["Normal"], fontName="DengBold", fontSize=8, leading=10, textColor=TEAL, wordWrap="CJK")
info_style = ParagraphStyle("Info", parent=styles["BodyText"], fontName="Deng", fontSize=10, leading=16, textColor=TEXT, wordWrap="CJK")
scan_caption = ParagraphStyle("ScanCaption", parent=styles["Normal"], fontName="DengBold", fontSize=10, leading=14, textColor=NAVY, alignment=TA_CENTER, spaceAfter=7, wordWrap="CJK")


def parse_sections(path):
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## ([A-Z]+-\d+)\s*$", text, flags=re.MULTILINE))
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


def labelled(label, value, style, chinese=False):
    body = rich_text(value, style, chinese).text
    return Paragraph(f'<font name="DengBold" color="#28756B">{label}</font><br/>{body}', style)


def bilingual_table(labels, english, chinese):
    data = [[Paragraph("经校正的英文 OCR", table_head), Paragraph("中文译文", table_head)]]
    for label in labels:
        data.append([labelled(label, english[label], eng_style), labelled(label, chinese[label], zh_style, True)])
    table = LongTable(data, colWidths=[86 * mm, 98 * mm], repeatRows=1, hAlign="CENTER", splitByRow=1, splitInRow=1)
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("BOX", (0, 0), (-1, -1), 0.7, MID),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, MID), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8), ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
    ]
    for index in range(1, len(data)):
        commands.append(("BACKGROUND", (0, index), (-1, index), colors.white if index % 2 else PALE))
    table.setStyle(TableStyle(commands))
    return table


def scaled_image(path, max_width, max_height):
    from PIL import Image as PILImage
    with PILImage.open(path) as image:
        width, height = image.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


VERSION = "v3" if "--v3" in sys.argv else ("v2" if "--v2" in sys.argv else "v1")
ONLY = {arg for arg in sys.argv[1:] if not arg.startswith("--")}


def build(config):
    en = parse_sections(TRANS / f'{config["stem"]}_en_ocr.md')
    zh = parse_sections(TRANS / f'{config["stem"]}_zh.md')
    expected = set(config["labels"])
    if set(en) != expected or set(zh) != expected:
        raise ValueError(f'{config["stem"]}: English={sorted(en)}, Chinese={sorted(zh)}')

    output = OUT / f'chess_middlegame_planning_{config["slug"]}_zh_proof_{VERSION}.pdf'
    doc = SimpleDocTemplate(
        str(output), pagesize=A4, rightMargin=13 * mm, leftMargin=13 * mm,
        topMargin=20 * mm, bottomMargin=17 * mm,
        title=f'Chess Middlegame Planning - {config["header"]} - Chinese Proof',
        author='OCR and Chinese translation proof',
    )

    def header_footer(canvas, doc_obj):
        canvas.saveState()
        if doc_obj.page > 1:
            canvas.setStrokeColor(MID)
            canvas.setLineWidth(0.5)
            canvas.line(18 * mm, A4[1] - 14 * mm, A4[0] - 18 * mm, A4[1] - 14 * mm)
            canvas.setFillColor(MUTED)
            canvas.setFont("Deng", 8)
            canvas.drawString(18 * mm, A4[1] - 11 * mm, f'《国际象棋中局计划》｜{config["header"]}｜校对稿')
        canvas.setFillColor(MUTED)
        canvas.setFont("Deng", 8)
        canvas.drawCentredString(A4[0] / 2, 10 * mm, str(doc_obj.page))
        canvas.restoreState()

    story = [
        Spacer(1, 27 * mm), Paragraph("《国际象棋中局计划》", cover_title),
        Paragraph(config["title"], cover_title), Spacer(1, 4 * mm),
        Paragraph("英文 OCR 校正稿 + 中文翻译校对稿", cover_subtitle), Spacer(1, 14 * mm),
    ]
    cover_info = [
        [Paragraph("文档性质", label_style), Paragraph("初译校对稿，非最终出版版本", info_style)],
        [Paragraph("内容范围", label_style), Paragraph(config["range"], info_style)],
        [Paragraph("棋谱规范", label_style), Paragraph("中文译文采用现代 SAN；黑方单独着法使用省略号；结果使用 1-0 / 0-1", info_style)],
        [Paragraph("术语延续", label_style), Paragraph("tempo 译为“先手”；动象 / 动后 / 动马 / 动车；material 按棋理语境译为“子力”", info_style)],
        [Paragraph("版本日期", label_style), Paragraph("2026-09-24", info_style)],
    ]
    table = Table(cover_info, colWidths=[30 * mm, 125 * mm], hAlign="CENTER")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE), ("BOX", (0, 0), (-1, -1), 0.7, MID),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, MID), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.extend([table, Spacer(1, 10 * mm), Paragraph(config["note"], section_note), PageBreak()])
    story.extend([Paragraph(config["title"], section_title), bilingual_table(config["labels"], en, zh), PageBreak()])
    story.extend([
        Paragraph("附录：原扫描页", section_title),
        Paragraph("以下扫描页保留原书棋盘图、版面和旧式记谱，用于核对 OCR、棋谱与译文。相邻小节共用的边界页会在两份校样中重复收录。", section_note),
        PageBreak(),
    ])
    scans = list(config["scans"])
    for index, page in enumerate(scans):
        story.append(Paragraph(f"原书印刷页 {page - 2}", scan_caption))
        story.append(scaled_image(SOURCE / f"page-{page:03d}.png", 170 * mm, 238 * mm))
        if index != len(scans) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(output)


for item in CONFIGS:
    if not ONLY or item["slug"] in ONLY:
        build(item)
