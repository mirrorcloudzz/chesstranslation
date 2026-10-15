import json
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
from reportlab.platypus import LongTable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess")
TMP = ROOT / "tmp" / "pdfs" / "middlegame_chapters34"
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

CONFIGS = [
    {
        "chapter": 3,
        "start": 89,
        "end": 100,
        "prefix": "CH3",
        "title": "第三章：a线上的战斗",
        "short": "第三章｜a线上的战斗",
        "range": "原书印刷页 87–98",
        "output": "chess_middlegame_planning_chapter_three_a_file_bilingual_proof_v2.pdf",
    },
    {
        "chapter": 4,
        "start": 101,
        "end": 144,
        "prefix": "CH4",
        "title": "第四章：中心及其战略意义",
        "short": "第四章｜中心及其战略意义",
        "range": "原书印刷页 99–142",
        "output": "chess_middlegame_planning_chapter_four_centre_bilingual_proof_v2.pdf",
    },
]

pdfmetrics.registerFont(TTFont("Deng", r"C:\Windows\Fonts\Deng.ttf"))
pdfmetrics.registerFont(TTFont("DengBold", r"C:\Windows\Fonts\Dengb.ttf"))
pdfmetrics.registerFontFamily('Deng', normal='Deng', bold='DengBold', italic='Deng', boldItalic='DengBold')

NAVY = colors.HexColor("#18354C")
BLUE = colors.HexColor("#3B6885")
PALE = colors.HexColor("#F5F7F8")
RULE = colors.HexColor("#CDD5DB")
TEXT = colors.HexColor("#202A31")
MUTED = colors.HexColor("#64727B")

base = getSampleStyleSheet()
cover_title = ParagraphStyle(
    "CoverTitle", parent=base["Title"], fontName="DengBold", fontSize=22,
    leading=31, textColor=NAVY, alignment=TA_CENTER, wordWrap="CJK",
)
cover_subtitle = ParagraphStyle(
    "CoverSubtitle", parent=base["Normal"], fontName="Deng", fontSize=12,
    leading=20, textColor=BLUE, alignment=TA_CENTER, wordWrap="CJK",
)
info_label = ParagraphStyle(
    "InfoLabel", parent=base["Normal"], fontName="DengBold", fontSize=9,
    leading=14, textColor=NAVY, wordWrap="CJK",
)
info_value = ParagraphStyle(
    "InfoValue", parent=base["Normal"], fontName="Deng", fontSize=9.5,
    leading=15, textColor=TEXT, wordWrap="CJK",
)
table_head = ParagraphStyle(
    "TableHead", parent=base["Normal"], fontName="DengBold", fontSize=9.5,
    leading=13, textColor=colors.white, alignment=TA_CENTER, wordWrap="CJK",
)
eng_style = ParagraphStyle(
    "English", parent=base["BodyText"], fontName="Times-Roman", fontSize=7.6,
    leading=10.7, textColor=TEXT, alignment=TA_LEFT, splitLongWords=True,
)
eng_bold = ParagraphStyle(
    "EnglishBold", parent=eng_style, fontName="Times-Bold",
)
zh_style = ParagraphStyle(
    "Chinese", parent=base["BodyText"], fontName="Deng", fontSize=8.5,
    leading=13.2, textColor=TEXT, alignment=TA_LEFT, wordWrap="CJK",
)
zh_bold = ParagraphStyle(
    "ChineseBold", parent=zh_style, fontName="DengBold",
)


def xml_text(value: str) -> str:
    value = escape(value)
    value = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', value)
    value = value.replace("\n", "<br/>")
    return value


def segment_cell(label: str, page_label: str, value: str, style, chinese=False):
    label_font = "DengBold"
    body = xml_text(value)
    return Paragraph(
        f'<font name="{label_font}" size="7.4" color="#3B6885">{label} · {page_label}</font>'
        f'<br/><font name="{style.fontName}">{body}</font>',
        style,
    )


def selected_segments(all_segments, config):
    return [
        item for item in all_segments
        if config["start"] <= item["page"] <= config["end"] and item["kind"] != "chapter"
    ]


def page_reference(item):
    first = item["page"] - 2
    last = item.get("page_end", item["page"]) - 2
    return f"原书{first}页" if first == last else f"原书{first}–{last}页"


def build(config, all_segments):
    segments = selected_segments(all_segments, config)
    output = OUT / config["output"]
    doc = SimpleDocTemplate(
        str(output), pagesize=A4,
        leftMargin=13 * mm, rightMargin=13 * mm,
        topMargin=20 * mm, bottomMargin=16 * mm,
        title=f'Chess Middlegame Planning - {config["title"]} - Bilingual Proof',
        author="English OCR and Chinese translation proof",
    )

    def header_footer(canvas, doc_obj):
        canvas.saveState()
        if doc_obj.page > 1:
            canvas.setStrokeColor(RULE)
            canvas.setLineWidth(0.45)
            canvas.line(17 * mm, A4[1] - 14 * mm, A4[0] - 17 * mm, A4[1] - 14 * mm)
            canvas.setFillColor(MUTED)
            canvas.setFont("Deng", 8)
            canvas.drawString(17 * mm, A4[1] - 11 * mm,
                              f'《国际象棋中局计划》｜{config["short"]}｜中英对照分段校样')
        canvas.setFillColor(MUTED)
        canvas.setFont("Deng", 8)
        canvas.drawCentredString(A4[0] / 2, 9.5 * mm, str(doc_obj.page))
        canvas.restoreState()

    first_id = segments[0].get('segment_id', f'{config["prefix"]}-1')
    last_id = segments[-1].get('segment_id', f'{config["prefix"]}-{len(segments)}')
    cover_info = [
        [Paragraph("文档性质", info_label), Paragraph("英文 OCR 复核稿 + 中文修订校对稿", info_value)],
        [Paragraph("内容范围", info_label), Paragraph(config["range"], info_value)],
        [Paragraph("段落编号", info_label), Paragraph(f"{first_id} 至 {last_id}，左右栏严格对应", info_value)],
        [Paragraph("版本日期", info_label), Paragraph("2026-09-27", info_value)],
    ]
    info = Table(cover_info, colWidths=[29 * mm, 119 * mm], hAlign="CENTER")
    info.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))

    data = [[Paragraph("经复核的英文 OCR", table_head), Paragraph("中文修订稿", table_head)]]
    for number, item in enumerate(segments, 1):
        label = item.get('segment_id', f'{config["prefix"]}-{number}')
        kind = item.get("kind", "body")
        en_cell_style = eng_bold if kind in {"title", "heading", "metadata"} else eng_style
        zh_cell_style = zh_bold if kind in {"title", "heading", "metadata"} else zh_style
        ref = page_reference(item)
        data.append([
            segment_cell(label, ref, item["text"], en_cell_style),
            segment_cell(label, ref, item["zh"], zh_cell_style, True),
        ])
    table = LongTable(
        data, colWidths=[86 * mm, 98 * mm], repeatRows=1,
        splitByRow=1, splitInRow=0, hAlign="CENTER",
    )
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, NAVY),
        ("LINEBELOW", (0, 1), (-1, -1), 0.32, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6.5),
        ("TOPPADDING", (0, 1), (-1, -1), 6.5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6.5),
    ]
    for row in range(1, len(data)):
        commands.append(("BACKGROUND", (0, row), (-1, row), colors.white if row % 2 else PALE))
    table.setStyle(TableStyle(commands))

    story = [
        Spacer(1, 28 * mm),
        Paragraph("《国际象棋中局计划》", cover_title),
        Paragraph(config["title"], cover_title),
        Spacer(1, 5 * mm),
        Paragraph("中英对照分段校样", cover_subtitle),
        Spacer(1, 15 * mm),
        info,
        PageBreak(),
        table,
    ]
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(output)


MANUSCRIPTS = ROOT / "translations" / "chess_middlegame_planning"
all_segments = []
for filename in ["13_chapter_three_reviewed.json", "14_chapter_four_reviewed.json"]:
    all_segments.extend(json.loads((MANUSCRIPTS / filename).read_text(encoding="utf-8")))
for config in CONFIGS:
    build(config, all_segments)

