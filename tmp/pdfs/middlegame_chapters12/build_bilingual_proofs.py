import re
import sys
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
from reportlab.platypus import Image, LongTable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(str(Path(__file__).resolve().parents[3]))
TRANS = ROOT / "translations" / "chess_middlegame_planning"
SOURCE = ROOT / "tmp" / "pdfs" / "middlegame_chapters12" / "source"
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

CONFIGS = [
    {
        "prefix": "CH1", "count": 10,
        "en": "11_chapter_one_steinitz_en_ocr.md", "zh": "11_chapter_one_steinitz_zh.md",
        "title": "第一章：威廉·斯坦尼茨的两场胜局",
        "short": "第一章｜斯坦尼茨的两场胜局",
        "range": "原书印刷页 60–67", "pages": range(62, 70),
        "output": "chess_middlegame_planning_chapter_one_steinitz_zh_proof_v2.pdf",
        "version_date": "2026-09-26",
        "focus": "重点核对两盘斯坦尼茨—拉斯克例局、全部分析变化，以及“稳固中心后发动侧翼进攻”和“以最少力量取得最大成果”等核心表述。",
    },
    {
        "prefix": "CH2", "count": 15,
        "en": "12_chapter_two_stages_en_ocr.md", "zh": "12_chapter_two_stages_zh.md",
        "title": "第二章：计划的各个阶段",
        "short": "第二章｜计划的各个阶段",
        "range": "原书印刷页 68–86", "pages": range(70, 89),
        "output": "chess_middlegame_planning_chapter_two_stages_zh_proof_v1.pdf",
        "version_date": "2026-09-24",
        "focus": "重点核对三阶段与四阶段计划、弱格和开放线、三盘完整例局，以及长篇变化中的行棋次序和术语一致性。",
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
cover_title = ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="DengBold", fontSize=22, leading=31, textColor=NAVY, alignment=TA_CENTER, spaceAfter=12, wordWrap="CJK")
cover_subtitle = ParagraphStyle("CoverSubtitle", parent=styles["Normal"], fontName="Deng", fontSize=13, leading=21, textColor=TEAL, alignment=TA_CENTER, wordWrap="CJK")
section_title = ParagraphStyle("SectionTitle", parent=styles["Heading1"], fontName="DengBold", fontSize=18, leading=24, textColor=NAVY, spaceAfter=10, wordWrap="CJK")
section_note = ParagraphStyle("SectionNote", parent=styles["Normal"], fontName="Deng", fontSize=9, leading=14, textColor=MUTED, spaceAfter=10, wordWrap="CJK")
table_head = ParagraphStyle("TableHead", parent=styles["Normal"], fontName="DengBold", fontSize=10, leading=14, textColor=colors.white, alignment=TA_CENTER, wordWrap="CJK")
eng_style = ParagraphStyle("English", parent=styles["BodyText"], fontName="Times-Roman", fontSize=7.7, leading=10.8, textColor=TEXT, alignment=TA_LEFT, splitLongWords=True)
zh_style = ParagraphStyle("Chinese", parent=styles["BodyText"], fontName="Deng", fontSize=8.55, leading=13.4, textColor=TEXT, alignment=TA_LEFT, wordWrap="CJK")
label_style = ParagraphStyle("Label", parent=styles["Normal"], fontName="DengBold", fontSize=8, leading=10, textColor=TEAL, wordWrap="CJK")
info_style = ParagraphStyle("Info", parent=styles["BodyText"], fontName="Deng", fontSize=10, leading=16, textColor=TEXT, wordWrap="CJK")
scan_caption = ParagraphStyle("ScanCaption", parent=styles["Normal"], fontName="DengBold", fontSize=10, leading=14, textColor=NAVY, alignment=TA_CENTER, spaceAfter=7, wordWrap="CJK")


def parse_sections(path, prefix):
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(rf"^## ({re.escape(prefix)}-\d+)\s*$", text, flags=re.MULTILINE))
    result = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[match.end():end].strip()
    return result


def rich_text(text, style, chinese=False):
    # Mainline move paragraphs are bold in the original. Inline analysis
    # variations keep the surrounding body weight.
    text = re.sub(r"(?m)^`([^`]+)`$", r"**`\1`**", text)
    value = escape(text)
    value = re.sub(r"`([^`]+)`", r'<font color="#15324A">\1</font>', value)
    font = "DengBold" if chinese else "Times-Bold"
    value = re.sub(r"^#### (.+)$", rf'<font name="{font}" size="10" color="#28756B">\1</font>', value, flags=re.MULTILINE)
    value = re.sub(r"^### (.+)$", rf'<font name="{font}" size="11.5" color="#15324A">\1</font>', value, flags=re.MULTILINE)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
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
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 7), ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
    ]
    for index in range(1, len(data)):
        commands.append(("BACKGROUND", (0, index), (-1, index), colors.white if index % 2 else PALE))
    table.setStyle(TableStyle(commands))
    return table


def scaled_image(path, max_width, max_height):
    with PILImage.open(path) as image:
        width, height = image.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


def build(config):
    labels = [f'{config["prefix"]}-{i}' for i in range(1, config["count"] + 1)]
    english = parse_sections(TRANS / config["en"], config["prefix"])
    chinese = parse_sections(TRANS / config["zh"], config["prefix"])
    expected = set(labels)
    if set(english) != expected or set(chinese) != expected:
        raise ValueError(f'{config["prefix"]}: English={sorted(english)}, Chinese={sorted(chinese)}')

    output = OUT / config["output"]
    doc = SimpleDocTemplate(
        str(output), pagesize=A4, rightMargin=13 * mm, leftMargin=13 * mm,
        topMargin=20 * mm, bottomMargin=17 * mm,
        title=f'Chess Middlegame Planning - {config["title"]} - Chinese Bilingual Proof',
        author="OCR and Chinese translation proof",
    )

    def header_footer(canvas, doc_obj):
        canvas.saveState()
        if doc_obj.page > 1:
            canvas.setStrokeColor(MID)
            canvas.setLineWidth(0.5)
            canvas.line(18 * mm, A4[1] - 14 * mm, A4[0] - 18 * mm, A4[1] - 14 * mm)
            canvas.setFillColor(MUTED)
            canvas.setFont("Deng", 8)
            canvas.drawString(18 * mm, A4[1] - 11 * mm, f'《国际象棋中局计划》｜{config["short"]}｜中英文对照校对稿')
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
        [Paragraph("段落编号", label_style), Paragraph(f'{labels[0]} 至 {labels[-1]}；左右栏按编号严格对应', info_style)],
        [Paragraph("棋谱规范", label_style), Paragraph("中英文棋谱均采用现代 SAN；黑方单独行棋时使用省略号；结果使用 1-0 / 0-1", info_style)],
        [Paragraph("术语延续", label_style), Paragraph("出子、先手、动象 / 动后 / 动马 / 动车、子力、得子 / 失子、弃子、冲起、过渡着等沿用既定规范", info_style)],
        [Paragraph("版本日期", label_style), Paragraph(config["version_date"], info_style)],
    ]
    cover_table = Table(cover_info, colWidths=[30 * mm, 125 * mm], hAlign="CENTER")
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE), ("BOX", (0, 0), (-1, -1), 0.7, MID),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, MID), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.extend([
        cover_table, Spacer(1, 10 * mm), Paragraph(config["focus"], section_note), PageBreak(),
        Paragraph(config["title"], section_title), bilingual_table(labels, english, chinese), PageBreak(),
        Paragraph("附录：原扫描页", section_title),
        Paragraph("以下扫描页保留原书棋盘图、版面和旧式记谱，用于核对 OCR、棋谱与译文。", section_note), PageBreak(),
    ])
    pages = list(config["pages"])
    for index, page in enumerate(pages):
        story.append(Paragraph(f"原书印刷页 {page - 2}", scan_caption))
        story.append(scaled_image(SOURCE / f"page-{page:03d}.png", 170 * mm, 238 * mm))
        if index != len(pages) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(output)


selected = {item.upper() for item in sys.argv[1:]}
for chapter in CONFIGS:
    if not selected or chapter["prefix"] in selected:
        build(chapter)
