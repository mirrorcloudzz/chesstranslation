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
TMP = Path(__file__).resolve().parent
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
SEGMENTS = json.loads((TMP / "reviewed_segments.json").read_text(encoding="utf-8"))

CONFIGS = [
    {"chapter": 5, "title": "第五章：进一步谈兵的积极行动", "short": "第五章｜进一步谈兵的积极行动",
     "range": "原书印刷页 143-174", "output": "chess_middlegame_planning_chapter_five_active_pawns_bilingual_proof_v1.pdf"},
    {"chapter": 6, "title": "第六章：重子斗争", "short": "第六章｜重子斗争",
     "range": "原书印刷页 175-193", "output": "chess_middlegame_planning_chapter_six_heavy_pieces_bilingual_proof_v1.pdf"},
    {"chapter": 7, "title": "第七章：调动与主动权", "short": "第七章｜调动与主动权",
     "range": "原书印刷页 194-214", "output": "chess_middlegame_planning_chapter_seven_manoeuvring_initiative_bilingual_proof_v1.pdf"},
    {"chapter": 8, "title": "第八章：双象", "short": "第八章｜双象",
     "range": "原书印刷页 215-225", "output": "chess_middlegame_planning_chapter_eight_two_bishops_bilingual_proof_v1.pdf"},
]

pdfmetrics.registerFont(TTFont("Deng", r"C:\Windows\Fonts\Deng.ttf"))
pdfmetrics.registerFont(TTFont("DengBold", r"C:\Windows\Fonts\Dengb.ttf"))
pdfmetrics.registerFontFamily("Deng", normal="Deng", bold="DengBold", italic="Deng", boldItalic="DengBold")

NAVY = colors.HexColor("#18354C")
BLUE = colors.HexColor("#3B6885")
PALE = colors.HexColor("#F5F7F8")
RULE = colors.HexColor("#CDD5DB")
TEXT = colors.HexColor("#202A31")
MUTED = colors.HexColor("#64727B")

base = getSampleStyleSheet()
cover_title = ParagraphStyle("CoverTitle", parent=base["Title"], fontName="DengBold", fontSize=22,
                             leading=31, textColor=NAVY, alignment=TA_CENTER, wordWrap="CJK")
cover_subtitle = ParagraphStyle("CoverSubtitle", parent=base["Normal"], fontName="Deng", fontSize=12,
                                leading=20, textColor=BLUE, alignment=TA_CENTER, wordWrap="CJK")
info_label = ParagraphStyle("InfoLabel", parent=base["Normal"], fontName="DengBold", fontSize=9,
                            leading=14, textColor=NAVY, wordWrap="CJK")
info_value = ParagraphStyle("InfoValue", parent=base["Normal"], fontName="Deng", fontSize=9.5,
                            leading=15, textColor=TEXT, wordWrap="CJK")
table_head = ParagraphStyle("TableHead", parent=base["Normal"], fontName="DengBold", fontSize=9.5,
                            leading=13, textColor=colors.white, alignment=TA_CENTER, wordWrap="CJK")
eng_style = ParagraphStyle("English", parent=base["BodyText"], fontName="Times-Roman", fontSize=7.45,
                           leading=10.5, textColor=TEXT, alignment=TA_LEFT, splitLongWords=True)
eng_bold = ParagraphStyle("EnglishBold", parent=eng_style, fontName="Times-Bold")
zh_style = ParagraphStyle("Chinese", parent=base["BodyText"], fontName="Deng", fontSize=8.35,
                          leading=13, textColor=TEXT, alignment=TA_LEFT, wordWrap="CJK")
zh_bold = ParagraphStyle("ChineseBold", parent=zh_style, fontName="DengBold")


def xml_text(value):
    value = escape(value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    return value.replace("\n", "<br/>")


def page_reference(item):
    first = item["page"] - 2
    last = item.get("page_end", item["page"]) - 2
    return f"原书{first}页" if first == last else f"原书{first}-{last}页"


def segment_cell(label, page_label, value, style):
    return Paragraph(
        f'<font name="DengBold" size="7.4" color="#3B6885">{label} · {page_label}</font>'
        f'<br/><font name="{style.fontName}">{xml_text(value)}</font>', style
    )


def build(config):
    selected = [x for x in SEGMENTS if x["chapter"] == config["chapter"]]
    output = OUT / config["output"]
    doc = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=13*mm, rightMargin=13*mm,
                            topMargin=20*mm, bottomMargin=16*mm,
                            title=f'Chess Middlegame Planning - {config["title"]} - Bilingual Proof',
                            author="English OCR and Chinese revised translation proof")

    def furniture(canvas, doc_obj):
        canvas.saveState()
        if doc_obj.page > 1:
            canvas.setStrokeColor(RULE); canvas.setLineWidth(0.45)
            canvas.line(17*mm, A4[1]-14*mm, A4[0]-17*mm, A4[1]-14*mm)
            canvas.setFillColor(MUTED); canvas.setFont("Deng", 8)
            canvas.drawString(17*mm, A4[1]-11*mm,
                              f'《国际象棋中局计划》｜{config["short"]}｜中英对照分段校样')
        canvas.setFillColor(MUTED); canvas.setFont("Deng", 8)
        canvas.drawCentredString(A4[0]/2, 9.5*mm, str(doc_obj.page))
        canvas.restoreState()

    info_data = [
        [Paragraph("文档性质", info_label), Paragraph("英文 OCR 校对稿 + 中文修订稿（待用户校对）", info_value)],
        [Paragraph("内容范围", info_label), Paragraph(config["range"], info_value)],
        [Paragraph("段落编号", info_label), Paragraph(f'{selected[0]["segment_id"]} 至 {selected[-1]["segment_id"]}，左右栏严格对应', info_value)],
        [Paragraph("术语规范", info_label), Paragraph("沿用此前已确认的棋谱、棋子、兵形与行棋术语", info_value)],
        [Paragraph("版本日期", info_label), Paragraph("2026-09-28 · 语言与术语复核版", info_value)],
    ]
    info = Table(info_data, colWidths=[29*mm, 119*mm], hAlign="CENTER")
    info.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PALE), ("LINEBELOW", (0,0), (-1,-2), 0.35, RULE),
        ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8), ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))

    data = [[Paragraph("英文 OCR 校对稿", table_head), Paragraph("中文修订稿", table_head)]]
    for item in selected:
        bold = item.get("kind") in {"title", "heading", "metadata"}
        data.append([
            segment_cell(item["segment_id"], page_reference(item), item["text"], eng_bold if bold else eng_style),
            segment_cell(item["segment_id"], page_reference(item), item["zh"], zh_bold if bold else zh_style),
        ])
    table = LongTable(data, colWidths=[86*mm, 98*mm], repeatRows=1,
                      splitByRow=1, splitInRow=0, hAlign="CENTER")
    commands = [
        ("BACKGROUND", (0,0), (-1,0), NAVY), ("LINEBELOW", (0,0), (-1,0), 0.8, NAVY),
        ("LINEBELOW", (0,1), (-1,-1), 0.32, RULE), ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 6.5), ("RIGHTPADDING", (0,0), (-1,-1), 6.5),
        ("TOPPADDING", (0,1), (-1,-1), 6.5), ("BOTTOMPADDING", (0,1), (-1,-1), 6.5),
    ]
    for row in range(1, len(data)):
        commands.append(("BACKGROUND", (0,row), (-1,row), colors.white if row % 2 else PALE))
    table.setStyle(TableStyle(commands))

    story = [Spacer(1, 28*mm), Paragraph("《国际象棋中局计划》", cover_title),
             Paragraph(config["title"], cover_title), Spacer(1, 5*mm),
             Paragraph("中英对照分段校样 · 修订版", cover_subtitle), Spacer(1, 15*mm),
             info, PageBreak(), table]
    doc.build(story, onFirstPage=furniture, onLaterPages=furniture)
    print(output)


for config in CONFIGS:
    config["output"] = config["output"].replace("_v1.pdf", "_v2.pdf")
    build(config)
