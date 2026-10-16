import re
import sys
from html import escape
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(str(Path(__file__).resolve().parents[3]))
TRANS = ROOT / "translations" / "chess_middlegame_planning"
DIAGRAMS = ROOT / "tmp" / "pdfs" / "middlegame_chapters12" / "diagrams"
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("CN", r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("CNBold", r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))

INK = colors.HexColor("#263238")
ACCENT = colors.HexColor("#395B64")
MUTED = colors.HexColor("#6B7478")
RULE = colors.HexColor("#BAC4C7")

styles = getSampleStyleSheet()
cover_title = ParagraphStyle(
    "CoverTitle",
    parent=styles["Title"],
    fontName="CNBold",
    fontSize=24,
    leading=34,
    textColor=ACCENT,
    alignment=TA_CENTER,
    wordWrap="CJK",
)
cover_subtitle = ParagraphStyle(
    "CoverSubtitle",
    parent=styles["Normal"],
    fontName="CN",
    fontSize=12,
    leading=20,
    textColor=MUTED,
    alignment=TA_CENTER,
    wordWrap="CJK",
)
chapter_heading = ParagraphStyle(
    "ChapterHeading",
    parent=styles["Heading1"],
    fontName="CNBold",
    fontSize=19,
    leading=27,
    textColor=ACCENT,
    spaceBefore=2 * mm,
    spaceAfter=4 * mm,
    wordWrap="CJK",
)
subheading = ParagraphStyle(
    "Subheading",
    parent=styles["Heading2"],
    fontName="CNBold",
    fontSize=12,
    leading=18,
    textColor=ACCENT,
    spaceBefore=2.5 * mm,
    spaceAfter=2 * mm,
    wordWrap="CJK",
)
body_style = ParagraphStyle(
    "BodyCN",
    parent=styles["BodyText"],
    fontName="CN",
    fontSize=10.2,
    leading=17.2,
    textColor=INK,
    alignment=TA_JUSTIFY,
    firstLineIndent=2 * 10.2,
    spaceAfter=2.3 * mm,
    wordWrap="CJK",
)
move_style = ParagraphStyle(
    "MoveCN",
    parent=body_style,
    fontName="CNBold",
    firstLineIndent=0,
    leftIndent=4 * mm,
    rightIndent=3 * mm,
    spaceBefore=0.7 * mm,
    spaceAfter=1.7 * mm,
)
bullet_style = ParagraphStyle(
    "BulletCN",
    parent=body_style,
    firstLineIndent=0,
    leftIndent=8 * mm,
    bulletIndent=2.5 * mm,
    spaceAfter=1.2 * mm,
)
caption_style = ParagraphStyle(
    "CaptionCN",
    fontName="CN",
    fontSize=7.8,
    leading=11,
    textColor=MUTED,
    alignment=TA_CENTER,
    spaceBefore=1.2 * mm,
)


def figure(name, anchor, caption, kind="move"):
    return {"name": name, "anchor": anchor, "caption": caption, "kind": kind}


CHAPTERS = [
    {
        "title": "第一章：威廉·斯坦尼茨的两场胜局",
        "short": "第一章｜斯坦尼茨的两场胜局",
        "source": "11_chapter_one_steinitz_zh.md",
        "range": "原书印刷页 60-67",
        "version": "3",
        "output": "chess_middlegame_planning_chapter_one_steinitz_zh_proof_v3.pdf",
        "figures": [
            figure("page-063-diagram-1.png", "10. Bb3 c6", "黑方走完10... c6后的局面"),
            figure("page-065-diagram-1.png", "20. g5 h5", "黑方走完20... h5后的局面"),
            figure("page-067-diagram-1.png", "5. e3 O-O", "黑方走完5... O-O后的局面"),
            figure("page-068-diagram-1.png", "13... f4", "黑方走完13... f4后的局面"),
            figure("page-068-diagram-2.png", "23. g5 Bd8", "黑方走完23... Bd8后的局面"),
        ],
    },
    {
        "title": "第二章：计划的各个阶段",
        "short": "第二章｜计划的各个阶段",
        "source": "12_chapter_two_stages_zh.md",
        "range": "原书印刷页 68-86",
        "version": "3",
        "output": "chess_middlegame_planning_chapter_two_stages_zh_proof_v3.pdf",
        "figures": [
            figure("page-071-diagram-1.png", "9. Bxc6 bxc6", "黑方走完9... bxc6后的局面"),
            figure("page-073-diagram-1.png", "22. Rb1 a5", "黑方走完22... a5后的局面"),
            figure("page-074-diagram-1.png", "26... Bxa4", "黑方走完26... Bxa4后的局面"),
            figure("page-075-diagram-1.png", "32... f6 33. Qb2 Rf8", "黑方走完33... Rf8后的局面"),
            figure("page-077-diagram-1.png", "7... g6", "黑方走完7... g6后的局面"),
            figure("page-078-diagram-1.png", "14. Bb3 O-O", "黑方走完14... O-O后的局面"),
            figure("page-081-diagram-1.png", "27... b4", "黑方走完27... b4后的局面"),
            figure("page-082-diagram-2.png", "28... Re6", "黑方走完28... Re6后的局面"),
            figure("page-082-diagram-1.png", "32... c5", "黑方走完32... c5后的局面"),
            figure("page-084-diagram-1.png", "48. Kb1 Qf3", "黑方走完48... Qf3后的局面"),
            figure("page-087-diagram-1.png", "18. Bf2 Nh5", "黑方走完18... Nh5后的局面"),
            figure("page-087-diagram-2.png", "29. Qc1", "白方走完29. Qc1后的局面"),
            figure("page-088-diagram-1.png", "39. Kh1 Rd1", "黑方走完39... Rd1后的局面"),
        ],
    },
]


def read_blocks(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks = []
    buffer = []
    started = False

    def flush():
        if not buffer:
            return
        text = "\n".join(buffer).strip()
        buffer.clear()
        if not text:
            return
        move_match = re.fullmatch(r"(?:\*\*)?`([^`]+)`(?:\*\*)?", text)
        if move_match:
            blocks.append(("move", move_match.group(1)))
        else:
            blocks.append(("body", text))

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## CH"):
            flush()
            started = True
            continue
        if not started:
            continue
        if not stripped:
            flush()
            continue
        if stripped.startswith("#### "):
            flush()
            blocks.append(("h3", stripped[5:]))
            continue
        if stripped.startswith("### "):
            flush()
            blocks.append(("h2", stripped[4:]))
            continue
        if re.match(r"^\d+\.\s", stripped):
            flush()
            blocks.append(("bullet", re.sub(r"^\d+\.\s*", "", stripped)))
            continue
        buffer.append(line)
    flush()
    return blocks


def markup(text):
    value = escape(text)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = value.replace("  \n", "<br/>")
    value = value.replace("\n\n", "<br/><br/>").replace("\n", " ")
    return value


def paragraph_for(kind, text):
    if kind == "h2":
        return Paragraph(markup(text), chapter_heading)
    if kind == "h3":
        return Paragraph(markup(text), subheading)
    if kind == "move":
        return Paragraph(markup(text), move_style)
    if kind == "bullet":
        return Paragraph(markup(text), bullet_style, bulletText="•")
    return Paragraph(markup(text), body_style)


def diagram_card(spec):
    path = DIAGRAMS / spec["name"]
    with PILImage.open(path) as source:
        width, height = source.size
    target_width = 64 * mm
    picture = Image(str(path), width=target_width, height=target_width * height / width)
    contents = [picture, Paragraph(spec["caption"], caption_style)]
    table = Table([[contents]], colWidths=[84 * mm], hAlign="CENTER")
    table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1.4 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm),
            ]
        )
    )
    return table


def build_chapter(config):
    output = OUT / config["output"]
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=23 * mm,
        rightMargin=23 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        title=f'《国际象棋中局计划》{config["title"]}中文整章校样',
        author="中文翻译校样",
    )

    def header_footer(canvas, document):
        canvas.saveState()
        if document.page > 1:
            canvas.setStrokeColor(RULE)
            canvas.setLineWidth(0.45)
            canvas.line(23 * mm, A4[1] - 14 * mm, A4[0] - 23 * mm, A4[1] - 14 * mm)
            canvas.setFillColor(MUTED)
            canvas.setFont("CN", 7.7)
            canvas.drawString(23 * mm, A4[1] - 11 * mm, f'彼得·罗曼诺夫斯基《国际象棋中局计划》｜{config["short"]}')
            canvas.drawCentredString(A4[0] / 2, 9.5 * mm, str(document.page))
        canvas.restoreState()

    story = [
        Spacer(1, 48 * mm),
        Paragraph("《国际象棋中局计划》", cover_title),
        Spacer(1, 5 * mm),
        Paragraph(config["title"], cover_title),
        Spacer(1, 7 * mm),
        Paragraph(f'中文整章校样 · 版本 {config["version"]}', cover_subtitle),
        Spacer(1, 6 * mm),
        Paragraph(config["range"], cover_subtitle),
        PageBreak(),
    ]

    blocks = read_blocks(TRANS / config["source"])
    specs = config["figures"]
    placed = set()
    index = 0
    while index < len(blocks):
        kind, text = blocks[index]
        matches = [
            spec
            for spec in specs
            if spec["name"] not in placed
            and spec["kind"] == kind
            and spec["anchor"] in text
        ]
        if len(matches) > 1:
            raise ValueError(f'Multiple figures match block in {config["source"]}: {matches}')
        if not matches:
            story.append(paragraph_for(kind, text))
            index += 1
            continue

        spec = matches[0]
        placed.add(spec["name"])
        anchor = spec["anchor"]
        anchor_end = text.index(anchor) + len(anchor)
        before = text[:anchor_end].strip()
        after = text[anchor_end:].strip()
        if kind == "move" and spec["name"] == "page-087-diagram-2.png" and after == "g5":
            after = "29... g5"
        current = paragraph_for(kind, before)
        card = diagram_card(spec)

        if after:
            story.append(
                KeepTogether(
                    [current, Spacer(1, 1.2 * mm), card, Spacer(1, 1.5 * mm), paragraph_for(kind, after)]
                )
            )
            index += 1
            continue

        next_flowable = None
        if index + 1 < len(blocks):
            next_kind, next_text = blocks[index + 1]
            next_has_figure = any(
                candidate["name"] not in placed
                and candidate["kind"] == next_kind
                and candidate["anchor"] in next_text
                for candidate in specs
            )
            if not next_has_figure and next_kind not in {"h2", "h3"}:
                next_flowable = paragraph_for(next_kind, next_text)

        if len(before) <= 240:
            cluster = [current, Spacer(1, 1.2 * mm), card]
            if next_flowable is not None:
                cluster.extend([Spacer(1, 1.5 * mm), next_flowable])
                index += 1
            story.append(KeepTogether(cluster))
        else:
            story.append(current)
            cluster = [card]
            if next_flowable is not None:
                cluster.extend([Spacer(1, 1.5 * mm), next_flowable])
                index += 1
            story.append(KeepTogether(cluster))
        index += 1

    missing = [spec["name"] for spec in specs if spec["name"] not in placed]
    if missing:
        raise ValueError(f'Unplaced figures in {config["source"]}: {missing}')

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(output)


requested = set(sys.argv[1:])
for chapter in CHAPTERS:
    if not requested or chapter["source"] in requested:
        build_chapter(chapter)
